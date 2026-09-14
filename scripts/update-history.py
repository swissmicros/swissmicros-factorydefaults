#!/usr/bin/env python3
"""Generate the vendored SwissMicros firmware history files.

Fetches the upstream history pages and rewrites them as Markdown, one file per
Pioneer model plus one shared file per platform (DMCP, DMCP5) and one for the
Voyager line. Run it by hand when upstream publishes a new release:

    python3 scripts/update-history.py

Output is deterministic — no fetch date is stamped into the files — so a run
that finds nothing new leaves the working tree clean. Files are written only
when their content actually changes.

The per-model files land inside Pioneer_Models/<MODEL>/, which generate-manifest.py
walks recursively, so they enter models.json and reach calculators. The two
platform files sit loose in Pioneer_Models/, which that script skips: they are
documentation and are not shipped. Voyager_Models/ is listed wholesale, so
Voyager_Models/HISTORY.md does ship; voyager_version() filters on .hex and is
unaffected by it.

Standard library only, matching generate-manifest.py.
"""

import collections
import html
import html.parser
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

Platform = collections.namedtuple("Platform", "name relpath url")

BASE = "https://technical.swissmicros.com"

DMCP = Platform("DMCP", "../DMCP_HISTORY.md", BASE + "/dmcp/firmware/history.html")
DMCP5 = Platform("DMCP5", "../DMCP5_HISTORY.md", BASE + "/dmcp/firmware_dmcp5/history.html")

# output path -> (source url, platform history to cross-link, or None)
SOURCES = collections.OrderedDict([
    ("Pioneer_Models/DM32/HISTORY.md", (BASE + "/dm32/firmware/history.html", DMCP5)),
    ("Pioneer_Models/DM42/HISTORY.md", (BASE + "/dm42/firmware/history.html", DMCP)),
    ("Pioneer_Models/DM42n/HISTORY.md", (BASE + "/dm42/firmware_dm42n/history.html", DMCP5)),
    ("Pioneer_Models/DM41X/HISTORY.md", (BASE + "/dm41x/firmware/history.html", DMCP)),
    ("Pioneer_Models/DMCP_HISTORY.md", (DMCP.url, None)),
    ("Pioneer_Models/DMCP5_HISTORY.md", (DMCP5.url, None)),
])

VOYAGER_PATH = "Voyager_Models/HISTORY.md"
VOYAGER_URL = BASE + "/voyager/firmware/history.txt"

# Escape only what would otherwise change how the text renders. Underscores are
# left alone: CommonMark does not treat intra-word "_" as emphasis, and escaping
# would turn DM15_M80_V16a_32k.hex into noise.
_ESCAPE = re.compile(r"([\\`*<])")


def escape_md(text):
    return _ESCAPE.sub(r"\\\1", text)


def collapse(text):
    """Source text is hard-wrapped mid-sentence; join it back to one line."""
    return " ".join(text.split())


def iso_date(year, month, day):
    return "%04d-%02d-%02d" % (int(year), int(month), int(day))


# ---------------------------------------------------------------- HTML pages

# "DM32 v2.11:  2025-12-05", "DM42n v3.26 (built with DMCP5 3.55): 2025-11-14",
# "DM32 v2.02 : 2023-05-21", "DMCP v3.8 : 2018/07/03", "v3.0 : 2017/12/08".
_H3_DATE = re.compile(r"^(.*?)\s*:\s*(\d{4})[-/](\d{1,2})[-/](\d{1,2})\s*$")


def format_heading(text):
    """Release heading -> "Name — YYYY-MM-DD". Headings that carry no date
    (dm32's "End of Beta Phase") pass through unchanged."""
    text = collapse(text)
    m = _H3_DATE.match(text)
    if not m:
        return text
    return "%s — %s" % (m.group(1), iso_date(m.group(2), m.group(3), m.group(4)))


class _HistoryParser(html.parser.HTMLParser):
    """Collects (kind, value) events from an upstream history page.

    The page body is flat — h1, h3, div.sub and ul are siblings — so a shallow
    mode flag is enough. Bullet text is gathered as segments so that anchors can
    become Markdown links while the surrounding prose is escaped.
    """

    def __init__(self):
        html.parser.HTMLParser.__init__(self, convert_charrefs=True)
        self.events = []
        self.mode = None        # "h1", "h3", "sub", "li"
        self.buf = []           # rendered pieces of the current element
        self.link_href = None
        self.link_buf = []

    # -- helpers

    def _flush(self):
        value = collapse("".join(self.buf))
        if value:
            self.events.append((self.mode, value))
        self.mode = None
        self.buf = []

    def _add_text(self, data):
        if self.link_href is not None:
            self.link_buf.append(data)
        else:
            self.buf.append(escape_md(data))

    # -- parser hooks

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        cls = attrs.get("class", "")
        # Upstream leaves <li> unclosed in places. Emit whatever is buffered
        # before opening a new block, rather than dropping it.
        if tag in ("h1", "h3", "li", "ul", "hr", "p") or tag == "div":
            if self.mode and self.mode != "a":
                self._close_link()
                self._flush()
        if tag == "h1":
            self.mode, self.buf = "h1", []
        elif tag == "h3":
            self.mode, self.buf = "h3", []
        elif tag == "div" and cls == "sub":
            self.mode, self.buf = "sub", []
        elif tag == "div" and cls == "highlighted":
            self.mode, self.buf = "highlighted", []
        elif tag == "li":
            self.mode, self.buf = "li", []
        elif tag == "a" and self.mode == "li":
            self.link_href = attrs.get("href", "")
            self.link_buf = []

    def _close_link(self):
        if self.link_href is None:
            return
        label = escape_md(collapse("".join(self.link_buf)))
        self.buf.append("[%s](%s)" % (label, self.link_href))
        self.link_href, self.link_buf = None, []

    def handle_endtag(self, tag):
        if tag == "a":
            self._close_link()
        elif tag == "ul" and self.mode == "li":
            self._close_link()
            self._flush()
        elif tag in ("h1", "h3", "li") and self.mode:
            self._flush()
        elif tag == "div" and self.mode in ("sub", "highlighted"):
            self._flush()

    def handle_data(self, data):
        if self.mode:
            self._add_text(data)

    def handle_comment(self, data):
        pass

    def finish(self):
        """Emit anything still buffered when the document ends."""
        if self.mode:
            self._close_link()
            self._flush()


def convert_html(page, platform=None):
    """Upstream history HTML -> Markdown."""
    parser = _HistoryParser()
    parser.feed(page)
    parser.close()
    parser.finish()

    title = "Firmware History"
    highlighted = None
    body = []
    saw_heading = False

    def push_heading(level, text):
        if not body or body[-1] != "":
            body.append("")
        body.append("#" * level + " " + text)
        body.append("")

    for kind, value in parser.events:
        if kind == "h1":
            title = value
        elif kind == "highlighted":
            highlighted = value
        elif kind == "h3":
            push_heading(2, format_heading(value))
            saw_heading = True
        elif kind == "sub" and saw_heading:
            push_heading(3, value)
        elif kind == "li" and saw_heading:
            body.append("- " + value)

    out = ["# " + title]
    if highlighted:
        out += ["", "> " + highlighted]
    if platform:
        out += ["",
                "Platform firmware: see [%s system firmware history](%s)\n([upstream](%s))."
                % (platform.name, platform.relpath, platform.url)]
    out += body

    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.rstrip("\n") + "\n"


# ------------------------------------------------------------ Voyager text

# Release heading at column 0: "V34: 2025-04-15", "V32: 31.08.2021",
# "V2: 21.2.2012:" (trailing colon), "V30: 17.01.2020 " (trailing space).
_VOY_HEADING = re.compile(r"^(V\d+[A-Za-z]?)\s*:\s*(.+?)\s*$")
_VOY_ISO = re.compile(r"^(\d{4})-(\d{1,2})-(\d{1,2}):?$")
_VOY_DOTTED = re.compile(r"^(\d{1,2})\.(\d{1,2})\.(\d{4}):?$")

# A colon does not make a model label — "Bugfix:" and "GTO I:" are prose. Only
# these shapes count: ALL, DM1x, DM1X, DMXX, DM15/16, DM15_M80, DM15_Mxx.
_VOY_MODEL = re.compile(r"^(?:ALL|DM[0-9xX]+(?:[/_][0-9A-Za-z]+)*)$")

# An item inside a "DM1x:" block: three spaces then "- ".
_VOY_BLOCK_ITEM = re.compile(r"^\s+-\s+(.*)$")


def _voy_date(token):
    m = _VOY_ISO.match(token)
    if m:
        return iso_date(m.group(1), m.group(2), m.group(3))
    m = _VOY_DOTTED.match(token)
    if m:
        return iso_date(m.group(3), m.group(2), m.group(1))
    return token.rstrip(":")


def _voy_split_label(text):
    """Return (model, rest) if the line opens with a model label, else None.

    Recognises "DM1x: rest", "DM1x:" (block header) and "DM41 - rest". The
    separator-less form V21 uses ("DM1X fixed PSE") is deliberately not
    recognised: telling it from ordinary prose would be guesswork.
    """
    if ":" in text:
        label, _, rest = text.partition(":")
        if _VOY_MODEL.match(label.strip()):
            return label.strip(), rest.strip()
    m = re.match(r"^(\S+)\s+-\s+(.*)$", text)
    if m and _VOY_MODEL.match(m.group(1)):
        return m.group(1), m.group(2).strip()
    return None


def convert_voyager(text):
    """Upstream Voyager history.txt -> Markdown, mirroring the source's
    version-major order."""
    body = []
    pending_note = None
    open_model = None      # the "### model" section still accepting bullets
    in_block = False       # inside a "DM1x:" block, so "- " items belong to it

    def push_heading(level, text):
        if not body or body[-1] != "":
            body.append("")
        body.append("#" * level + " " + text)
        body.append("")

    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue

        indented = line[:1].isspace()

        if not indented:
            if line.startswith("!!!"):
                pending_note = collapse(line)
                continue
            m = _VOY_HEADING.match(line)
            if m:
                push_heading(2, "%s — %s" % (m.group(1), _voy_date(m.group(2))))
                if pending_note:
                    body.append("> " + escape_md(pending_note))
                    body.append("")
                    pending_note = None
                open_model = None
                in_block = False
                continue
            continue  # the "Firmware History" banner line and any other stray text

        stripped = line.strip()

        item = _VOY_BLOCK_ITEM.match(line)
        if item and in_block:
            body.append("- " + escape_md(collapse(item.group(1))))
            continue

        split = _voy_split_label(stripped)
        if split:
            model, rest = split
            # V27 lists DM1x twice in a row and V33 lists DM16 twice; repeating
            # the heading adds nothing, so keep the open section instead.
            if model != open_model:
                push_heading(3, model)
                open_model = model
            if rest:                           # label and text on one line
                body.append("- " + escape_md(collapse(rest)))
                in_block = False
            else:                              # block header: items follow
                in_block = True
            continue

        if item:                               # a "- " item with no open block
            stripped = item.group(1)
        body.append("- " + escape_md(collapse(stripped)))
        open_model = None
        in_block = False

    out = ["# Voyager Firmware History"] + body
    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.rstrip("\n") + "\n"


# ------------------------------------------------------------------ driver

def fetch(url):
    """Network seam — kept thin so the converters stay testable offline."""
    with urllib.request.urlopen(url, timeout=60) as resp:
        if resp.status != 200:
            raise RuntimeError("%s returned HTTP %s" % (url, resp.status))
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset)


def write_if_changed(path, text):
    full = os.path.join(ROOT, path)
    if os.path.exists(full):
        with open(full, encoding="utf-8") as fp:
            if fp.read() == text:
                return False
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fp:
        fp.write(text)
    return True


def main():
    jobs = [(path, url, platform, convert_html)
            for path, (url, platform) in SOURCES.items()]
    jobs.append((VOYAGER_PATH, VOYAGER_URL, None, convert_voyager))

    changed = []
    for path, url, platform, convert in jobs:
        try:
            source = fetch(url)
        except Exception as exc:
            sys.stderr.write("error: fetching %s for %s failed: %s\n" % (url, path, exc))
            return 1
        if convert is convert_html:
            text = convert(source, platform)
        else:
            text = convert(source)
        if write_if_changed(path, text):
            changed.append(path)

    if changed:
        print("wrote %d of %d history files: %s"
              % (len(changed), len(jobs), ", ".join(changed)))
    else:
        print("checked %d history files: no changes" % len(jobs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
