"""
The Benedict Year: a homeschool curriculum that walks the essays map in order.

Each unit is a page in _src/pages with, in its comment block:

    kind: unit
    unit: <1..12>
    term: <1..3>
    weeks: <first>–<last>
    field: <a field slug from essay_map.py>
    essays: <essay slugs used in the unit, comma-separated; empty for a gap>
    summary: <one line for the list on the index>

The build checks that the units cover the map's fields once each, numbered 1 to n,
and that no unit comes before a field it draws on (the map's own arrows). It then
fills {{curriculum_units}} on the index with the map and the unit list, puts
{{field_name}} and {{field_gloss}} into each unit page from essay_map.py, adds the
band at the foot of each unit page, and gives each field's page a line pointing
to its unit.
"""
import html

import essay_map

esc = html.escape
INDEX = "/curriculum/"

TERMS = {
    "1": "The word and the world",
    "2": "The person and God",
    "3": "The act and the common life",
}


def units_of(metas):
    return sorted((m for m in metas if m.get("kind") == "unit"), key=lambda m: int(m["unit"]))


def check_units(units):
    """Refuse a year that misses a field, repeats one, or takes one before what it draws on."""
    slugs = [u.get("field", "") for u in units]
    for u, s in zip(units, slugs):
        if s not in essay_map.BY_SLUG:
            raise SystemExit(f"curriculum: {u['path']} is a unit of unknown field {s!r}")
    if sorted(slugs) != sorted(f["slug"] for f in essay_map.FIELDS):
        raise SystemExit("curriculum: the units must cover every field on the map exactly once")
    if [int(u["unit"]) for u in units] != list(range(1, len(units) + 1)):
        raise SystemExit("curriculum: units must be numbered 1, 2, 3 ... without a gap")
    done = set()
    for u in units:
        for d in essay_map.BY_SLUG[u["field"]]["draws_on"]:
            if d not in done:
                raise SystemExit(f"curriculum: unit {u['unit']} ({u['field']}) comes before {d}, which it draws on")
        done.add(u["field"])


def _essays_used(u, essays):
    by_slug = {e["path"].strip("/").split("/")[-1]: e for e in essays}
    out = []
    for s in (x.strip() for x in u.get("essays", "").split(",")):
        if not s:
            continue
        if s not in by_slug:
            raise SystemExit(f"curriculum: {u['path']} uses unknown essay {s!r}")
        out.append(by_slug[s])
    return out


def fill_unit(meta, body):
    """Put the field's name and gloss into a unit page, so the rule is quoted from one place."""
    f = essay_map.BY_SLUG[meta["field"]]
    return body.replace("{{field_name}}", esc(f["name"])).replace("{{field_gloss}}", esc(f["gloss"]))


def units_section(units, essays):
    """The curriculum index: the map with each unit's number, then the units term by term."""
    by_field = {u["field"]: u for u in units}
    svg = essay_map.map_svg(
        {s: 1 for s in by_field},
        href=lambda s: f"{INDEX}{s}/",
        label=lambda s: f"Unit {by_field[s]['unit']} · weeks {by_field[s]['weeks']}",
        title="The Benedict Year on the map of the disciplines: twelve units in the map's order",
    )
    terms = []
    for t, name in TERMS.items():
        mine = [u for u in units if u.get("term") == t]
        if not mine:
            continue
        first, last = mine[0]["weeks"].split("–")[0], mine[-1]["weeks"].split("–")[-1]
        cards = []
        for u in mine:
            f = essay_map.BY_SLUG[u["field"]]
            used = _essays_used(u, essays)
            if used:
                reading = "Essay: " + ", ".join(f'<a href="{e["path"]}">{esc(e["title"])}</a>' for e in used)
            else:
                reading = "A gap on the map: the child writes into it"
            cards.append(f"""      <li>
        <p class="reg">Unit {u['unit']} · weeks {u['weeks']} · {esc(f['kind'])}</p>
        <h2><a href="{u['path']}">{esc(f['name'])}</a></h2>
        <p>{u.get('summary', '')}</p>
        <p class="field-also">{reading}</p>
        <p class="more"><a href="{u['path']}">Open the unit →</a></p>
      </li>""")
        terms.append(f"""    <h2 class="off-map-head">Term {t} · {esc(name)} <span class="reg-inline">weeks {first}–{last}</span></h2>
    <ul class="essay-list">
{chr(10).join(cards)}
    </ul>""")
    return f"""<section class="section map-band">
  <div class="wrap narrow">
    <figure class="map-figure">
      {svg}
      <figcaption>The units follow the arrows: nothing is taken before what it draws on. Click a unit to open it.</figcaption>
    </figure>
{chr(10).join(terms)}
  </div>
</section>"""


def unit_nav(meta, units):
    """The band at the foot of a unit: its field on the map, and the units either side."""
    i = [u["path"] for u in units].index(meta["path"])
    prev_u = units[i - 1] if i > 0 else None
    next_u = units[i + 1] if i + 1 < len(units) else None
    def ref(u):
        return f'<a href="{u["path"]}">Unit {u["unit"]} · {esc(essay_map.BY_SLUG[u["field"]]["name"])}</a>'
    prev_html = f'<p><span class="map-nav-label">Before it</span> {ref(prev_u)}</p>' if prev_u else ""
    next_html = f'<p><span class="map-nav-label">After it</span> {ref(next_u)}</p>' if next_u else ""
    return f"""
<section class="section map-nav-band">
  <div class="wrap narrow">
    <nav class="map-nav" aria-label="In the year">
      <p class="eyebrow">In the year</p>
      <p><span class="map-nav-label">On the map</span> {essay_map.link(meta['field'])}</p>
      {prev_html}
      {next_html}
      <p class="more"><a href="{INDEX}">The whole year →</a> · <a href="{INDEX}for-parents/">For parents →</a></p>
    </nav>
  </div>
</section>
"""


def field_line(slug, units):
    """A line on a field's page pointing to the unit that teaches it."""
    for u in units:
        if u["field"] == slug:
            return (f'<p class="field-also" style="margin-top:32px">In <a href="{INDEX}">The Benedict Year</a>, a homeschool '
                    f'curriculum that walks this map, {esc(essay_map.BY_SLUG[slug]["name"])} is '
                    f'<a href="{u["path"]}">Unit {u["unit"]}, weeks {u["weeks"]}</a>.</p>')
    return ""
