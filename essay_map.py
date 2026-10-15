"""
The essays map.

The disciplines are sorted by the kind of answer each gives (read, computed,
found, made, dated, taught, enacted, supplied ...) and ordered as a directed
acyclic graph: each field lists the fields it draws on. Essays are filed on the
map by `field:` (and optionally `also:`) in their comment block.

To add a field: add a dict to FIELDS (its `draws_on` may only name fields that
do not, directly or indirectly, draw on it; build.py refuses a cycle).
To file an essay: give it `field: <slug>` and, if it touches others,
`also: <slug>, <slug>`.
"""
import html

FIELDS = [
    {
        "slug": "reading", "name": "Reading", "discipline": "Grammar and interpretation", "kind": "Read",
        "gloss": "Every text is entered with its readings, and each reading is followed to its end. Interpretation weighs a reading; it never fixes one.",
        "draws_on": [],
    },
    {
        "slug": "number", "name": "Number", "discipline": "Logic and mathematics", "kind": "Computed",
        "gloss": "What follows from what, and how much. Order comes first, and measure is laid on it, as a date is laid on an event.",
        "draws_on": [],
    },
    {
        "slug": "nature", "name": "Nature", "discipline": "The empirical sciences", "kind": "Found",
        "gloss": "A finding fixes a fact from its year until a later finding replaces it. Method by division tells us about the parts; it never says what a thing is.",
        "draws_on": ["number"],
    },
    {
        "slug": "making", "name": "Making", "discipline": "The arts, photography among them", "kind": "Made",
        "gloss": "The sculptor acts on the bronze, and the statue is the bronze given a form, not a new thing. The camera is the same: light acts on the sensor, and the maker gives the picture its form.",
        "draws_on": ["nature", "number"],
    },
    {
        "slug": "memory", "name": "Memory", "discipline": "History", "kind": "Dated",
        "gloss": "Events stand in an order, and dates are measures laid on it. A claim about who wrote what is checked against that order.",
        "draws_on": ["reading", "number"],
    },
    {
        "slug": "person", "name": "The Person", "discipline": "Philosophy of human nature", "kind": "Understood",
        "gloss": "Stone, oak, lion, man, angel: what merely is, what lives, what senses, what understands in a body, what understands without one. One soul is the form of one body, and the will follows the intellect.",
        "draws_on": ["nature"],
    },
    {
        "slug": "being", "name": "Being", "discipline": "Metaphysics", "kind": "Said by analogy",
        "gloss": "The true, the good and the one are said first of God, and of creatures by participation. We come to know God from his effects, so the road runs from things to him.",
        "draws_on": ["person", "number"],
    },
    {
        "slug": "god", "name": "God", "discipline": "Theology", "kind": "Taught",
        "gloss": "Sources are weighed by their rank, form and date. Nothing crosses the line between Creator and creature unannounced.",
        "draws_on": ["being", "memory", "reading"],
    },
    {
        "slug": "act", "name": "The Act", "discipline": "Ethics", "kind": "Judged",
        "gloss": "What a kind of act is, morally, is taught; the verdict is said of an act, never of a person. What a person knew and willed is claimed, never computed.",
        "draws_on": ["person", "being", "god"],
    },
    {
        "slug": "city", "name": "The City", "discipline": "Prudence and politics", "kind": "Supplied",
        "gloss": "The judgment of those responsible for the common good. It is supplied by them, never computed, and the principles it applies come from the act.",
        "draws_on": ["act", "memory"],
    },
    {
        "slug": "law", "name": "Law", "discipline": "Canon and civil law", "kind": "Enacted",
        "gloss": "Law answers questions of governance and never a question of doctrine. It is ordered to teaching: where it presupposes a teaching, the teaching must hold.",
        "draws_on": ["city", "act", "god", "memory", "reading"],
    },
    {
        "slug": "worship", "name": "Worship", "discipline": "Liturgy and the sacraments", "kind": "Witnessed",
        "gloss": "The prayer of the Church witnesses and fixes nothing. The rite is matter and form, word, law and time, and the whole person is in it.",
        "draws_on": ["god", "law", "making"],
    },
]

# Disciplines left off the map, and why.
NOT_ON_MAP = [
    ("Economics", "Taken whole, it lays market findings on moral questions and says what a man is from a model reached by division. Taken apart, its findings belong to Nature, justice in exchange to The Act, and policy to The City."),
    ("Psychology", "The same two faults: guilt treated as nothing but a symptom, and a moral question rested on a finding. Its findings belong to Nature, the soul to The Person, and guilt to The Act."),
    ("Folded in", "Some disciplines have no kind of answer of their own and live inside others: computer science in Number and Making; medicine in Nature and Making, ordered by The Act; music and photography in Making, with Number and Nature; rhetoric in Making and Reading, since the speech is a thing made and the persuasion of another’s mind is never computed."),
]

# Where each field sits in the drawing: a column for the word (left), the spine of
# the person (centre), and number, nature and making (right).
COLUMN = {"reading": 0, "memory": 0, "number": 2, "nature": 2, "making": 2}

BY_SLUG = {f["slug"]: f for f in FIELDS}
esc = html.escape


def check_graph():
    """Refuse unknown fields and cycles; return the fields in topological order."""
    for f in FIELDS:
        for d in f["draws_on"]:
            if d not in BY_SLUG:
                raise SystemExit(f"essay_map: {f['slug']} draws on unknown field {d!r}")
    order, state = [], {}

    def visit(s, trail):
        if state.get(s) == 1:
            raise SystemExit("essay_map: cycle " + " -> ".join(trail + [s]))
        if state.get(s) == 2:
            return
        state[s] = 1
        for d in BY_SLUG[s]["draws_on"]:
            visit(d, trail + [s])
        state[s] = 2
        order.append(s)

    for f in FIELDS:
        visit(f["slug"], [])
    return order


def leads_to(slug):
    return [f["slug"] for f in FIELDS if slug in f["draws_on"]]


def ancestors(slug):
    seen, stack = set(), list(BY_SLUG[slug]["draws_on"])
    while stack:
        s = stack.pop()
        if s not in seen:
            seen.add(s)
            stack.extend(BY_SLUG[s]["draws_on"])
    return seen


def reduced_edges():
    """The edges with every one implied by a longer path removed (for the drawing only)."""
    edges = []
    for f in FIELDS:
        for d in f["draws_on"]:
            implied = any(d in ancestors(o) for o in f["draws_on"] if o != d)
            if not implied:
                edges.append((d, f["slug"]))
    return edges


def layers():
    lay = {}
    for s in check_graph():
        ds = BY_SLUG[s]["draws_on"]
        lay[s] = 0 if not ds else 1 + max(lay[d] for d in ds)
    return lay


def link(slug):
    f = BY_SLUG[slug]
    return f'<a href="/essays/{f["slug"]}/">{esc(f["name"])}</a>'


def link_list(slugs):
    return ", ".join(link(s) for s in slugs) if slugs else "nothing on the map yet"


def map_svg(counts):
    """The graph as an inline SVG: nodes link to their pages; empty fields drawn dashed."""
    W, ROW, BW, BH, TOP = 560, 76, 168, 48, 16
    xs = {0: 98, 1: 280, 2: 462}
    lay = layers()
    pos = {}
    for f in FIELDS:
        s = f["slug"]
        pos[s] = (xs[COLUMN.get(s, 1)], TOP + lay[s] * ROW)
    H = TOP + (max(lay.values()) + 1) * ROW
    parts = [f'<svg class="map-svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="map-title">',
             '<title id="map-title">A map of the disciplines: what each draws on, from reading and number to worship</title>',
             '<defs><marker id="map-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
             '<path d="M1 1L9 5L1 9" fill="none" stroke="#a8844c" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>']
    for a, b in reduced_edges():
        (xa, ya), (xb, yb) = pos[a], pos[b]
        y1, y2 = ya + BH, yb
        if abs(xa - xb) < 1:                       # straight down a column
            d = f"M{xa},{y1} L{xb},{y2 - 2}"
        elif lay[b] - lay[a] > 1:                  # a long edge: down its own column, then in from the side
            side = xb - BW / 2 - 2 if xa < xb else xb + BW / 2 + 2
            ym = yb + BH / 2
            d = f"M{xa},{y1} C{xa},{ym} {xa},{ym} {side},{ym}"
        else:                                      # one row down, across
            dy = (y2 - y1) / 2
            d = f"M{xa},{y1} C{xa},{y1 + dy} {xb},{y2 - dy} {xb},{y2 - 2}"
        parts.append(f'<path class="edge" d="{d}" fill="none" stroke="#a8844c" stroke-width="1.3" marker-end="url(#map-arrow)"/>')
    for f in FIELDS:
        s = f["slug"]
        x, y = pos[s]
        gap = " gap" if not counts.get(s) else ""
        n = counts.get(s, 0)
        label = f'{n} essay{"s" if n != 1 else ""}' if n else "a gap"
        rect_attrs = ('fill="none" stroke="#c9bda7" stroke-width="1.2" stroke-dasharray="5 4"' if gap
                      else 'fill="#fffdf9" stroke="#ddd4c4" stroke-width="1.2"')
        name_fill = "#5a6273" if gap else "#1c2230"
        parts.append(
            f'<a class="node{gap}" href="/essays/{s}/" aria-label="{esc(f["name"])}: {esc(f["discipline"])}, {label}">'
            f'<rect x="{x - BW / 2}" y="{y}" width="{BW}" height="{BH}" rx="9" {rect_attrs}/>'
            f'<text class="n-name" x="{x}" y="{y + 21}" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="19" fill="{name_fill}">{esc(f["name"])}</text>'
            f'<text class="n-kind" x="{x}" y="{y + 37}" text-anchor="middle" font-family="Inter, system-ui, sans-serif" font-size="10.5" letter-spacing=".07em" fill="#5a6273">{esc((f["kind"] + " · " + label).upper())}</text></a>')
    parts.append("</svg>")
    return "".join(parts)


# ---------------------------------------------------------------------------
# Pages. `essays` is a list of the essay pages' meta dicts (title, path,
# register, date, summary, field, also).

def _also(meta):
    return [s.strip() for s in meta.get("also", "").split(",") if s.strip()]


def check_filing(essays):
    for e in essays:
        for s in [e.get("field", "")] + _also(e):
            if s not in BY_SLUG:
                raise SystemExit(f"essay_map: {e['path']} is filed under unknown field {s!r}")


def filed(essays, slug):
    """Essays filed under this field, newest first, and those that also touch it."""
    key = lambda e: e.get("date", "")
    main = sorted((e for e in essays if e.get("field") == slug), key=key, reverse=True)
    also = sorted((e for e in essays if slug in _also(e)), key=key, reverse=True)
    return main, also


def _month(meta):
    import datetime
    try:
        return datetime.date.fromisoformat(meta["date"]).strftime("%B %Y")
    except (KeyError, ValueError):
        return ""


def _essay_card(e):
    reg = f'In the register of {esc(e["register"])} · {_month(e)}' if e.get("register") else _month(e)
    return f"""      <li>
        <p class="reg">{reg}</p>
        <h2><a href="{e['path']}">{esc(e['title'])}</a></h2>
        <p>{e.get('summary', '')}</p>
        <p class="more"><a href="{e['path']}">Read the essay →</a></p>
      </li>"""


def map_section(essays):
    """The essays index: the drawing, then every field in order with what is filed there."""
    check_filing(essays)
    counts = {f["slug"]: len(filed(essays, f["slug"])[0]) for f in FIELDS}
    rows = []
    for slug in check_graph():
        f = BY_SLUG[slug]
        main, also = filed(essays, slug)
        if main:
            items = "".join(f'<li><a href="{e["path"]}">{esc(e["title"])}</a> <span class="reg-inline">{esc(e.get("register", ""))}</span></li>' for e in main)
            body = f'<ul class="field-essays">{items}</ul>'
        else:
            body = '<p class="field-gap">Nothing here yet.</p>'
        if also:
            body += '<p class="field-also">Also touching it: ' + ", ".join(f'<a href="{e["path"]}">{esc(e["title"])}</a>' for e in also) + "</p>"
        draws = f'<p class="field-edges">Draws on {link_list(f["draws_on"])}.</p>' if f["draws_on"] else '<p class="field-edges">Draws on nothing before it.</p>'
        rows.append(f"""      <li class="field" id="{slug}">
        <p class="reg">{esc(f['discipline'])} · {esc(f['kind'])}</p>
        <h2><a href="/essays/{slug}/">{esc(f['name'])}</a></h2>
        <p>{esc(f['gloss'])}</p>
        {draws}
        {body}
      </li>""")
    off = "".join(f"<li><strong>{esc(n)}.</strong> {esc(t)}</li>" for n, t in NOT_ON_MAP)
    return f"""<section class="section map-band">
  <div class="wrap narrow">
    <figure class="map-figure">
      {map_svg(counts)}
      <figcaption>Each discipline is placed after what it draws on. Click one to see what is filed there; the dashed ones are gaps, still to be written into.</figcaption>
    </figure>
    <ul class="essay-list field-list">
{chr(10).join(rows)}
    </ul>
    <h2 class="off-map-head">Not on the map</h2>
    <ul class="off-map">{off}</ul>
  </div>
</section>"""


def field_page(slug, essays):
    """The body and meta for /essays/<slug>/."""
    f = BY_SLUG[slug]
    main, also = filed(essays, slug)
    nexts = leads_to(slug)
    if main:
        cards = '<ul class="essay-list">\n' + "\n".join(_essay_card(e) for e in main) + "\n    </ul>"
    else:
        cards = '<p class="note">Nothing is filed here yet. This is one of the gaps; it will be written into when we get there.</p>'
    also_html = ""
    if also:
        also_html = ('<h2 class="off-map-head">Also touching ' + esc(f["name"]) + '</h2>\n    <ul class="field-essays">'
                     + "".join(f'<li><a href="{e["path"]}">{esc(e["title"])}</a> <span class="reg-inline">filed under {link(e["field"])}</span></li>' for e in also)
                     + "</ul>")
    body = f"""<section class="page-head">
  <div class="wrap narrow">
    <p class="crumbs"><a href="/essays/">Essays</a></p>
    <p class="eyebrow">{esc(f['discipline'])}</p>
    <h1>{esc(f['name'])}</h1>
    <p class="lead">{esc(f['gloss'])}</p>
    <p class="essay-meta">The kind of answer it gives: {esc(f['kind'].lower())}</p>
  </div>
</section>

<section class="section">
  <div class="wrap narrow">
    <nav class="map-nav" aria-label="Neighbours on the map">
      <p><span class="map-nav-label">Draws on</span> {link_list(f['draws_on'])}</p>
      <p><span class="map-nav-label">Leads to</span> {link_list(nexts)}</p>
    </nav>
    {cards}
    {also_html}
    <p class="more" style="margin-top:40px"><a href="/essays/">The whole map →</a></p>
  </div>
</section>
"""
    meta = {
        "title": f"{f['name']}: {f['discipline']}",
        "crumb": f["name"],
        "description": f"{f['name']} ({f['discipline']}) on the map of essays by Richard Verver. {f['gloss']}",
        "path": f"/essays/{slug}/",
        "nav": "essays",
        "kind": "field",
    }
    return meta, body


def essay_crumbs(meta):
    """The visible breadcrumb on an essay page, with its field."""
    return f'<p class="crumbs"><a href="/essays/">Essays</a> › {link(meta["field"])}</p>'


def essay_nav(meta):
    """The band at the foot of an essay: where it is filed and where the map goes from there."""
    f = BY_SLUG[meta["field"]]
    also = _also(meta)
    also_html = f' · also {link_list(also)}' if also else ""
    return f"""
<section class="section map-nav-band">
  <div class="wrap narrow">
    <nav class="map-nav" aria-label="On the map">
      <p class="eyebrow">On the map</p>
      <p><span class="map-nav-label">Filed under</span> {link(f['slug'])}{also_html}</p>
      <p><span class="map-nav-label">Draws on</span> {link_list(f['draws_on'])}</p>
      <p><span class="map-nav-label">Leads to</span> {link_list(leads_to(f['slug']))}</p>
      <p class="more"><a href="/essays/">The whole map →</a></p>
    </nav>
  </div>
</section>
"""
