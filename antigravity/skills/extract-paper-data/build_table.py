#!/usr/bin/env python3
"""Assemble extraction notes into a plain HTML table, and validate the Paperpile links.

Reads one `[citekey]-extraction-notes.md` per paper, takes the `## Extracted` block from
each, and emits a single HTML file: one row per paper, one column per attribute, followed
by the reference list. Deliberately plain — the point is legibility and correct links, not
visual design.

Usage:
    python3 build_table.py config.json                 # write the HTML named in the config
    python3 build_table.py config.json --check         # validate only, write nothing

Config (JSON):
{
  "notes_dir":  "/path/to/scratch",              # holds the *-extraction-notes.md files
  "out":        "/path/to/table.html",           # where to write
  "title":      "Data sources and computational methods",
  "subtitle":   "Five papers from the Paperpile folder 'ancient genomes'",   # optional
  "generated":  "25 August 2026",                                            # optional
  "size":       "M",                             # optional; S/M/L, enforces the per-cell ceiling
  "order":      ["Citekey2026-aa", "Citekey2026-bb"],   # row order, top to bottom
  "labels":     {"Citekey2026-aa": "Bossoms Mesa 2026<br>Nature"},  # optional row labels
  "columns":    ["Study ID / DOI", "..."],       # optional; default = order in first file
  "references": [                                # optional; rendered below the table
    {"title": "...", "authors": "Last F, Last F", "journal": "Nature", "year": "2026",
     "type": "Journal article", "doi": "https://doi.org/10.1000/xyz", "note": "..."}
  ]
}

Exit status is 1 if any hard error was found (a missing column, an unconvertible link, a
page number that disagrees with its link, or — when "size" is set — a cell over that size's
character ceiling). Warnings do not change the exit status.
"""

import html
import json
import os
import re
import sys

BULLET = re.compile(r"^- \*\*(.+?)\*\*:\s*(.*)$")
# Per-cell ceilings for the S/M/L table sizes, counted in user-visible characters.
SIZES = {"S": 120, "M": 250, "L": 600}
PAPERPILE = re.compile(r"/view/\?")

errors = []
warnings = []


def normalize(key):
    """Column labels drift between em dash and hyphen; treat them as the same column."""
    return key.replace("—", "-").replace("–", "-").strip()


# --------------------------------------------------------------------------- parsing

def parse_notes(path):
    """Return {column: markdown value} from the `## Extracted` block of a notes file."""
    with open(path, encoding="utf-8") as handle:
        text = handle.read()

    if "## Extracted" not in text:
        errors.append("%s: no '## Extracted' section" % os.path.basename(path))
        return {}

    block = text.split("## Extracted", 1)[1]
    rows, key, buffer = {}, None, []

    for line in block.splitlines():
        match = BULLET.match(line)
        if match:
            if key:
                rows[key] = " ".join(buffer).strip()
            key, buffer = normalize(match.group(1)), [match.group(2)]
        elif key is not None and line.strip():
            if line.startswith("## "):
                break
            buffer.append(line.strip())

    if key:
        rows[key] = " ".join(buffer).strip()
    return rows


def scan_url(text, open_paren):
    """Find the URL in `](url)` starting at the '(' index. Returns (url, index_after).

    A well-formed value has balanced parentheses and is found by depth counting. A value
    whose #hl still contains a stray '(' — which the skill forbids, but which happens —
    is recovered by falling back to the last ')' before the next space, since a URL never
    contains whitespace. Recovery is reported as a warning so the source gets fixed.
    """
    start = open_paren + 1
    end = start
    while end < len(text) and not text[end].isspace():
        end += 1
    segment = text[start:end]

    depth = 1
    for index, char in enumerate(segment):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return segment[:index], start + index + 1

    if ")" in segment:
        index = segment.rfind(")")
        return segment[:index], start + index + 1

    return None, None


def render_inline(markdown, where):
    """Convert inline Markdown to HTML: links, bold, italic. Everything else is escaped.

    Returns (html, visible). `visible` is the text a reader actually sees — a link
    contributes its anchor text and not the URL behind it — which is what the size
    ceiling is defined against, so the check and the rendering never disagree.
    """
    out, plain, index = [], [], 0

    while index < len(markdown):
        if markdown[index] == "[":
            close = markdown.find("]", index)
            if close != -1 and close + 1 < len(markdown) and markdown[close + 1] == "(":
                url, after = scan_url(markdown, close + 1)
                if url is not None:
                    label = markdown[index + 1:close]
                    check_link(url, label, where)
                    out.append('<a href="%s">%s</a>'
                               % (html.escape(url, quote=True), html.escape(label)))
                    plain.append(label)
                    index = after
                    continue
                errors.append("%s: could not parse the link starting at %r"
                              % (where, markdown[index:index + 60]))
        out.append(html.escape(markdown[index]))
        plain.append(markdown[index])
        index += 1

    text = "".join(out)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", text)

    visible = "".join(plain)
    visible = re.sub(r"\*\*(.+?)\*\*", r"\1", visible)
    visible = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"\1", visible)
    return text, visible


# ------------------------------------------------------------------------ validation

def check_link(url, label, where):
    if not PAPERPILE.search(url):
        return

    page = re.search(r"[?&]page=(\d+)", url)
    shown = re.search(r"\bp\.\s*(\d+)", label)
    if page and shown and page.group(1) != shown.group(1):
        errors.append("%s: link says page=%s but its text reads 'p. %s'"
                      % (where, page.group(1), shown.group(1)))
    if shown and not page:
        warnings.append("%s: link text reads 'p. %s' but the URL has no page parameter"
                        % (where, shown.group(1)))

    fragment = url.split("#hl=", 1)
    if len(fragment) == 1:
        warnings.append("%s: link has no #hl anchor, so nothing will be highlighted" % where)
        return

    anchor = fragment[1]
    if not anchor.strip():
        errors.append("%s: link has an empty #hl anchor" % where)
    if "(" in anchor or ")" in anchor:
        warnings.append("%s: #hl contains a parenthesis — remove it at the source, it is "
                        "what breaks these links" % where)
    if anchor.endswith("..."):
        warnings.append("%s: #hl ends with '...', so it has no closing anchor and will "
                        "highlight the wrong span" % where)
    if "+" in anchor:
        warnings.append("%s: #hl contains '+' — spaces must be encoded as %%20" % where)


def report(notes, level, examples=3):
    """Group repeated notes by kind so one systematic mistake is one line, not fifty."""
    kinds = {}
    for note in notes:
        where, _, what = note.partition(": ")
        kinds.setdefault(what, []).append(where)

    for what, places in sorted(kinds.items(), key=lambda item: -len(item[1])):
        shown = ", ".join(places[:examples])
        if len(places) > examples:
            shown += ", and %d more" % (len(places) - examples)
        print("%s (%d): %s\n    at %s" % (level, len(places), what, shown), file=sys.stderr)


# -------------------------------------------------------------------------- rendering

STYLE = """
:root {
  --ink: #111; --muted: #555; --line: #ccc; --hair: #e5e5e5;
  --ground: #fff; --head: #f5f5f5; --link: #0b4fa8;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --ink: #e8e8e8; --muted: #a0a0a0; --line: #444; --hair: #2c2c2c;
    --ground: #131313; --head: #1d1d1d; --link: #7fb3f0;
  }
}
:root[data-theme="dark"] {
  --ink: #e8e8e8; --muted: #a0a0a0; --line: #444; --hair: #2c2c2c;
  --ground: #131313; --head: #1d1d1d; --link: #7fb3f0;
}
body {
  margin: 0; padding: 32px 24px 64px; background: var(--ground); color: var(--ink);
  font: 15px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
}
.wrap { max-width: 1400px; margin: 0 auto; }
h1 { font-size: 22px; font-weight: 600; margin: 0 0 6px; }
h2 { font-size: 16px; font-weight: 600; margin: 40px 0 12px; }
p.sub { color: var(--muted); margin: 0 0 4px; }
p.stamp { color: var(--muted); font-size: 13px; margin: 0 0 24px; }
.scroll { overflow-x: auto; border: 1px solid var(--line); }
table { border-collapse: collapse; width: 100%; min-width: 1100px; font-size: 13px; }
th, td { border-bottom: 1px solid var(--hair); padding: 10px 12px; text-align: left;
         vertical-align: top; }
thead th { background: var(--head); border-bottom: 1px solid var(--line);
           font-weight: 600; position: sticky; top: 0; }
tbody th { font-weight: 600; white-space: nowrap; }
tbody tr:last-child th, tbody tr:last-child td { border-bottom: none; }
a { color: var(--link); }
ol.refs { list-style: none; margin: 0; padding: 0; }
.ref { padding: 12px 0; border-bottom: 1px solid var(--hair); }
.ref:last-child { border-bottom: none; }
.ref p { margin: 0; }
.ref .t { font-weight: 600; }
.ref .a, .ref .m { color: var(--muted); font-size: 14px; }
.ref .d { font-size: 13px; word-break: break-all; }
.ref .n { color: var(--muted); font-size: 13px; margin-top: 6px; }
"""

PAGE = """<title>%(title)s</title>
<style>%(style)s</style>
<div class="wrap">
<h1>%(title)s</h1>
%(subtitle)s%(stamp)s
<div class="scroll">
<table>
<thead><tr><th>Paper</th>%(head)s</tr></thead>
<tbody>
%(body)s
</tbody>
</table>
</div>
%(references)s
</div>
"""


def render_references(references):
    if not references:
        return ""

    items = []
    for ref in references:
        meta = " &middot; ".join(
            part for part in (
                "<em>%s</em>" % html.escape(ref["journal"]) if ref.get("journal") else "",
                html.escape(ref.get("year", "")),
                html.escape(ref.get("type", "")),
            ) if part
        )
        doi = ref.get("doi", "")
        items.append(
            '<li class="ref"><p class="t">%s</p><p class="a">%s</p><p class="m">%s</p>%s%s</li>' % (
                html.escape(ref.get("title", "")),
                html.escape(ref.get("authors", "")),
                meta,
                '<p class="d"><a href="%s">%s</a></p>' % (html.escape(doi, quote=True),
                                                          html.escape(doi)) if doi else "",
                '<p class="n">%s</p>' % html.escape(ref["note"]) if ref.get("note") else "",
            )
        )
    return '<h2>References</h2>\n<ol class="refs">\n%s\n</ol>' % "\n".join(items)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)

    check_only = "--check" in sys.argv[1:]
    with open(sys.argv[1], encoding="utf-8") as handle:
        config = json.load(handle)

    notes_dir = config["notes_dir"]
    order = config["order"]

    papers = {}
    for citekey in order:
        path = os.path.join(notes_dir, "%s-extraction-notes.md" % citekey)
        if not os.path.exists(path):
            errors.append("%s: no notes file at %s" % (citekey, path))
            papers[citekey] = {}
            continue
        papers[citekey] = parse_notes(path)

    columns = [normalize(c) for c in config.get("columns", [])]
    if not columns:
        for citekey in order:
            if papers[citekey]:
                columns = list(papers[citekey].keys())
                break

    for citekey in order:
        for column in columns:
            if column not in papers[citekey]:
                errors.append("%s: missing the column %r" % (citekey, column))

    size = config.get("size")
    ceiling = None
    if size is not None:
        ceiling = SIZES.get(str(size).strip().upper())
        if ceiling is None:
            errors.append("config: size %r is not one of %s"
                          % (size, ", ".join(sorted(SIZES))))

    labels = config.get("labels", {})
    rows = []
    for citekey in order:
        cells = []
        for column in columns:
            where = "%s / %s" % (citekey, column)
            cell, visible = render_inline(papers[citekey].get(column, ""), where)
            if ceiling is not None and len(visible) > ceiling:
                errors.append("%s: %d characters of visible text, %d over the %s ceiling of %d"
                              % (where, len(visible), len(visible) - ceiling,
                                 str(size).strip().upper(), ceiling))
            cells.append("<td>%s</td>" % cell)
        rows.append("<tr><th>%s</th>%s</tr>"
                    % (labels.get(citekey, html.escape(citekey)), "".join(cells)))

    report(warnings, "warning")
    report(errors, "ERROR")

    if check_only:
        print("%d column(s) x %d paper(s); %d error(s), %d warning(s)"
              % (len(columns), len(order), len(errors), len(warnings)))
        return 1 if errors else 0

    page = PAGE % {
        "title": html.escape(config.get("title", "Extracted data")),
        "style": STYLE,
        "subtitle": '<p class="sub">%s</p>\n' % html.escape(config["subtitle"])
                    if config.get("subtitle") else "",
        "stamp": '<p class="stamp">%s</p>\n' % html.escape(config["generated"])
                 if config.get("generated") else "",
        "head": "".join("<th>%s</th>" % html.escape(column) for column in columns),
        "body": "\n".join(rows),
        "references": render_references(config.get("references")),
    }

    out = config["out"]
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as handle:
        handle.write(page)

    print("wrote %s — %d paper(s) x %d column(s), %d error(s), %d warning(s)"
          % (out, len(order), len(columns), len(errors), len(warnings)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
