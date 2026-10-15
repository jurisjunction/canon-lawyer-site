"""
Downloadable PDFs of the writing: essays, biblical reflections, colloquies and explainers.

build.py calls make(meta, body) for each writing page, then add_tools() to put the
download link under the byline. The PDF is typeset with WeasyPrint when it is
installed (pip install weasyprint). A PDF is rebuilt only when its text changes
(the hash is kept in _src/pdf-manifest.json), so unchanged PDFs never churn in git.

Without WeasyPrint the build still runs: a PDF that is still current keeps its
link; one that is out of date is not linked (the page offers the browser's print
to PDF instead) and the build lists it.
"""
import hashlib
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "docs"
MANIFEST = ROOT / "_src" / "pdf-manifest.json"
FONTS = OUT / "assets" / "fonts"          # the site's own (Latin) fonts
PDF_FONTS = ROOT / "_src" / "fonts"       # Greek subsets, for the PDFs only
TEMPLATE_VERSION = 3  # bump to rebuild every PDF after changing the template

SECTIONS = {"essays": "Essay", "reflections": "Biblical reflection", "colloquies": "Colloquy", "explainers": "Explainer"}
CC0_URL = "https://creativecommons.org/publicdomain/zero/1.0/"

try:
    import weasyprint  # noqa: F401
    AVAILABLE = True
except Exception:  # not installed, or its system libraries are missing
    AVAILABLE = False

_manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}
_stale, _built = [], []


def is_writing(meta):
    parts = meta["path"].strip("/").split("/")
    return len(parts) == 2 and parts[0] in SECTIONS and meta.get("kind") != "field"


def pdf_path(meta):
    slug = meta["path"].strip("/").split("/")[-1]
    return meta["path"] + slug + ".pdf", OUT / meta["path"].strip("/") / (slug + ".pdf")


# --- pulling the text out of a page ------------------------------------------

def _first(pattern, text):
    m = re.search(pattern, text, re.S)
    return m.group(1).strip() if m else ""


def _inner_div(text, open_pattern):
    """Inner HTML of the first div matching open_pattern, with nested divs balanced."""
    m = re.search(open_pattern, text)
    if not m:
        return None, None
    depth, start = 1, m.end()
    for t in re.finditer(r"<(/?)div\b[^>]*>", text[start:]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            return m, text[start:start + t.start()]
    raise SystemExit(f"pdfs: unbalanced <div> after {open_pattern!r}")


def _absolute(fragment, domain):
    return re.sub(r'href="/', f'href="{domain}/', fragment)


def _strip_tags(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


# --- the document -------------------------------------------------------------

def _font_faces():
    faces = [
        ("EB Garamond", 400, "normal", "eb-garamond-latin-400-normal"),
        ("EB Garamond", 400, "italic", "eb-garamond-latin-400-italic"),
        ("EB Garamond", 500, "normal", "eb-garamond-latin-500-normal"),
        ("EB Garamond", 500, "italic", "eb-garamond-latin-500-italic"),
        ("Inter", 400, "normal", "inter-latin-400-normal"),
        ("Inter", 500, "normal", "inter-latin-500-normal"),
        ("Inter", 600, "normal", "inter-latin-600-normal"),
    ]
    for sub, fam in (("greek", "EB Garamond Greek"), ("greek-ext", "EB Garamond Greek Ext")):
        for w in (400, 500):
            for s in ("normal", "italic"):
                faces.append((fam, w, s, f"eb-garamond-{sub}-{w}-{s}"))
    def src(f):
        path = FONTS / (f + ".woff2")
        return (path if path.exists() else PDF_FONTS / (f + ".woff2")).as_uri()
    return "\n".join(
        f'@font-face {{ font-family: "{fam}"; font-weight: {w}; font-style: {s}; src: url("{src(f)}") format("woff2"); }}'
        for fam, w, s, f in faces
    )


CSS = """
@page {
  size: letter; margin: 0.95in 1.05in 0.9in;
  @bottom-left { content: string(doctitle); font-family: Inter, sans-serif; font-size: 7.5pt; color: #5a6273; }
  @bottom-right { content: counter(page) " of " counter(pages); font-family: Inter, sans-serif; font-size: 7.5pt; color: #5a6273; }
}
@page :first { @bottom-left { content: "canon-lawyer.ca"; } }
html { font-family: "EB Garamond", "EB Garamond Greek", "EB Garamond Greek Ext", Georgia, serif; font-size: 11.5pt; line-height: 1.5; color: #1c2230; }
body { margin: 0; }
a { color: inherit; text-decoration: none; }
strong, b { font-weight: 500; }
.prose a, .colophon a { border-bottom: 0.4pt solid #c9bda7; }
.eyebrow { font-family: Inter, sans-serif; font-size: 7.5pt; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: #7a2231; margin: 0 0 14pt; }
h1 { font-size: 27pt; font-weight: 500; line-height: 1.1; margin: 0 0 10pt; string-set: doctitle content(); }
.lead { font-size: 13pt; font-style: italic; line-height: 1.45; color: #2b3346; margin: 0 0 12pt; }
.byline { font-family: Inter, sans-serif; font-size: 8.5pt; letter-spacing: 0.02em; color: #5a6273; margin: 0 0 24pt; padding-bottom: 14pt; border-bottom: 0.6pt solid #a8844c; }
.prose p { margin: 0 0 8pt; text-align: justify; hyphens: auto; hyphenate-character: "-"; orphans: 2; widows: 2; }
.prose h2 { font-size: 15.5pt; font-weight: 500; line-height: 1.2; margin: 20pt 0 7pt; break-after: avoid; }
.prose h3 { font-size: 12.5pt; font-weight: 500; margin: 14pt 0 5pt; break-after: avoid; }
.prose ul, .prose ol { margin: 0 0 10pt; padding-left: 1.2em; }
.prose li { margin: 0 0 4pt; }
.prose p.qn { padding-left: 1.6em; text-align: left; }
.prose .note { font-size: 10pt; line-height: 1.45; text-align: left; background: #efe9de; padding: 8pt 10pt; border-radius: 3pt; }
.prose .sources { font-size: 8.5pt; line-height: 1.45; text-align: left; color: #5a6273; border-top: 0.5pt solid #ddd4c4; padding-top: 8pt; margin-top: 18pt; }
.prose .sources-label { font-family: Inter, sans-serif; font-size: 6.5pt; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; margin-right: 4pt; }
.prose ul.claims li { font-size: 10pt; }
.prose .cite { font-family: Inter, sans-serif; font-size: 7pt; font-weight: 600; letter-spacing: 0.04em; color: #7a2231; white-space: nowrap; }
.prose .checklist { padding-left: 1.1em; }
.dialogue p.line { text-align: left; padding-left: 1.4em; text-indent: -1.4em; }
.dialogue .sp { font-variant: small-caps; font-weight: 500; letter-spacing: 0.04em; margin-right: 0.2em; }
.dialogue p.stage { font-style: italic; color: #5a6273; text-align: left; }
table.deadlines { width: 100%; border-collapse: collapse; font-size: 10pt; margin: 6pt 0 12pt; break-inside: avoid; }
table.deadlines th, table.deadlines td { text-align: left; vertical-align: top; padding: 5pt 6pt; border-bottom: 0.5pt solid #ddd4c4; }
table.deadlines th { font-family: Inter, sans-serif; font-size: 6.5pt; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: #5a6273; }
table.deadlines .days { font-weight: 600; color: #7a2231; white-space: nowrap; }
.key { break-inside: avoid; border: 0.5pt solid #ddd4c4; border-radius: 3pt; padding: 8pt 12pt 4pt; margin-top: 20pt; }
.key h3 { font-family: Inter, sans-serif; font-size: 7pt; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: #5a6273; margin: 0 0 6pt; }
.key ul { padding-left: 1.1em; margin: 0 0 6pt; }
.key li { font-size: 10pt; margin: 0 0 3pt; }
.colophon { break-inside: avoid; margin-top: 26pt; padding-top: 10pt; border-top: 0.6pt solid #a8844c; font-family: Inter, sans-serif; font-size: 7.8pt; line-height: 1.55; color: #5a6273; }
.colophon p { margin: 0 0 5pt; }
.colophon .label { font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; font-size: 6.5pt; color: #7a2231; margin-right: 4pt; }
"""


def license_html(meta):
    """The licence line: CC0 for the essays, all rights reserved for the rest."""
    if meta.get("license") == "cc0":
        what = "this essay"
        return (f'<span class="label">Public domain</span> To the extent possible under law, Richard Verver has waived '
                f'all copyright and related or neighbouring rights to {what} under '
                f'<a href="{CC0_URL}">CC0 1.0 Universal</a>. You may copy, change, translate, print and share it, '
                f'for any purpose, without asking. Quotations from other writers keep their own terms.')
    text = "© Richard Verver. All rights reserved."
    if meta["path"].startswith("/explainers/"):
        text += (" General information about canon law, not advice about your situation, and not advice on civil or "
                 "criminal law.")
    return text


def document(meta, body, domain):
    head = _first(r'<section class="page-head">(.*?)</section>', body)
    eyebrow = _first(r'<p class="eyebrow">(.*?)</p>', head)
    title = _first(r"<h1>(.*?)</h1>", head) or html.escape(meta["title"])
    lead = _first(r'<p class="lead">(.*?)</p>', head)
    byline = _first(r'<p class="essay-meta">(.*?)</p>', head) or "Richard Verver, JCL · Canon Lawyer"
    m, prose = _inner_div(body, r'<div class="(prose[^"]*)">')
    if prose is None:
        raise SystemExit(f"pdfs: no prose in {meta['path']}")
    prose_class = m.group(1)
    key = ""
    _, box = _inner_div(body, r'<div class="box">')
    if box and meta["path"].startswith("/explainers/"):
        key = f'<aside class="key">{box}</aside>'
    url = domain + meta["path"]
    shown_url = url.replace("https://www.", "")
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    doc = f"""<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<title>{html.escape(_strip_tags(title))}</title>
<meta name="author" content="Richard Verver">
<meta name="description" content="{html.escape(meta.get('description', ''))}">
<meta name="keywords" content="{html.escape(SECTIONS[meta['path'].strip('/').split('/')[0]])}{', ' + html.escape(meta['register']) if meta.get('register') else ''}">
{f'<meta name="dcterms.created" content="{meta["date"]}T12:00:00Z">' if meta.get('date') else ''}
<style>{_font_faces()}{CSS}</style>
</head>
<body>
<header>
<p class="eyebrow">{eyebrow}</p>
<h1>{title}</h1>
{lead_html}
<p class="byline">{byline}</p>
</header>
<main class="{prose_class}">
{prose}
</main>
{key}
<footer class="colophon">
<p>{license_html(meta)}</p>
<p>Read online at <a href="{url}">{shown_url}</a>.</p>
</footer>
</body>
</html>
"""
    return _absolute(doc, domain)


# --- building ------------------------------------------------------------------

def make(meta, body, domain):
    """Build (or keep) the PDF for a writing page. Returns {'url', 'pages'} if current, else None."""
    url, dest = pdf_path(meta)
    doc = document(meta, body, domain)
    digest = hashlib.sha256(f"{TEMPLATE_VERSION}\n{doc}".encode("utf-8")).hexdigest()
    entry = _manifest.get(meta["path"])
    if entry and entry.get("hash") == digest and dest.exists():
        return {"url": url, "pages": entry["pages"]}
    if not AVAILABLE:
        _stale.append(meta["path"])
        return None
    import weasyprint
    rendered = weasyprint.HTML(string=doc, base_url=OUT.as_uri() + "/").render()
    dest.parent.mkdir(parents=True, exist_ok=True)
    rendered.write_pdf(dest)
    pages = len(rendered.pages)
    _manifest[meta["path"]] = {"hash": digest, "pages": pages}
    _built.append(meta["path"])
    return {"url": url, "pages": pages}


def add_tools(body, pdf):
    """The download link (or, failing a current PDF, a print button) under the byline."""
    if pdf:
        n = pdf["pages"]
        tools = (f'<p class="essay-tools"><a class="pdf-link" href="{pdf["url"]}" download>Download PDF</a>'
                 f' <span class="pdf-size">{n} page{"s" if n != 1 else ""}</span></p>')
    else:
        tools = '<p class="essay-tools"><button type="button" class="pdf-link" data-print>Print or save as PDF</button></p>'
    for anchor in (r'(<p class="essay-meta">.*?</p>)', r'(<section class="page-head">.*?<p class="lead">.*?</p>)'):
        new, n = re.subn(anchor, lambda m: m.group(1) + "\n    " + tools, body, count=1, flags=re.S)
        if n:
            return new
    return body


def finish():
    if _built:
        MANIFEST.write_text(json.dumps(_manifest, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print(f"pdfs: typeset {len(_built)}")
    if _stale:
        print(f"pdfs: WeasyPrint is not installed, so {len(_stale)} PDF(s) are out of date and not linked "
              f"(those pages offer print to PDF instead). Run `pip install weasyprint` and build again:")
        for p in _stale:
            print("   ", p)
