#!/usr/bin/env python3
"""Generate models.json consumed by the swissmicros-esp32s3-toolkit firmware.

The firmware (esp32_calculator_flasher/main/firmware_download.cpp) fetches this
file from raw.githubusercontent.com/.../main/models.json and then downloads each
listed file directly from the same raw base. So every path here must be
repo-relative (e.g. "Voyager_Models/DM10_34.hex"), keeping its top-level folder
so the device stores it at /data/<path>.

Schema:
  {
    "voyager_version": "34",                  # opaque; bumped when Voyager changes
    "voyager": ["Voyager_Models/<file>", ...],
    "pioneer": [ { "name": "DM32",
                   "files": ["Pioneer_Models/DM32/<file>", ...] }, ... ]
  }

Loose top-level files in Pioneer_Models/ (e.g. DM42_qspi_3.x.bin) are not model
directories and are intentionally ignored.
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)


def list_files(top):
    """Sorted repo-relative paths of every file under `top` (recursive)."""
    out = []
    for dirpath, dirnames, filenames in os.walk(top):
        dirnames.sort()
        for name in sorted(filenames):
            out.append(os.path.join(dirpath, name).replace(os.sep, "/"))
    return out


def voyager_version(files):
    """Shared version tag from the .hex filenames: the last underscore-delimited
    token before .hex (DM10_34.hex, DM15_M80_34.hex -> "34")."""
    tags = sorted({
        re.sub(r"\.hex$", "", os.path.basename(p)).rsplit("_", 1)[-1]
        for p in files if p.endswith(".hex")
    })
    if len(tags) == 1:
        return tags[0]
    if len(tags) > 1:
        sys.stderr.write("warning: Voyager files differ in version tag: %s\n" % tags)
        return "-".join(tags)
    sys.stderr.write("warning: no version tag in Voyager .hex filenames\n")
    return ""


manifest = {}

voyager = list_files("Voyager_Models") if os.path.isdir("Voyager_Models") else []
if voyager:
    ver = voyager_version(voyager)
    if ver:
        manifest["voyager_version"] = ver
    manifest["voyager"] = voyager

pioneer = []
if os.path.isdir("Pioneer_Models"):
    for name in sorted(os.listdir("Pioneer_Models")):
        d = os.path.join("Pioneer_Models", name)
        if not os.path.isdir(d):
            continue  # skip loose top-level files
        files = list_files(d)
        if files:
            pioneer.append({"name": name, "files": files})
manifest["pioneer"] = pioneer

if not voyager and not pioneer:
    sys.stderr.write("error: no model files found\n")
    sys.exit(1)

with open("models.json", "w") as fp:
    json.dump(manifest, fp, indent=2)
    fp.write("\n")

print("wrote models.json: %d voyager files, %d pioneer models (%d bytes)"
      % (len(voyager), len(pioneer), os.path.getsize("models.json")))
