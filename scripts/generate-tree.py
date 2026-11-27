#!/usr/bin/env python3
"""Generate tree.json — the file index the directory browser reads.

index.html used to list directories through the GitHub contents API, which
costs one request per folder and allows anonymous callers 60 an hour. This
file replaces those calls: GitHub Pages serves it from the same origin as the
page, so browsing the repository costs no API requests at all.

Schema:
  {
    "branch": "main",
    "tree": [ {"path": "Pioneer_Models/DM32/keymap_DM32.bin", "size": 1024,
               "date": "2026-02-18 14:05"}, ... ],
    "folders": { "Pioneer_Models/DM32": {"date": "2026-02-18 14:05"}, ... }
  }

A file's date is its last commit (Zurich time); a folder's is its newest file's.
CI must check out the full history (fetch-depth: 0) for the dates to be right.

Only tracked files are listed, taken from `git ls-files` — those are exactly
the files GitHub Pages serves. Directories are not listed; the browser derives
them from the paths (git has no standalone directory objects either).

tree.json excludes itself. Listing it would make its own recorded size change
on every run, so CI would commit a new one forever.

Run by hand with `python3 scripts/generate-tree.py`; CI runs it on push.
Standard library only, matching generate-manifest.py.
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = "tree.json"
BRANCH = os.environ.get("TREE_BRANCH", "main")
ZONE = ZoneInfo("Europe/Zurich")


def format_date(timestamp):
    return datetime.fromtimestamp(timestamp, ZONE).strftime("%Y-%m-%d %H:%M")


def parse_log(text):
    """Output of `git log --format=%x00%ct --name-only` -> {path: unix time}.
    git log runs newest first, so a path's first sighting is its last change."""
    dates = {}
    for commit in text.split("\0"):
        lines = commit.splitlines()
        if not lines or not lines[0].strip():
            continue
        when = int(lines[0])
        for path in lines[1:]:
            if path and path not in dates:
                dates[path] = when
    return dates


def build_index(entries, branch, dates=None):
    """(path, size) pairs -> the tree.json document, sorted and self-excluding.
    With dates ({path: unix time}), files get a date and folders their newest."""
    dates = dates or {}
    tree, newest = [], {}
    for path, size in entries:
        if path == OUTPUT:
            continue
        entry = {"path": path, "size": size}
        when = dates.get(path)
        if when is not None:
            entry["date"] = format_date(when)
            parts = path.split("/")[:-1]
            for i in range(1, len(parts) + 1):
                folder = "/".join(parts[:i])
                newest[folder] = max(newest.get(folder, 0), when)
        tree.append(entry)
    tree.sort(key=lambda e: e["path"])
    index = {"branch": branch, "tree": tree}
    if newest:
        index["folders"] = {f: {"date": format_date(t)} for f, t in sorted(newest.items())}
    return index


def commit_dates():
    out = subprocess.check_output(
        ["git", "-C", ROOT, "-c", "core.quotepath=off", "log",
         "--format=%x00%ct", "--name-only", "--no-renames"])
    return parse_log(out.decode("utf-8"))


def render(index):
    return json.dumps(index, indent=1) + "\n"


def tracked_files():
    """Tracked paths with their on-disk sizes. Files listed by git but absent
    from the working tree are skipped rather than failing the run."""
    out = subprocess.check_output(["git", "-C", ROOT, "ls-files", "-z"])
    for path in out.decode("utf-8").split("\0"):
        if not path:
            continue
        full = os.path.join(ROOT, path)
        if os.path.isfile(full):
            yield path, os.path.getsize(full)


def main():
    try:
        entries = list(tracked_files())
        dates = commit_dates()
    except (subprocess.CalledProcessError, OSError) as exc:
        sys.stderr.write("error: listing tracked files failed: %s\n" % exc)
        return 1
    if not entries:
        sys.stderr.write("error: no tracked files found\n")
        return 1

    index = build_index(entries, BRANCH, dates)
    text = render(index)
    count = len(index["tree"])          # after self-exclusion, so runs agree
    full = os.path.join(ROOT, OUTPUT)
    if os.path.exists(full):
        with open(full, encoding="utf-8") as fp:
            if fp.read() == text:
                print("checked %s: no changes (%d files)" % (OUTPUT, count))
                return 0
    with open(full, "w", encoding="utf-8") as fp:
        fp.write(text)
    print("wrote %s: %d files (%d bytes)" % (OUTPUT, count, len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
