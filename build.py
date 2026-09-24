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
    ("contact", "/contact/", "Contact"),
]

# Old Google Sites URLs -> new locations (kept so old links and search results still work)
REDIRECTS = {
    "/home/": "/",
    "/mission/": "/about/",
    "/areas-of-practice/": "/services/",
}

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
        </ul>
      </div>
    </div>
    <div class="disclaimer">
      <p>Richard Verver practises canon law, the law of the Catholic Church. Nothing on this site is advice on civil or criminal law; for those matters please consult a lawyer licensed in your jurisdiction. The information here is general and is not advice about your particular situation. Contacting me does not by itself create an advocate–client relationship; that begins only once we agree on it in writing.</p>
      <p>&copy; {year} Richard Verver. All rights reserved.</p>
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
    crumbs.append((meta.get("crumb", meta["title"]), meta["path"]))
    items = [{"@type": "ListItem", "position": i + 1, "name": n, "item": d + p} for i, (n, p) in enumerate(crumbs)]
    data = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}
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
    robots = '<meta name="robots" content="noindex">' if meta.get("noindex") else ""
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
    return meta, body

def redirect_page(target):
    url = CONFIG["domain"] + target
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Redirecting…</title>
<link rel="canonical" href="{url}">
<meta http-equiv="refresh" content="0; url={target}"></head>
<body><p>This page has moved: <a href="{target}">{url}</a></p></body></html>"""

def main():
    pages = []
    for p in sorted(SRC.glob("*.html")):
        meta, body = parse(p)
        dest = OUT / ("404.html" if meta["path"] == "/404" else meta["path"].strip("/") + "/index.html" if meta["path"] != "/" else "index.html")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(layout(meta, body), encoding="utf-8")
        if not meta.get("noindex"):
            pages.append((meta["path"], last_modified(p)))
        print("built", dest.relative_to(ROOT))
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
