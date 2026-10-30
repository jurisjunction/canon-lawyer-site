#!/usr/bin/env python3
"""The household: every track of the essays, as one family.

Each track's header names its parents, one quoted line per edge, with a
short hash of the parent's original:

    //   whether-the-cloud.strudel.js   VIRI   fd123dbc28e8

This script reads those lines and nothing else, so the family tree has one
source of truth: the tracks themselves. It

  1. checks every edge: the quoted line hashes as its header says, and the
     parent's file holds it, word for word;
  2. writes docs/assets/music/family.strudel.js, the household: every track
     sealed in its own scope, so that any of them can be played or stacked;
  3. writes docs/assets/music/family.svg, the family tree, parents above;
  4. fills the generated parts of the music page (_src/pages/34-music.html):
     the tree, the links that open a track in Strudel, and the sources.

Run it after adding a track, then build:  python3 music.py && python3 build.py
It refuses a broken edge or a cycle. Python standard library only.
"""
import base64, hashlib, html, re, sys, urllib.parse
from pathlib import Path

MUSIC = Path(__file__).parent / "docs" / "assets" / "music"
PAGE = Path(__file__).parent / "_src" / "pages" / "34-music.html"  # A New Song, at /music/

# The tracks, oldest first: file, title, mix, and the page it belongs to.
# A new track goes at the end; its parents must stand above it.
TRACKS = [
    ("whether-the-cloud.strudel.js", "Whether the Cloud Makes Many Worlds", "the dance mix", "/essays/whether-the-cloud-makes-many-worlds/"),
    ("what-is-to-be-done.strudel.js", "What Is to Be Done?", "the garage mix", "/essays/what-is-to-be-done/"),
    ("brother-electron.strudel.js", "Brother Electron", "the clockwork mix", "/essays/brother-electron/"),
    ("a-new-song.strudel.js", "A New Song", "a motet for the household", "/music/"),
    ("on-these-two-hang.strudel.js", "On These Two Hang", "a double fugue", "/music/#the-double-fugue"),
    ("soap-by-its-causes.strudel.js", "Soap, by Its Causes", "the dub mix", "/essays/soap-by-its-causes/"),
]
EDGE = re.compile(r"^//\s+([\w.-]+\.strudel\.js)\s+([A-Z_]+)\s+([0-9a-f]{12})\s*$", re.M)
# A track may say, in its header, that the household hangs on it ("// LIFTED UP."):
# in the order of time it is the youngest, a merge of every track before it;
# in the order of the end every track hangs on it (Matthew 22:40; John 12:32).
# The claim is checked, not taken on its word: such a track must quote them all.
LIFTED = re.compile(r"^// LIFTED UP\.", re.M)


def ident(file):
    return file.replace(".strudel.js", "").replace("-", "_")


def read_tracks():
    tracks = []
    for file, title, mix, page in TRACKS:
        src = (MUSIC / file).read_text(encoding="utf-8")
        tempo = re.search(r"^// (\d+) BPM · (\d+) bars · ~(\d+:\d+)", src, re.M)
        tracks.append({
            "file": file, "id": ident(file), "title": title, "mix": mix, "page": page, "src": src,
            "bpm": int(tempo.group(1)), "bars": int(tempo.group(2)), "length": tempo.group(3),
            "edges": [(p, name, h) for p, name, h in EDGE.findall(src)],
            "lifted": bool(LIFTED.search(src)),
        })
    return tracks


def check(tracks):
    by_file = {t["file"]: t for t in tracks}
    order = [t["file"] for t in tracks]
    problems = []
    for t in tracks:
        for parent, name, h in t["edges"]:
            if parent not in by_file:
                problems.append(f"{t['file']}: parent {parent} is not a track of the household")
                continue
            if order.index(parent) >= order.index(t["file"]):
                problems.append(f"{t['file']}: parent {parent} does not come before it (a cycle, or the order is wrong)")
            # the quoted line is the string in the child that hashes as the header says,
            # whatever the child calls it (the garage mix names its telegraph by the
            # parent's name, TALEA, and keeps it as PARENT_TALEA)
            found = [q for q in set(re.findall(r"'([^'\n]*)'", t["src"]))
                     if hashlib.sha256(q.encode()).hexdigest()[:12] == h]
            if not found:
                problems.append(f"{t['file']}: no quoted line hashes to {h} ({name})")
                continue
            quoted = found[0]
            if f"'{quoted}'" not in by_file[parent]["src"]:
                problems.append(f"{t['file']}: {name} is not quoted as written in {parent}")
        if t["lifted"]:
            quoted = {p for p, _, _ in t["edges"]}
            missing = [f for f in order[:order.index(t["file"])] if f not in quoted]
            if missing:
                problems.append(f"{t['file']}: says the household hangs on it, but does not quote " + ", ".join(missing))
    if problems:
        sys.exit("music.py:\n  " + "\n  ".join(problems))


def lift_samples(src, name):
    """Take a track's samples(...) calls out of its source, whole, and return both.

    Strudel's transpiler (strudel.cc runs it before the code) turns every
    samples(...) into await samples(...), and await is allowed only at the top
    level, not inside the scope each track is sealed in. So the household loads
    every track's samples at its own top level, and each track keeps a note
    where its calls stood. A call starts a line; it ends at its matching
    parenthesis, counted outside quotes."""
    calls, out, i = [], [], 0
    for m in re.finditer(r"^samples\(", src, re.M):
        if m.start() < i:
            continue
        depth, j, quote = 0, m.end() - 1, None
        while True:
            c = src[j]
            if quote:
                if c == "\\":
                    j += 1
                elif c == quote:
                    quote = None
            elif c in "'\"`":
                quote = c
            elif c in "([{":
                depth += 1
            elif c in ")]}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
            if j >= len(src):
                sys.exit(f"music.py: {name}: a samples( call that never closes")
        end = j + 1
        while end < len(src) and src[end] in " ;":
            end += 1
        calls.append(_resolve(src[m.start():end].rstrip(), src, name))
        out.append(src[i:m.start()] + "// (its samples load at the top of the household)")
        i = end
    out.append(src[i:])
    return "".join(out), calls


def _resolve(call, src, name):
    """A lifted call leaves its track's scope, so a name it uses must come with it: a name
    the track defines as a plain string (const VOICES = '...') is written in as that
    string. Any other bare name, outside quotes and not an object key, stops the build."""
    consts = dict(re.findall(r"^const (\w+) = ('[^'\n]*')", src, re.M))
    out, i, quote = [], 0, None
    while i < len(call):
        c = call[i]
        if quote:
            out.append(c)
            if c == "\\":
                out.append(call[i + 1])
                i += 1
            elif c == quote:
                quote = None
            i += 1
            continue
        if c in "'\"`":
            quote = c
            out.append(c)
            i += 1
            continue
        m = re.match(r"[A-Za-z_$][\w$]*", call[i:])
        if m and (i == 0 or not (call[i - 1].isalnum() or call[i - 1] in "_$.")):
            word, after = m.group(0), call[i + m.end():].lstrip()
            if word == "samples" or after.startswith(":"):
                out.append(word)
            elif word in consts:
                out.append(consts[word])
            else:
                sys.exit(f"music.py: {name}: samples(...) uses {word}, which is not a plain string the track defines; "
                         "the household cannot load it at the top level")
            i += m.end()
            continue
        out.append(c)
        i += 1
    return "".join(out)


def seal(t, order):
    """A track in its own scope: its setcpm left to the household, its samples lifted to the
    top, its last arrange returned."""
    src, _ = lift_samples(t["src"], t["file"])
    body = re.sub(r"^setcpm\(.*$", "// (its own tempo: " + str(t["bpm"]) + " BPM; the household keeps one)", src, count=1, flags=re.M)
    body, n = re.subn(r"\narrange\(\n(\s*\[\d+,\s*sec)", r"\nreturn arrange(\n\1", body)
    if n != 1:
        sys.exit(f"music.py: {t['file']} does not end in one arrange(...) of its sections")
    body = "\n".join(("  " + line) if line else "" for line in body.rstrip("\n").split("\n"))
    parents = sorted({p for p, _, _ in t["edges"]}, key=order.index)
    who = ", ".join(ident(p) for p in parents) or "none"
    return f"""// ============================================================
// {t['title'].upper()}: {t['mix']} · {t['bpm']} BPM · {t['bars']} bars
// parents: {who}
// ============================================================
const {t['id']} = (() => {{
{body}
}})()
"""


def household(tracks):
    by_id = [t["id"] for t in tracks]
    # it plays the track the household hangs on, if one says so; else the youngest
    lifted = [t["id"] for t in tracks if t["lifted"]]
    plays = (lifted or by_id)[-1]
    plays_note = ": the track it hangs on (LIFTED UP)" if lifted else ""
    lines = "\n".join(f"//   {t['id']:<22} {t['title']} ({t['mix']}), {t['bars']} bars" for t in tracks)
    order = [t["file"] for t in tracks]
    sealed = "\n\n".join(seal(t, order) for t in tracks)
    loads = []
    for t in tracks:
        for call in lift_samples(t["src"], t["file"])[1]:
            if call not in loads:
                loads.append(call)
    return f"""// ============================================================
// THE HOUSEHOLD: every track of the essays, as one family
// Generated by music.py from the tracks themselves; do not edit by hand.
// For Strudel (https://strudel.cc): paste, press play (Ctrl+Enter).
// Dedicated to the public domain (CC0 1.0).
//
// "Every scribe which is instructed unto the kingdom of heaven is
// like unto a man that is an householder, which bringeth forth out of
// his treasure things new and old" (Matthew 13:52).
//
// Each track is sealed in its own scope, so that its names do not
// collide with the others', and the household keeps one tempo. Strudel
// counts in bars, not seconds, so every track locks to it: the cloud
// slows from 122, the garage from 132. The tracks in the house:
{lines}
//
// Play one, or stack them, at the bottom. Some things to try:
//   stack(what_is_to_be_done, brother_electron)  // the children: the same seven notes
//   stack(whether_the_cloud, brother_electron)   // the eldest and the youngest: both 132 bars
//   brother_electron.mask("<1 0>")               // every other bar, to make room for another
// Stacked tracks are loud: .postgain(.6) on each keeps them from clipping.
// ============================================================

setcpm(120/4) // the household's tempo

// Every track's samples, loaded here at the top, where Strudel can wait
// for them (its transpiler awaits each samples() call, and await works
// only at the top level, not inside a track's own scope).
{chr(10).join(loads)}

{sealed}
// ============================================================
// THE HOUSEHOLD PLAYS{plays_note}
// ============================================================
{plays}
"""


def svg(tracks):
    """The family tree, oldest at the top: an arc diagram, drawn from the headers.

    A child of the track just above hangs straight beneath it; an edge that
    skips a generation is an arc on the left or the right, whichever side it
    can take without crossing another, nested outward by span. Each edge is
    named by the line it carries and the first six hex of its hash.
    """
    idx = {t["file"]: i for i, t in enumerate(tracks)}
    edges = []
    for t in tracks:
        groups = {}
        for parent, name, h in t["edges"]:
            groups.setdefault(parent, []).append(f"{name} {h[:6]}")
        edges += [(idx[parent], idx[t["file"]], tuple(names)) for parent, names in groups.items()]
    straight = [e for e in edges if e[1] - e[0] == 1]
    arcs = {"L": [], "R": []}  # side -> [(edge, depth)]
    for e in sorted((e for e in edges if e[1] - e[0] > 1), key=lambda e: (e[1] - e[0], e[0])):
        def cost(side):
            crossings = sum(f[0] < e[0] < f[1] < e[1] or e[0] < f[0] < e[1] < f[1] for f, _ in arcs[side])
            depth = 1 + max((d for f, d in arcs[side] if e[0] <= f[0] and f[1] <= e[1]), default=0)
            return crossings, depth
        side = min(("L", "R"), key=cost)
        arcs[side].append((e, cost(side)[1]))

    BW, BH, ROW, TOP, REACH = 360, 56, 132, 24, 66   # REACH: how far out an arc of depth 1 swings
    text_w = lambda names: max(len(n) for n in names) * 6.4
    margin = 24
    for side in arcs:
        for e, d in arcs[side]:
            margin = max(margin, REACH * d + text_w(e[2]) / 2 + 12)
    W = int(2 * margin + BW)
    cx = W / 2
    ys = [TOP + BH / 2 + i * ROW for i in range(len(tracks))]
    H = int(ys[-1] + BH / 2 + TOP)

    # where each arc meets a box: arriving arcs above leaving ones, the widest nearest the middle
    ends = {}
    for side in arcs:
        for i in range(len(tracks)):
            arriving = sorted((e for e, _ in arcs[side] if e[1] == i), key=lambda e: e[1] - e[0])
            leaving = sorted((e for e, _ in arcs[side] if e[0] == i), key=lambda e: e[0] - e[1])
            column = [("in", e) for e in arriving] + [("out", e) for e in leaving]
            for k, key in enumerate(column):
                ends[(side, i) + key] = ys[i] + (k - (len(column) - 1) / 2) * 11

    gold, ink, muted, paper = "#a8844c", "#1c2230", "#5a6273", "#f8f5ef"
    label = lambda x, y, names, anchor: "".join(
        f'<text x="{x:.0f}" y="{y + (j - (len(names) - 1) / 2) * 13 + 3.5:.0f}" text-anchor="{anchor}" font-size="10.5" '
        f'letter-spacing=".04em" fill="{muted}" stroke="{paper}" stroke-width="5" stroke-linejoin="round" paint-order="stroke">{html.escape(n)}</text>'
        for j, n in enumerate(names))
    lines, labels = [], []
    for a, b, names in straight:
        y1, y2 = ys[a] + BH / 2, ys[b] - BH / 2
        lines.append(f'<path d="M{cx:.0f} {y1:.0f}V{y2 - 1:.0f}" fill="none" stroke="{gold}" stroke-width="1.4" marker-end="url(#ft-a)"/>')
        labels.append(label(cx + 12, (y1 + y2) / 2, names, "start"))
    for side, sign in (("L", -1), ("R", 1)):
        for (a, b, names), d in arcs[side]:
            sx = cx + sign * BW / 2
            y1, y2 = ends[(side, a, "out", (a, b, names))], ends[(side, b, "in", (a, b, names))]
            c = sx + sign * REACH * d / .75   # a cubic's middle reaches three quarters of the way to its handles
            lines.append(f'<path d="M{sx:.0f} {y1:.0f}C{c:.0f} {y1:.0f},{c:.0f} {y2:.0f},{sx + sign:.0f} {y2:.0f}" fill="none" stroke="{gold}" stroke-width="1.4" marker-end="url(#ft-a)"/>')
            labels.append(label(sx + sign * REACH * d, (y1 + y2) / 2, names, "middle"))

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" class="family-svg" role="img" aria-labelledby="ft-t ft-d" font-family="Inter, system-ui, sans-serif">',
           '<title id="ft-t">The household: the tracks as a family tree</title>',
           '<desc id="ft-d">' + html.escape(" ".join(
               f"{t['title']} quotes " + "; ".join(f"{name} from {tracks[idx[p]]['title']}" for p, name, _ in t["edges"]) + "."
               for t in tracks if t["edges"]) + "".join(
               f" Every track hangs on {t['title']}: it quotes every track before it, so through it each is kin to every other."
               for t in tracks if t["lifted"])) + '</desc>',
           f'<defs><marker id="ft-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{gold}"/></marker></defs>']
    out += lines + labels
    for t, y in zip(tracks, ys):
        lifted = t["lifted"]   # the household hangs on it: drawn in gold, and says so
        fill, width = ("#f6ecd9", 2.4) if lifted else ("#fffdf9", 1.3)
        note = " · ALL HANG ON IT" if lifted else ""
        out.append(f'<a href="{t["page"]}"><rect x="{cx - BW / 2:.0f}" y="{y - BH / 2:.0f}" width="{BW}" height="{BH}" rx="6" fill="{fill}" stroke="{gold}" stroke-width="{width}"/>'
                   f'<text x="{cx:.0f}" y="{y - 4:.0f}" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="19" fill="{ink}">{html.escape(t["title"])}</text>'
                   f'<text x="{cx:.0f}" y="{y + 16:.0f}" text-anchor="middle" font-size="10.5" fill="{muted}" letter-spacing=".08em">{html.escape(t["mix"].upper())} · {t["bpm"]} BPM · {t["bars"]} BARS{note}</text></a>')
    out.append("</svg>")
    return "\n".join(out) + "\n"


def strudel_link(src):
    """strudel.cc opens the code carried in the link's fragment: base64, then URI-encoded, as Strudel's own share links are."""
    return "https://strudel.cc/#" + urllib.parse.quote(base64.b64encode(src.encode("utf-8")).decode("ascii"), safe="")


def fill_page(tracks, tree):
    """Fill the music page's generated parts, so that it never drifts from the tracks:
    <a data-strudel="FILE" href="..."> gets a link that opens FILE in Strudel,
    <code data-source="FILE">...</code> gets FILE's source, and the figure
    between <!-- family.svg --> and <!-- /family.svg --> gets the tree."""
    if not PAGE.exists():
        return
    page = PAGE.read_text(encoding="utf-8")
    source = lambda f: (MUSIC / f).read_text(encoding="utf-8")
    page = re.sub(r'(<a data-strudel="([\w.-]+)" href=")[^"]*(")', lambda m: m.group(1) + strudel_link(source(m.group(2))) + m.group(3), page)
    page = re.sub(r'(<code data-source="([\w.-]+)">).*?(</code>)', lambda m: m.group(1) + html.escape(source(m.group(2)), quote=False) + m.group(3), page, flags=re.S)
    page = re.sub(r"(<!-- family.svg -->\n).*?(<!-- /family.svg -->)", lambda m: m.group(1) + tree + m.group(2), page, flags=re.S)
    PAGE.write_text(page, encoding="utf-8")


def main():
    tracks = read_tracks()
    check(tracks)
    (MUSIC / "family.strudel.js").write_text(household(tracks), encoding="utf-8")
    tree = svg(tracks)
    (MUSIC / "family.svg").write_text(tree, encoding="utf-8")
    fill_page(tracks, tree)
    edges = sum(len(t["edges"]) for t in tracks)
    print(f"music.py: {len(tracks)} tracks, {edges} quoted lines, every hash and every parent checked; "
          f"family.strudel.js, family.svg and the music page written")


if __name__ == "__main__":
    main()
