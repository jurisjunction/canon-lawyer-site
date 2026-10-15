#!/usr/bin/env python3
"""
Builds the static site for canon-lawyer.ca.

  python3 build.py

Reads page bodies from _src/pages/*.html, wraps each in the shared layout
(header, footer, SEO tags) and writes the finished pages into docs/,
which is what GitHub Pages serves. Edit site-wide settings in CONFIG below.
No dependencies beyond Python 3.
"""
import datetime, html, json, pathlib, re, subprocess

import essay_map  # the map of disciplines the essays are filed on (essay_map.py)
import curriculum  # the homeschool year that walks the same map (curriculum.py)
import pdfs       # downloadable PDFs of the writing (pdfs.py; typesetting needs WeasyPrint)

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "_src" / "pages"
OUT = ROOT / "docs"

CONFIG = {
    "domain": "https://www.canon-lawyer.ca",
    "name": "Richard Verver, JCL",
    "tagline": "Canon Lawyer",
    # Where enquiries go. The contact form posts to FormSubmit, which emails this address.
    "email": "rverver@canon-lawyer.ca",
    # After FormSubmit activation you can replace this with the random alias they give you
    # (e.g. "a1b2c3d4e5...") to keep your address out of the page source.
    "form_endpoint": "https://formsubmit.co/rverver@canon-lawyer.ca",
    "x_handle": "jurisjunction",
}

NAV = [
    ("services", "/services/", "Services"),
    ("about", "/about/", "About"),
    ("faq", "/faq/", "FAQ"),
    ("explainers", "/explainers/", "Explainers"),
    ("essays", "/essays/", "Essays"),
    ("contact", "/contact/", "Contact"),
]

# Old Google Sites URLs -> new locations (kept so old links and search results still work)
REDIRECTS = {
    "/home/": "/",
    "/mission/": "/about/",
    "/areas-of-practice/": "/services/",
}

# Client testimonials. Add new ones to this list and rebuild.
#   quote: the client's words.  who: how they are credited (keep it anonymous).
#   area: the service page it also appears on (nullity, penal, recourse, institutions), or None.
# {{testimonials}} in a page shows all of them; {{testimonials:penal}} shows only that area's.
TESTIMONIALS = [
    {
        "quote": "I have been very grateful to have Richard Verver as my advocate. Very knowledgeable of the law, thorough in research and application, comprehensive and skilled in explanation. He makes himself available to my needs, listens carefully, incorporates my thoughts and suggestions appropriately. To these skills he adds a personable, friendly and informal approach, which has set me at ease and encouraged me along the way. The work on the case has felt like a genuine partnership, where I have been treated with respect. He loves the Church, but he also values its individual members in their difficulty and their need. I very highly recommend him.",
        "who": "Client in a canonical penal case",
        "area": "penal",
    },
]

def testimonials_html(area=None):
    items = [t for t in TESTIMONIALS if area is None or t.get("area") == area]
    figs = "".join(
        f'<figure class="testimonial"><blockquote><p>{html.escape(t["quote"])}</p></blockquote>'
        f'<figcaption>{html.escape(t["who"])}</figcaption></figure>'
        for t in items
    )
    if not figs:
        return ""
    if area:
        return figs
    return f"""<section class="section testimonials-band">
  <div class="wrap narrow">
    <div class="section-head">
      <p class="eyebrow">In clients’ words</p>
    </div>
    {figs}
  </div>
</section>"""

MARK = """<svg viewBox="0 0 34 42" aria-hidden="true" focusable="false"><path d="M1 41V17C1 8.2 8.2 1 17 1s16 7.2 16 16v24H1Z" fill="none" stroke="#a8844c" stroke-width="1.5"/><text x="17" y="31" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="17" fill="currentColor">RV</text></svg>"""

def header(active):
    links = []
    for key, href, label in NAV:
        cur = ' aria-current="page"' if key == active else ""
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    links.append('<a class="btn btn-primary" href="/contact/">Free consultation</a>')
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="/" aria-label="{CONFIG['name']}, home">{MARK}<span><span class="brand-name">Richard Verver, <span style="font-variant:small-caps;letter-spacing:.04em">jcl</span></span><span class="brand-tag">Canon Lawyer</span></span></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Menu"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
    <nav class="nav" id="site-nav" aria-label="Main">{''.join(links)}</nav>
  </div>
</header>"""

def footer():
    year = datetime.date.today().year
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="brand" href="/">{MARK}<span><span class="brand-name">Richard Verver, JCL</span><span class="brand-tag">Canon Lawyer</span></span></a>
        <p>Canonical advocacy and counsel for individuals, clergy, dioceses and religious institutes. Serving clients across Canada and the United States by phone and video.</p>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
          <li><a href="/services/marriage-nullity/">Marriage nullity</a></li>
          <li><a href="/services/penal-advocacy/">Penal advocacy</a></li>
          <li><a href="/services/administrative-recourse/">Administrative recourse</a></li>
          <li><a href="/services/dioceses-institutions/">Dioceses &amp; institutions</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="/contact/">Book a free consultation</a></li>
          <li><a href="#" data-email>Email</a></li>
          <li><a href="https://x.com/{CONFIG['x_handle']}" rel="me noopener">@{CONFIG['x_handle']}</a></li>
          <li><a href="/faq/">Frequently asked questions</a></li>
          <li><a href="/explainers/">Explainers</a></li>
          <li><a href="/essays/">Essays</a></li>
          <li><a href="/reflections/">Biblical reflections</a></li>
          <li><a href="/colloquies/">Colloquies</a></li>
          <li><a href="/curriculum/">Homeschool curriculum</a></li>
          <li><a href="/privacy/">Privacy policy</a></li>
        </ul>
      </div>
    </div>
    <div class="disclaimer">
      <p>Richard Verver practises canon law, the law of the Catholic Church. Nothing on this site is advice on civil or criminal law; for those matters please consult a lawyer licensed in your jurisdiction. The information here is general and is not advice about your particular situation. Contacting me through this site does not create an advocate–client relationship or any duty of confidentiality, and it does not prevent me from representing anyone else. Please do not send confidential details until I have confirmed that I can speak with you about your matter. Once I accept a consultation, what you share is kept strictly confidential and will not be used against you.</p>
      <p>&copy; {year} Richard Verver. All rights reserved, except the <a href="/essays/">essays</a>, which are dedicated to the public domain under <a href="https://creativecommons.org/publicdomain/zero/1.0/">CC0</a>.</p>
    </div>
  </div>
</footer>"""

def person_jsonld():
    d = CONFIG["domain"]
    person = {
        "@type": "Person",
        "@id": d + "/#richard",
        "name": "Richard Verver",
        "honorificSuffix": "JCL",
        "jobTitle": "Canon Lawyer",
        "url": d + "/about/",
        "image": d + "/assets/img/richard-verver-800.jpg",
        "worksFor": {"@id": d + "/#practice"},
        "alumniOf": [{"@type": "CollegeOrUniversity", "name": "Saint Paul University"}, {"@type": "CollegeOrUniversity", "name": "University of Toronto"}],
        "memberOf": [{"@type": "Organization", "name": "Canadian Canon Law Society"}, {"@type": "Organization", "name": "Canon Law Society of America"}],
        "knowsAbout": ["Canon law", "Declaration of nullity", "Catholic annulment", "Canonical penal law", "Hierarchical recourse"],
        "sameAs": [f"https://x.com/{CONFIG['x_handle']}"],
    }
    website = {
        "@type": "WebSite",
        "@id": d + "/#website",
        "url": d + "/",
        "name": "Richard Verver, JCL",
        "alternateName": "canon-lawyer.ca",
        "inLanguage": "en-CA",
        "publisher": {"@id": d + "/#practice"},
    }
    data = {
        "@type": "LegalService",
        "@id": d + "/#practice",
        "name": "Richard Verver, JCL, Canon Lawyer",
        "url": d + "/",
        "email": CONFIG["email"],
        "logo": d + "/assets/img/apple-touch-icon.png",
        "image": CONFIG["domain"] + "/assets/img/richard-verver-800.jpg",
        "description": "Canon law advocacy and counsel: marriage nullity cases, penal cases, administrative (hierarchical) recourse, and consulting for dioceses and religious institutes.",
        "areaServed": [{"@type": "Country", "name": "Canada"}, {"@type": "Country", "name": "United States"}],
        "address": {"@type": "PostalAddress", "addressLocality": "Toronto", "addressRegion": "ON", "addressCountry": "CA"},
        "founder": {"@id": d + "/#richard"},
        "employee": {"@id": d + "/#richard"},
        "sameAs": [f"https://x.com/{CONFIG['x_handle']}"],
    }
    graph = {"@context": "https://schema.org", "@graph": [data, person, website]}
    return '<script type="application/ld+json">' + json.dumps(graph, ensure_ascii=False) + "</script>"

def breadcrumb_jsonld(meta):
    """Home > (Services >) this page, so Google can show a breadcrumb trail instead of a bare URL."""
    d = CONFIG["domain"]
    crumbs = [("Home", "/")]
    if meta["path"].startswith("/services/") and meta["path"] != "/services/":
        crumbs.append(("Services", "/services/"))
    if meta["path"].startswith("/essays/") and meta["path"] != "/essays/":
        crumbs.append(("Essays", "/essays/"))
        if meta.get("field"):
            f = essay_map.BY_SLUG[meta["field"]]
            crumbs.append((f["name"], f"/essays/{f['slug']}/"))
    if meta["path"].startswith("/explainers/") and meta["path"] != "/explainers/":
        crumbs.append(("Explainers", "/explainers/"))
    if meta["path"].startswith("/reflections/") and meta["path"] != "/reflections/":
        crumbs.append(("Reflections", "/reflections/"))
    if meta["path"].startswith("/colloquies/") and meta["path"] != "/colloquies/":
        crumbs.append(("Colloquies", "/colloquies/"))
    crumbs.append((meta.get("crumb", meta["title"]), meta["path"]))
    items = [{"@type": "ListItem", "position": i + 1, "name": n, "item": d + p} for i, (n, p) in enumerate(crumbs)]
    data = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"

def article_jsonld(meta):
    """Essay pages: an Article by Richard, so search engines show author and date."""
    d = CONFIG["domain"]
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": meta["title"],
        "description": meta["description"],
        "url": d + meta["path"],
        "mainEntityOfPage": d + meta["path"],
        "inLanguage": "en-CA",
        "datePublished": meta["date"],
        "dateModified": meta.get("modified", meta["date"]),
        "author": {"@type": "Person", "@id": d + "/#richard", "name": "Richard Verver", "url": d + "/about/"},
        "publisher": {"@id": d + "/#practice"},
    }
    if meta.get("license") == "cc0":
        data["license"] = CC0_URL
    if meta.get("pdf_url"):
        data["encoding"] = {"@type": "MediaObject", "encodingFormat": "application/pdf", "contentUrl": d + meta["pdf_url"]}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"

def last_modified(path):
    """Date of the last git commit touching this page's source (falls back to today)."""
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", str(path)], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        return out or datetime.date.today().isoformat()
    except OSError:
        return datetime.date.today().isoformat()

def layout(meta, body):
    title = meta["title"]
    full_title = title if meta.get("path") == "/" else f"{title} | Richard Verver, JCL"
    desc = meta["description"]
    url = CONFIG["domain"] + meta["path"]
    if meta["path"] == "/":
        extra = person_jsonld()
    elif meta.get("noindex"):
        extra = ""
    else:
        extra = breadcrumb_jsonld(meta)
    if meta.get("jsonld"):
        extra += meta["jsonld"]
    if meta.get("kind") == "essay":
        extra += article_jsonld(meta)
    robots = '<meta name="robots" content="noindex">' if meta.get("noindex") else ""
    if meta.get("license") == "cc0":
        robots += f'\n<link rel="license" href="{CC0_URL}">'
    if meta.get("pdf_url"):
        robots += f'\n<link rel="alternate" type="application/pdf" href="{meta["pdf_url"]}" title="{html.escape(title)} (PDF)">'
    return f"""<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
{robots}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Richard Verver, JCL">
<meta property="og:locale" content="en_CA">
<meta property="og:title" content="{html.escape(full_title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{CONFIG['domain']}/assets/img/og-card.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Richard Verver, JCL, Canon Lawyer: marriage nullity, penal advocacy and recourse against Church decrees">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@{CONFIG['x_handle']}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/eb-garamond-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css">
<meta name="theme-color" content="#f8f5ef">
{extra}
</head>
<body>
{header(meta.get('nav'))}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/js/site.js" defer></script>
</body>
</html>
"""

def parse(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"\s*<!--(.*?)-->\s*", text, re.S)
    meta = {}
    for line in m.group(1).strip().splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    body = text[m.end():]
    for k, v in CONFIG.items():
        body = body.replace("{{" + k + "}}", v)
    body = re.sub(r"\{\{testimonials(?::(\w+))?\}\}", lambda m: testimonials_html(m.group(1)), body)
    return meta, body

def redirect_page(target):
    url = CONFIG["domain"] + target
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Redirecting…</title>
<link rel="canonical" href="{url}">
<meta http-equiv="refresh" content="0; url={target}"></head>
<body><p>This page has moved: <a href="{target}">{url}</a></p></body></html>"""

ESSAY_CRUMBS = '<p class="crumbs"><a href="/essays/">Essays</a></p>'

CC0_URL = "https://creativecommons.org/publicdomain/zero/1.0/"
LICENSE_BAND = f"""
<section class="section license-band">
  <div class="wrap narrow">
    <p class="license-note"><span class="license-label">Public domain</span> I have dedicated this essay to the public domain under <a href="{CC0_URL}" rel="license">CC0 1.0</a>. Copy it, change it, translate it, print it and share it, for any purpose, without asking. Quotations from other writers keep their own terms.</p>
  </div>
</section>
"""

def write_page(meta, body):
    dest = OUT / ("404.html" if meta["path"] == "/404" else meta["path"].strip("/") + "/index.html" if meta["path"] != "/" else "index.html")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(layout(meta, body), encoding="utf-8")
    print("built", dest.relative_to(ROOT))

def main():
    pages = []
    sources = []
    for p in sorted(SRC.glob("*.html")):
        meta, body = parse(p)
        meta["modified"] = last_modified(p)
        sources.append((p, meta, body))

    # The essays map: every essay is filed on a field (essay_map.py).
    essays = [m for _, m, _ in sources if m.get("kind") == "essay" and m["path"].startswith("/essays/")]
    essay_map.check_graph()
    essay_map.check_filing(essays)
    newest_essay = max((m["modified"] for m in essays), default=datetime.date.today().isoformat())

    # The homeschool year walks the same map, one unit per field (curriculum.py).
    units = curriculum.units_of(m for _, m, _ in sources)
    curriculum.check_units(units)

    for p, meta, body in sources:
        if "{{essay_map}}" in body:
            body = body.replace("{{essay_map}}", essay_map.map_section(essays))
        if "{{curriculum_units}}" in body:
            body = body.replace("{{curriculum_units}}", curriculum.units_section(units, essays))
        if meta.get("kind") == "unit":
            body = curriculum.fill_unit(meta, body)
        # Every essay is dedicated to the public domain (CC0), unless its comment block says otherwise.
        if meta.get("kind") == "essay" and meta["path"].startswith("/essays/"):
            meta.setdefault("license", "cc0")
        # A downloadable PDF of every piece of writing (pdfs.py), made from the page as written.
        if pdfs.is_writing(meta):
            pdf = pdfs.make(meta, body, CONFIG["domain"])
            meta["pdf_url"] = pdf["url"] if pdf else None
            body = pdfs.add_tools(body, pdf)
        if meta.get("kind") == "essay" and meta.get("field"):
            body = body.replace(ESSAY_CRUMBS, essay_map.essay_crumbs(meta), 1)
        if meta.get("license") == "cc0":
            body += LICENSE_BAND
        if meta.get("kind") == "essay" and meta.get("field"):
            body += essay_map.essay_nav(meta)
        if meta.get("kind") == "unit":
            body += curriculum.unit_nav(meta, units)
        write_page(meta, body)
        if not meta.get("noindex"):
            pages.append((meta["path"], meta["modified"]))
    pdfs.finish()

    for f in essay_map.FIELDS:
        meta, body = essay_map.field_page(f["slug"], essays, curriculum.field_line(f["slug"], units))
        filed = [e["modified"] for e in essays if e.get("field") == f["slug"] or f["slug"] in essay_map._also(e)]
        meta["modified"] = max(filed, default=newest_essay)
        write_page(meta, body)
        pages.append((meta["path"], meta["modified"]))
    for old, new in REDIRECTS.items():
        d = OUT / old.strip("/") / "index.html"
        d.parent.mkdir(parents=True, exist_ok=True)
        d.write_text(redirect_page(new), encoding="utf-8")
    urls = "".join(f"<url><loc>{CONFIG['domain']}{p}</loc><lastmod>{mod}</lastmod></url>" for p, mod in pages)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {CONFIG['domain']}/sitemap.xml\n")
    (OUT / "CNAME").write_text("www.canon-lawyer.ca\n")
    (OUT / ".nojekyll").write_text("")

if __name__ == "__main__":
    main()
