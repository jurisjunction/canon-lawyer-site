"""reflection.py: a reflection written in a doc, made into a page of the site.

    python3 reflection.py DOC.md SLUG [--date 2026-11-29] [--eyebrow "a layman's reading"]
                          [--register "a layman's reflection"] [--description "..."]
                          [--blurb "..."] [--dry-run]

DOC.md is the reflection as markdown, as the doc's own Export (Markdown) gives it:

    # Title
    Nov 18, 2026 · @Richard Verver          (the byline: optional; its date is used)
    The lead, one paragraph.
    ## A section
    Paragraphs, with *italics*, **bold** and [links](/music/#somewhere).
    > An indented quotation (one paragraph per line)
    - a list
    ## To watch                              (optional: a note in the small type)
    ## Sources                               (the rest, in the small type)

It writes _src/pages/17<letter>-reflections-SLUG.html (the next letter, or the same file if
the slug is already a page) and puts the reflection at the top of the reflections index
(or, if it is already there, leaves its entry alone unless --blurb is given). Then run
python3 build.py as usual; the build makes the PDF, the sitemap and llms.txt.

Links to the site's own writing: a title of a reflection, essay or colloquy, written in
*italics* in the doc, becomes a link to that page (its first mention in the text, and every
mention in the small type); so does a plain title in a sentence that begins "Kin on this
site". Every link made is listed, and so is any title found in plain text and left alone.
"""
import argparse
import datetime
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
PAGES = ROOT / "_src" / "pages"
INDEX = PAGES / "16-reflections.html"
SMALL = ("To watch", "Sources", "A note on sources")
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


# ---------------------------------------------------------------- the site's titles
def front(path):
    s = path.read_text(encoding="utf-8")
    m = re.match(r"\s*<!--(.*?)-->", s, re.S)
    if not m:
        return {}
    d = {}
    for line in m.group(1).strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            d[k.strip()] = v.strip()
    return d


def site_titles(own_path):
    """title (and crumb) -> path, for every reflection, essay and colloquy but this one"""
    t = {}
    for p in sorted(PAGES.glob("*.html")):
        d = front(p)
        path = d.get("path", "")
        if not path.startswith(("/reflections/", "/essays/", "/colloquies/")) or path == own_path:
            continue
        if path.count("/") < 3:          # the index pages themselves
            continue
        for k in ("title", "crumb"):
            if d.get(k):
                t.setdefault(d[k], path)
    return t


# ---------------------------------------------------------------- inline markdown
ESC = {c: chr(0xE000 + i) for i, c in enumerate("\\`*_{}[]()#+-.!>|~")}
UNESC = {v: k for k, v in ESC.items()}


def curly(s):
    s = re.sub(r'(^|[\s(\[—–/])"', r"\1“", s)
    s = s.replace('"', "”")
    s = re.sub(r"(^|[\s(\[—–/])'", r"\1‘", s)
    return s.replace("'", "’")


def emph(s):
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"(?<![\w_])_(?!\s)(.+?)(?<!\s)_(?![\w_])", r"<em>\1</em>", s)
    return s


def inline(s):
    """markdown to HTML for one block of text: escapes, links, curly quotes, emphasis"""
    s = re.sub(r"\\(.)", lambda m: ESC.get(m.group(1), m.group(1)), s)
    out, pos = [], 0
    for m in re.finditer(r"\[([^\]]+)\]\(([^)\s]+)\)", s):
        out.append(emph(curly(html.escape(s[pos:m.start()], quote=False))))
        text = emph(curly(html.escape(m.group(1), quote=False)))
        out.append(f'<a href="{html.escape(m.group(2))}">{text}</a>')
        pos = m.end()
    out.append(emph(curly(html.escape(s[pos:], quote=False))))
    return "".join(out).translate(str.maketrans(UNESC))


def plain(s):
    return re.sub(r"<[^>]+>", "", inline(s))


# ---------------------------------------------------------------- linking the site's titles
class Linker:
    def __init__(self, titles):
        self.titles = titles
        self.done = set()           # pages already linked in the text
        self.made, self.missed = [], []
        keys = sorted((curly(html.escape(k, quote=False)) for k in titles), key=len, reverse=True)
        self.by_html = {curly(html.escape(k, quote=False)): v for k, v in titles.items()}
        self.alt = "|".join(re.escape(k) for k in keys) or r"(?!)"

    def __call__(self, h, small=False):
        if not self.titles:
            return h
        # links already in the doc are left as they are
        parts = re.split(r"(<a [^>]*>.*?</a>)", h)

        def italic(m):
            k, path = m.group(1), self.by_html[m.group(1)]
            if small or path not in self.done:
                self.done.add(path)
                self.made.append((k, path, "italic"))
                return f'<a href="{path}">{k}</a>' if small else f'<a href="{path}"><em>{k}</em></a>'
            return m.group(0)

        def one(mm):
            k, path = mm.group(1), self.by_html[mm.group(1)]
            self.made.append((k, path, "kin"))
            return f'<a href="{path}">{k}</a>'

        def kin(m):
            return re.sub(rf"(?<![\w>])({self.alt})(?![\w<])", one, m.group(0))

        for i in range(0, len(parts), 2):
            # an italic title: <em>Title</em>
            parts[i] = re.sub(rf"<em>({self.alt})</em>", italic, parts[i])
            # a plain title in a sentence that begins "Kin on this site"
            parts[i] = re.sub(r"Kin on this site[^.]*\.", kin, parts[i])
        h = "".join(parts)
        # plain titles left alone: listed, for a look
        for m in re.finditer(rf"(?<![\w>])({self.alt})(?![\w<])", re.sub(r"<a [^>]*>.*?</a>", "", h)):
            self.missed.append(m.group(1))
        return h


# ---------------------------------------------------------------- the document
def blocks(md):
    """split markdown into blocks: ('h2'|'h3'|'p'|'qn'|'ul'|'ol', content)"""
    out = []
    for chunk in re.split(r"\n\s*\n", md.strip()):
        lines = [l.rstrip() for l in chunk.strip().splitlines() if l.strip()]
        if not lines:
            continue
        first = lines[0]
        if first.startswith("### "):
            out.append(("h3", first[4:].strip()))
            lines = lines[1:]
        elif first.startswith("## "):
            out.append(("h2", first[3:].strip()))
            lines = lines[1:]
        if not lines:
            continue
        if all(l.startswith(">") for l in lines):
            for l in lines:
                t = l.lstrip(">").strip()
                if t:
                    out.append(("qn", t))
        elif all(re.match(r"[-*] ", l) for l in lines):
            out.append(("ul", [l[2:].strip() for l in lines]))
        elif all(re.match(r"\d+[.)] ", l) for l in lines):
            out.append(("ol", [re.sub(r"^\d+[.)] ", "", l).strip() for l in lines]))
        else:
            out.append(("p", " ".join(lines)))
    return out


def next_file(slug):
    have = list(PAGES.glob(f"17*-reflections-{slug}.html"))
    if have:
        return have[0]
    letters = []
    for p in PAGES.glob("17*-reflections-*.html"):
        m = re.match(r"17([a-z]?)-reflections-", p.name)
        if m:
            letters.append(m.group(1) or "a")
    nxt = chr(max(map(ord, letters)) + 1) if letters else "c"
    if nxt > "z":
        sys.exit("reflection.py: the 17 prefixes are used up; choose a file name by hand")
    return PAGES / f"17{nxt}-reflections-{slug}.html"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("doc")
    ap.add_argument("slug")
    ap.add_argument("--date")
    ap.add_argument("--eyebrow", default="a layman’s reading")
    ap.add_argument("--register", default="a layman's reflection")
    ap.add_argument("--description")
    ap.add_argument("--blurb")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--out", help="write the page here instead (for a look); the index is left alone")
    a = ap.parse_args()
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", a.slug):
        sys.exit("reflection.py: the slug is lowercase words joined by hyphens")

    md = Path(a.doc).read_text(encoding="utf-8").replace("\r\n", "\n")
    lines = md.split("\n")
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if not lines[i].startswith("# "):
        sys.exit("reflection.py: the doc must begin with '# Title'")
    title = lines[i][2:].strip()
    rest = lines[i + 1:]
    # the byline: a line with a date and/or an @name, before the lead
    date = None
    while rest and not rest[0].strip():
        rest.pop(0)
    if rest and (re.search(r"\b(" + "|".join(MONTHS) + r")[a-z]* \d{1,2}, \d{4}", rest[0]) or "@" in rest[0]) and len(rest[0]) < 120:
        m = re.search(r"\b(" + "|".join(MONTHS) + r")[a-z]* (\d{1,2}), (\d{4})", rest[0])
        if m:
            date = datetime.date(int(m.group(3)), MONTHS.index(m.group(1)) + 1, int(m.group(2)))
        rest.pop(0)
    bl = blocks("\n".join(rest))
    if not bl or bl[0][0] != "p":
        sys.exit("reflection.py: a lead paragraph must follow the title")
    lead = bl.pop(0)[1]

    path = f"/reflections/{a.slug}/"
    out_file = next_file(a.slug)
    old = front(out_file) if out_file.exists() else {}
    if a.date:
        date = datetime.date.fromisoformat(a.date)
    elif old.get("date"):
        date = datetime.date.fromisoformat(old["date"])
    date = date or datetime.date.today()
    month = date.strftime("%B %Y")

    link = Linker(site_titles(path))
    body, small, cur_small = [], [], None
    for kind, c in bl:
        if kind == "h2" and c in SMALL:
            cur_small = [c, []]
            small.append(cur_small)
            continue
        if cur_small is not None:
            if kind == "h2":
                cur_small = None          # a section after the small type: back to the text
            else:
                items = c if isinstance(c, list) else [c]
                cur_small[1].extend(link(inline(x), small=True) for x in items)
                continue
        if kind in ("h2", "h3"):
            body.append(f"      <{kind}>{inline(c)}</{kind}>")
        elif kind == "p":
            body.append(f"      <p>{link(inline(c))}</p>")
        elif kind == "qn":
            body.append(f'      <p class="qn">{link(inline(c))}</p>')
        else:
            items = "".join(f"<li>{link(inline(x))}</li>" for x in c)
            body.append(f"      <{kind}>{items}</{kind}>")
    for label, paras in small:
        body.append("")
        body.append(f'      <p class="sources"><span class="sources-label">{label}</span> {" ".join(paras)}</p>')

    lead_html = link(inline(lead))
    lead_plain = re.sub(r"<[^>]+>", "", lead_html)
    core = re.sub(r"\s*Food for thought[^.]*;[^.]*\.\s*$|\s*Food for thought[^.]*\.\s*$", "", lead_plain).strip()
    description = a.description or (core + " A layman's reflection, with its liberties marked.")
    description = description.replace("\n", " ")
    blurb = a.blurb or core
    eyebrow = a.eyebrow[0].upper() + a.eyebrow[1:]

    page = f"""<!--
title: {title}
crumb: {title}
description: {description}
path: {path}
nav: essays
kind: essay
date: {date.isoformat()}
register: {a.register}
-->
<section class="page-head">
  <div class="wrap narrow">
    <p class="crumbs"><a href="/reflections/">Biblical reflections</a></p>
    <p class="eyebrow">Reflection · {html.escape(a.eyebrow, quote=False)}</p>
    <h1>{inline(title)}</h1>
    <p class="lead">{lead_html}</p>
    <p class="essay-meta">Richard Verver · {month}</p>
  </div>
</section>

<section class="section">
  <div class="wrap narrow">
    <div class="prose essay">
{chr(10).join(body)}
    </div>
  </div>
</section>
"""
    # what to look at
    text = re.sub(r"<[^>]+>", " ", page.split("-->", 1)[1])
    problems = [w for w in ("*", "\\", "<?claude", "](", " ") if w in text]
    words = len(text.split())
    print(f"reflection.py: {title!r} -> {out_file.relative_to(ROOT)} ({path}), {date.isoformat()}, {words} words")
    print(f"  sections: {sum(1 for k, _ in bl if k == 'h2' and _ not in SMALL)}; small type: {', '.join(l for l, _ in small) or 'none'}")
    for k, p, how in link.made:
        print(f"  linked ({how}): {html.unescape(k)} -> {p}")
    for k in sorted(set(link.missed)):
        print(f"  not linked (plain text; italicize it in the doc to link it): {html.unescape(k)}")
    if problems:
        print(f"  LOOK: {problems} in the text: markdown left over, or an escaped character meant to be there")
    if a.dry_run:
        return
    if a.out:
        Path(a.out).write_text(page, encoding="utf-8")
        print(f"  written to {a.out}; the index is left alone")
        return
    out_file.write_text(page, encoding="utf-8")

    # the index: at the top, unless it is there already
    idx = INDEX.read_text(encoding="utf-8")
    entry = f'''      <li>
        <p class="reg">{html.escape(eyebrow, quote=False)} · {month}</p>
        <h2><a href="{path}">{inline(title)}</a></h2>
        <p>{html.escape(blurb, quote=False)}</p>
        <p class="more"><a href="{path}">Read the reflection →</a></p>
      </li>
'''
    there = re.search(rf'      <li>\n(?:(?!      </li>).)*?<a href="{re.escape(path)}">.*?      </li>\n', idx, re.S)
    if there and a.blurb:
        idx = idx[:there.start()] + entry + idx[there.end():]
        print("  index: entry replaced")
    elif there:
        print("  index: entry already there, left alone (give --blurb to replace it)")
    else:
        anchor = '    <ul class="essay-list">\n'
        if idx.count(anchor) != 1:
            sys.exit("reflection.py: the index's list was not found; add the entry by hand")
        idx = idx.replace(anchor, anchor + entry)
        print("  index: entry added at the top")
    INDEX.write_text(idx, encoding="utf-8")
    print("  next: python3 build.py, then look at the page")


if __name__ == "__main__":
    main()
