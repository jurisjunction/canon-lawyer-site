#!/usr/bin/env python3
"""Illumination by rule for "Venite ad me 90-94, glossed".

Nothing here is painted. Every ornament is computed from a word of the
leaf's own text by a rule stated in the colophon; the same word and the
same seed give the same image. The rules are borrowed from the
household's Strudel tracks (the gates, the telegraph, the wheels, the
divisions, the isorhythm, the hashes), under three more: made by rule,
never painted; no figures; seed and rule in the colophon.

It reads the leaves of the glossed book and writes them illuminated; the
four plates of the auctoritates leaves are in auct_plates.py. The plates and
the frame can be drawn on their own: see plate_* and frame() below.

Standard library only. Usage: illum.py SRC_DIR DST_DIR
"""
import hashlib
import math
import pathlib
import re
import sys
import urllib.parse

# ---------------------------------------------------------------- strands
TEXT = '#1a140e'      # ink: the text
INK = '#3d2c1c'       # ink for drawing
LAPIS = '#22407a'     # the prayer
LAPIS_LT = '#4f74c0'
CINNABAR = '#9b2a1a'  # the law
GOLD = '#c9952f'      # the given
GOLD_LT = '#e2bd62'
GOLD_PALE = '#f6dd8e'
GOLD_DK = '#7a5418'
GOLD_MID = '#d4a845'
MATTER = '#9aa0ad'    # what has passed
RULE = '#b07a1e'
CORNER = '#e8d9b4'

GOLDEN = 137.50776405
W, H = 1056, 1632
MID = 23.75           # the midline between the leaf's two frame rules

NOTE = ['C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B']
MAJOR = [0, 2, 4, 5, 7, 9, 11]
MONO = "'IBM Plex Mono',ui-monospace,monospace"
SERIF = "'EB Garamond',Georgia,serif"
UNCIAL = "'Uncial Antiqua','EB Garamond',serif"

MORSE = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
         'G': '--.', 'H': '....', 'I': '..', 'K': '-.-', 'L': '.-..', 'M': '--',
         'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...',
         'T': '-', 'U': '..-', 'V': '...-', 'X': '-..-', 'Y': '-.--', 'Z': '--..'}


def h12(s):
    """sha256 of the quoted words, first 12 hex, as the tracks keep them."""
    return hashlib.sha256(s.encode()).hexdigest()[:12]


def euclid(k, n):
    """E(k,n): k onsets spread as evenly as they can be over n steps."""
    return [1 if (i * k) % n < k else 0 for i in range(n)]


def key_set(t):
    return sorted((t + i) % 12 for i in MAJOR)


def bits(word):
    return [format(ord(c), '08b') for c in word]


def morse_units(word):
    """The word as (kind, start, length) on a grid of units: dot 1, dash 3,
    1 between signs, 3 between letters, 7 after the word."""
    out, u = [], 0
    for li, ch in enumerate(word):
        if li:
            u += 3
        for si, sign in enumerate(MORSE[ch]):
            if si:
                u += 1
            n = 1 if sign == '.' else 3
            out.append(('.' if n == 1 else '-', u, n))
            u += n
    return out, u + 7


def xorshift(seed):
    x = (seed * 2654435761) & 0xFFFFFFFF or 1
    while True:
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= x >> 17
        x ^= (x << 5) & 0xFFFFFFFF
        yield x / 0xFFFFFFFF


def f(x):
    return f'{x:.1f}'.rstrip('0').rstrip('.') if abs(x - round(x)) > 1e-9 else str(int(round(x)))


# ---------------------------------------------------------------- the leaves
# The keys go up by fifths and come home (my end is my beginning); the
# divisions cut five times and join five times. Both are palindromes.
LEAVES = [
    # file, label, n, word, source, quoted words
    ('Main', 'fol. i', 90, 'TRADIDI', '1 Cor 11:23, Vulg.', 'Ego enim accepi a Domino quod et tradidi vobis'),
    ('Auct1', 'auct. i', 90, 'CULMEN', 'SC 10', 'culmen ad quod actio Ecclesiae tendit'),
    ('Folio2', 'fol. ii', 91, 'SUBSTANTIA', 'Trent XXI, 2', 'salva illorum substantia'),
    ('Auct2', 'auct. ii', 91, 'APTATIO', 'SC 38', 'legitimis variationibus et aptationibus'),
    ('Folio3', 'fol. iii', 92, 'SUPPLICANDI', 'Indiculus 8', 'ut legem credendi lex statuat supplicandi'),
    ('Auct3', 'auct. iii', 92, 'ACTUOSA', 'SC 14', 'consciam atque actuosam'),
    ('Folio4', 'fol. iv', 93, 'VIDEAM', 'Ps 26:4, Vulg.', 'ut videam voluptatem Domini'),
    ('Auct4', 'auct. iv', 93, 'SILENTIUM', 'SC 30', 'sacrum silentium servetur'),
    ('Folio5', 'fol. v', 94, 'ORDINEM', '1 Cor 14:40, Vulg.', 'omnia autem honeste et secundum ordinem fiant'),
    ('Auct5', 'auct. v', 94, 'FIDELITER', 'c. 846 §1', 'fideliter serventur libri liturgici'),
]
KEYS = [7, 2, 9, 4, 11, 11, 4, 9, 2, 7]          # G D A E B | B E A D G
CUTS = [2, 4, 8, 16, 32, 32, 16, 8, 4, 2]


# ---------------------------------------------------------------- the frame
def gates(word, x=41, y0=210, y1=1422):
    """THE GATES: the word in ASCII down the inner margin, eight bits a
    letter: a filled cell a crossing, an empty one a waiting. It loops."""
    n = len(word)
    span = y1 - y0
    sep = 1.4
    reps = 1
    while span / (reps * n * (8 + sep) + sep) > 15.5:
        reps += 1
    p = span / (reps * n * (8 + sep) + sep)
    out = []
    y = y0
    seq = [c for _ in range(reps) for c in word]
    for ch in seq:
        out.append(f'<circle cx="{x}" cy="{f(y + sep * p / 2)}" r="{f(min(3.4, sep * p / 2 - .6))}" fill="{GOLD}" stroke="{GOLD_DK}" stroke-width=".6"/>')
        y += sep * p
        b = format(ord(ch), '08b')
        out.append(f'<text x="{x + 12}" y="{f(y + 4 * p + 3)}" font-family="{MONO}" font-size="8.5" fill="{CINNABAR}" fill-opacity=".8">{ch}</text>')
        for bit in b:
            if bit == '1':
                out.append(f'<rect x="{x - 4.5}" y="{f(y + 1.1)}" width="9" height="{f(p - 2.2)}" rx="1" fill="{LAPIS}"/>')
            else:
                out.append(f'<rect x="{x - 4}" y="{f(y + 1.6)}" width="8" height="{f(p - 3.2)}" rx="1" fill="none" stroke="{INK}" stroke-opacity=".45" stroke-width=".7"/>')
            y += p
    out.append(f'<circle cx="{x}" cy="{f(y + sep * p / 2)}" r="{f(min(3.4, sep * p / 2 - .6))}" fill="{GOLD}" stroke="{GOLD_DK}" stroke-width=".6"/>')
    return '\n'.join(out), reps


def telegraph(word, x0=52, x1=1004, y=MID):
    """THE TELEGRAPH: the word in Morse along the head of the frame, looped."""
    signs, units = morse_units(word)
    L = x1 - x0
    reps = max(1, int(L / (units * 3.6)))
    u = L / (reps * units)
    out = []
    for r in range(reps):
        base = x0 + r * units * u
        for kind, s, n in signs:
            if kind == '.':
                out.append(f'<circle cx="{f(base + (s + .5) * u)}" cy="{y}" r="{f(min(1.55, u * .42))}" fill="{INK}"/>')
            else:
                out.append(f'<rect x="{f(base + s * u + .35 * u)}" y="{f(y - 1.15)}" width="{f(n * u - .7 * u)}" height="2.3" rx="1" fill="{CINNABAR}"/>')
    return '\n'.join(out), reps


def divisions(d, x0=52, x1=1004, y=H - MID):
    """THE DIVISIONS: the foot of the frame cut into d equal parts."""
    out = []
    for k in range(1, d):
        x = x0 + k * (x1 - x0) / d
        mid = (k * 2 == d)
        out.append(f'<line x1="{f(x)}" y1="{f(y - 2.8)}" x2="{f(x)}" y2="{f(y + 2.8)}" stroke="{INK}" stroke-width=".7" stroke-opacity=".6"/>')
        out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{2.1 if mid else 1.6}" fill="{CINNABAR if mid else GOLD}" stroke="{GOLD_DK}" stroke-width=".4"/>')
    return '\n'.join(out)


def isorhythm(word, y0=52, y1=H - 52, step=8):
    """THE ISORHYTHM: a talea E(k,16), k the letters of the word, carrying the
    strands in turn (a colour of three against a talea of k): down the left
    side, and backwards up the right, a crab."""
    k = len(word)
    talea = euclid(k, 16)
    colour = [LAPIS, CINNABAR, GOLD]
    steps = int((y1 - y0) / step)
    out, c = [], 0
    for i in range(steps):
        if talea[i % 16]:
            y = y0 + (i + .5) * step
            col = colour[c % 3]
            c += 1
            for x, yy in ((MID, y), (W - MID, H - y)):
                out.append(f'<circle cx="{f(x)}" cy="{f(yy)}" r="1.7" fill="{col}"/>')
    return '\n'.join(out)


def wheel(cx, cy, key, beat):
    """THE WHEELS: a wheel in the middle of a wheel. The ring of twelve holds
    the leaf's key (C at the top, its seven notes in gold, the tonic in
    cinnabar); the ring of four marks this corner's beat; one in the middle."""
    out = [f'<circle cx="{f(cx)}" cy="{f(cy)}" r="22.5" fill="{CORNER}" stroke="{RULE}" stroke-width=".9"/>',
           f'<circle cx="{f(cx)}" cy="{f(cy)}" r="18.5" fill="none" stroke="{RULE}" stroke-width=".6"/>',
           f'<circle cx="{f(cx)}" cy="{f(cy)}" r="10" fill="none" stroke="{RULE}" stroke-width=".5"/>']
    scale = key_set(key)
    for pc in range(12):
        a = math.radians(-90 + 30 * pc)
        x, y = cx + 18.5 * math.cos(a), cy + 18.5 * math.sin(a)
        if pc in scale:
            fill = CINNABAR if pc == key else GOLD
            out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="2.5" fill="{fill}" stroke="{GOLD_DK}" stroke-width=".45"/>')
        else:
            out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r=".95" fill="{INK}"/>')
    for b in range(4):
        a = math.radians(-90 + 90 * b)
        x, y = cx + 10 * math.cos(a), cy + 10 * math.sin(a)
        if b == beat:
            out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="2.3" fill="{LAPIS}"/>')
        else:
            out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r=".95" fill="{INK}"/>')
    out.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="3.3" fill="{GOLD}" stroke="{GOLD_DK}" stroke-width=".6"/>')
    return '\n'.join(out)


def frame(i):
    file, label, n, word, src, quote = LEAVES[i]
    g, greps = gates(word)
    t, treps = telegraph(word)
    parts = [
        f'<svg class="regula" viewBox="0 0 {W} {H}" width="{W}" height="{H}" aria-hidden="true">',
        f'<g>{t}</g>', f'<g>{divisions(CUTS[i])}</g>', f'<g>{isorhythm(word)}</g>', f'<g>{g}</g>',
        wheel(MID, MID, KEYS[i], 0), wheel(W - MID, MID, KEYS[i], 1),
        wheel(W - MID, H - MID, KEYS[i], 2), wheel(MID, H - MID, KEYS[i], 3),
        '</svg>']
    return '\n'.join(parts)


# ---------------------------------------------------------------- grounds
def data_uri(svg):
    return 'data:image/svg+xml,' + urllib.parse.quote(svg, safe=" =:/'(),;-.")


def circulant(ch, on=GOLD_LT, off='#d3a748'):
    """An initial's ground: its own byte, turned one place a row."""
    b = ord(ch)
    cells = []
    for r in range(8):
        row = ((b << r) | (b >> (8 - r))) & 0xFF
        for c in range(8):
            bit = (row >> (7 - c)) & 1
            cells.append(f"<rect x='{c}' y='{r}' width='1' height='1' fill='{on if bit else off}'/>")
    svg = f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 8 8' preserveAspectRatio='none' shape-rendering='crispEdges'>{''.join(cells)}</svg>"
    return data_uri(svg)


def morse_tail(word, u=3.4):
    """The initial's tail: the leaf's word in Morse, running down the gutter."""
    signs, units = morse_units(word)
    units -= 7
    u = min(u, 330 / units)
    hgt = units * u
    els = []
    for kind, s, n in signs:
        if kind == '.':
            els.append(f"<circle cx='3' cy='{f((s + .5) * u)}' r='{f(min(1.6, u * .45))}' fill='{CINNABAR}'/>")
        else:
            els.append(f"<rect x='1.8' y='{f(s * u + .3 * u)}' width='2.4' height='{f(n * u - .6 * u)}' rx='1' fill='{CINNABAR}'/>")
    svg = f"<svg xmlns='http://www.w3.org/2000/svg' width='6' height='{f(hgt)}' viewBox='0 0 6 {f(hgt)}'>{''.join(els)}</svg>"
    return data_uri(svg), hgt


def phyllo_ground(n=233):
    els = []
    c = 47 / math.sqrt(n)
    for k in range(1, n):
        r = c * math.sqrt(k)
        a = math.radians(k * GOLDEN)
        x, y = 50 + r * math.cos(a), 50 + r * math.sin(a)
        col = GOLD if k % 13 == 0 else LAPIS_LT
        op = .9 if k % 13 == 0 else .55
        els.append(f"<circle cx='{x:.2f}' cy='{y:.2f}' r='{.7 + .6 * k / n:.2f}' fill='{col}' fill-opacity='{op}'/>")
    svg = f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100' preserveAspectRatio='xMidYMid slice'>{''.join(els)}</svg>"
    return data_uri(svg)


# ---------------------------------------------------------------- the plates
def plate_wrap(num, title, svg, caption, width):
    return (f'<div class="tabula" style="max-width: {width}px">\n'
            f'<p class="sig" style="color: {{{{rubric}}}}; text-align: center">Tabula {num} · {title}</p>\n'
            f'{svg}\n<p class="tab-cap">{caption}</p>\n</div>')


def plate_refresh(seed=90, width=640):
    """I. THE REFRESH. 1 Cor 11:24 in ASCII, a letter a column, a bit a row,
    each row written back before it fades. The cursor is seed mod 8."""
    text = 'HOC FACITE IN MEAM COMMEMORATIONEM'
    n = len(text)
    pitch = min(17.5, (width - 34) / n)
    cell = pitch - 3.6
    left, top = 26, 6
    cur = seed % 8
    out = []
    for r in range(8):
        age = (cur - r) % 8
        op = 1 - .085 * age
        y = top + r * pitch
        for j, ch in enumerate(text):
            bit = (ord(ch) >> (7 - r)) & 1
            x = left + j * pitch
            if bit:
                out.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(cell)}" height="{f(cell)}" rx="1.2" fill="{LAPIS}" fill-opacity="{op:.2f}"/>')
            else:
                out.append(f'<rect x="{f(x + .5)}" y="{f(y + .5)}" width="{f(cell - 1)}" height="{f(cell - 1)}" rx="1.2" fill="none" stroke="{INK}" stroke-width=".6" stroke-opacity="{op * .5:.2f}"/>')
    yc = top + cur * pitch
    out.append(f'<rect x="{f(left - 3)}" y="{f(yc - 2.2)}" width="{f(n * pitch + 2.4)}" height="{f(cell + 4.4)}" rx="2" fill="none" stroke="{CINNABAR}" stroke-width="1.1"/>')
    out.append(f'<path d="M {f(left - 16)} {f(yc + cell / 2 - 5)} l 8 5 l -8 5 z" fill="{CINNABAR}"/>')
    ly = top + 8 * pitch + 9
    for j, ch in enumerate(text):
        x = left + j * pitch + cell / 2
        out.append(f'<text x="{f(x)}" y="{f(ly)}" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{CINNABAR}">{ch if ch != " " else "·"}</text>')
    wv = left + n * pitch + 8
    hv = ly + 6
    svg = f'<svg viewBox="0 0 {f(wv)} {f(hv)}" width="{f(wv)}" height="{f(hv)}" role="img" aria-label="Hoc facite in meam commemorationem in ASCII bits, a refreshing memory">\n' + '\n'.join(out) + '\n</svg>'
    cap = ('<i>Hoc facite in meam commemorationem</i> (1 Cor 11:24, Vulgate) in ASCII, a letter a column, '
           'eight bits deep. A memory keeps its bits only by reading each row and writing it back before it fades: '
           f'the cursor is on row {cur + 1} (seed {seed}); the rows behind it are fresh, those ahead fading. '
           'As often as you do this, <i>donec veniat</i> (v. 26).')
    return plate_wrap('I', 'Memoria', svg, cap, width)


def plate_fifths(width=928):
    """II. THE FIFTHS. E(7,12) counted from C is G major. Carried up a fifth it
    turns, keeps its shape, keeps six notes and moves one by a semitone."""
    R = 102
    cy = 140
    xs = [158, 464, 770]
    keys = [7, 2, 9]
    out = []
    for w, (cx, t) in enumerate(zip(xs, keys)):
        S = key_set(t)
        P = key_set(keys[w - 1]) if w else None
        added = [p for p in S if P and p not in P]
        gone = [p for p in P if p not in S] if P else []

        def pt(pc, r=R):
            a = math.radians(-90 + 30 * pc)
            return cx + r * math.cos(a), cy + r * math.sin(a)
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{RULE}" stroke-width=".9"/>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{R + 5}" fill="none" stroke="{RULE}" stroke-width=".4"/>')
        if P:
            d = ' '.join(('M' if i == 0 else 'L') + f' {f(pt(p)[0])} {f(pt(p)[1])}' for i, p in enumerate(P)) + ' Z'
            out.append(f'<path d="{d}" fill="none" stroke="{MATTER}" stroke-width="1.3" stroke-dasharray="4 3"/>')
        d = ' '.join(('M' if i == 0 else 'L') + f' {f(pt(p)[0])} {f(pt(p)[1])}' for i, p in enumerate(S)) + ' Z'
        out.append(f'<path d="{d}" fill="{LAPIS}" fill-opacity=".07" stroke="{LAPIS}" stroke-width="1.7" stroke-linejoin="round"/>')
        for pc in range(12):
            x, y = pt(pc)
            lx, ly = pt(pc, R + 19)
            if pc in S:
                fill = CINNABAR if pc in added else GOLD
                out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="6.5" fill="{fill}" stroke="{GOLD_DK}" stroke-width=".8"/>')
                if pc == t:
                    out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="10.5" fill="none" stroke="{LAPIS}" stroke-width="1.5"/>')
            else:
                out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="2" fill="{INK}" fill-opacity=".55"/>')
                if pc in gone:
                    out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="7.5" fill="none" stroke="{CINNABAR}" stroke-width="1.1" stroke-dasharray="2.4 2"/>')
            out.append(f'<text x="{f(lx)}" y="{f(ly + 4.5)}" text-anchor="middle" font-family="{SERIF}" font-size="13" fill="{TEXT if pc in S else MATTER}">{NOTE[pc]}</text>')
        out.append(f'<text x="{cx}" y="{cy + 9}" text-anchor="middle" font-family="{UNCIAL}" font-size="28" fill="{CINNABAR}">{NOTE[t]}</text>')
        sub = 'given' if not P else f'{NOTE[gone[0]]} → {NOTE[added[0]]}'
        out.append(f'<text x="{cx}" y="{cy + R + 46}" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="{INK}">{sub}</text>')
        if w:
            ax = (xs[w - 1] + cx) / 2
            ty = cy - R + 2
            out.append(f'<text x="{f(ax)}" y="{ty}" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="13" fill="{RULE}">a fifth up</text>')
            out.append(f'<path d="M {f(ax - 22)} {ty + 10} L {f(ax + 20)} {ty + 10} M {f(ax + 14)} {ty + 6} L {f(ax + 20)} {ty + 10} L {f(ax + 14)} {ty + 14}" fill="none" stroke="{RULE}" stroke-width="1.1"/>')
    hv = cy + R + 54
    svg = f'<svg viewBox="0 0 {width} {hv}" width="{width}" height="{hv}" role="img" aria-label="the major scale on the circle of twelve, in G, D and A">\n' + '\n'.join(out) + '\n</svg>'
    cap = ('Seven notes in twelve, spread as evenly as they can be (the Euclidean rhythm E(7,12)), are the major scale; '
           'counted from C they are G. Carried up a fifth the figure turns but keeps its shape: six notes stay, one moves a semitone '
           '(cinnabar; its old place ringed, the old figure in grey). G, D, A are the keys of the corner wheels of fol. i, auct. i and fol. ii. '
           '<i>Salva illorum substantia</i>, the rest ordered to the place.')
    return plate_wrap('III', 'Salva substantia', svg, cap, width)


def plate_slits(width=928):
    """III. TWO OPENINGS. Young's experiment: one source, two openings,
    supplicandi and credendi; where crests from both meet, gold."""
    hv = 158
    src = (64, 79)
    bx = 252
    A, B = (bx, 30), (bx, 128)
    lam = 10
    x1 = 884
    out = [f'<defs><clipPath id="clipL"><rect x="0" y="4" width="{bx}" height="{hv - 8}"/></clipPath>'
           f'<clipPath id="clipR"><rect x="{bx}" y="4" width="{x1 - bx}" height="{hv - 8}"/></clipPath></defs>']
    g = [f'<g clip-path="url(#clipL)">']
    for k in range(1, int((bx - src[0]) / lam) + 2):
        g.append(f'<circle cx="{src[0]}" cy="{src[1]}" r="{k * lam}" fill="none" stroke="{INK}" stroke-opacity=".28" stroke-width=".7"/>')
    g.append('</g>')
    out += g
    K = int(math.hypot(x1 - bx, hv) / lam) + 1
    g = [f'<g clip-path="url(#clipR)">']
    for k in range(1, K + 1):
        g.append(f'<circle cx="{A[0]}" cy="{A[1]}" r="{k * lam}" fill="none" stroke="{LAPIS}" stroke-opacity=".2" stroke-width=".6"/>')
        g.append(f'<circle cx="{B[0]}" cy="{B[1]}" r="{k * lam}" fill="none" stroke="{GOLD_DK}" stroke-opacity=".2" stroke-width=".6"/>')
    g.append('</g>')
    out += g
    d = B[1] - A[1]
    beads = []
    for i in range(1, K + 1):
        for j in range(1, K + 1):
            r1, r2 = i * lam, j * lam
            if abs(i - j) > 3 or abs(r1 - r2) > d or r1 + r2 < d:
                continue
            a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
            hh = math.sqrt(max(0, r1 * r1 - a * a))
            yy = A[1] + a
            for x in (bx + hh, bx - hh):
                if bx + 3 < x < x1 - 2 and 6 < yy < hv - 6:
                    beads.append((x, yy, i == j))
    for x, y, central in beads:
        if central:
            beads_el = f'<circle cx="{f(x)}" cy="{f(y)}" r="2.2" fill="{GOLD_PALE}" stroke="{GOLD_DK}" stroke-width=".6"/>'
        else:
            beads_el = f'<circle cx="{f(x)}" cy="{f(y)}" r="1.55" fill="{GOLD}"/>'
        out.append(beads_el)
    # the wall: the light that reaches it
    wx = x1 + 10
    for y in range(6, hv - 6):
        dd = math.hypot(wx - A[0], y - A[1]) - math.hypot(wx - B[0], y - B[1])
        I = math.cos(math.pi * dd / lam) ** 2
        out.append(f'<rect x="{wx}" y="{y}" width="14" height="1.05" fill="{GOLD}" fill-opacity="{I:.2f}"/>')
    out.append(f'<rect x="{wx}" y="6" width="14" height="{hv - 12}" fill="none" stroke="{RULE}" stroke-width=".7"/>')
    # the barrier with its two openings
    gap = 5
    segs = [(6, A[1] - gap), (A[1] + gap, B[1] - gap), (B[1] + gap, hv - 6)]
    for y0, y1 in segs:
        out.append(f'<line x1="{bx}" y1="{y0}" x2="{bx}" y2="{y1}" stroke="{INK}" stroke-width="3.2"/>')
    out.append(f'<circle cx="{src[0]}" cy="{src[1]}" r="4.5" fill="{GOLD}" stroke="{GOLD_DK}" stroke-width=".8"/>')
    out.append(f'<text x="{src[0]}" y="{src[1] + 22}" text-anchor="middle" font-family="{MONO}" font-size="9.5" fill="{INK}">TRADITA</text>')
    out.append(f'<text x="{bx - 8}" y="{A[1] - 8}" text-anchor="end" font-family="{MONO}" font-size="9.5" fill="{LAPIS}">SUPPLICANDI</text>')
    out.append(f'<text x="{bx - 8}" y="{B[1] + 16}" text-anchor="end" font-family="{MONO}" font-size="9.5" fill="{GOLD_DK}">CREDENDI</text>')
    svg = f'<svg viewBox="0 0 {width} {hv}" width="{width}" height="{hv}" role="img" aria-label="two-slit interference: one source, two openings">\n' + '\n'.join(out) + '\n</svg>'
    cap = ('Young’s two openings. One source, two openings, <i>supplicandi</i> and <i>credendi</i>; the crests from each are drawn as rings, '
           'and where a crest from one meets a crest from the other, gold. The bars on the right are the light that reaches the wall. '
           'Neither opening alone makes bands: they come from two openings lit by one source, what is <i>ab apostolis tradita</i>.')
    return plate_wrap('V', 'Lex supplicandi, lex credendi', svg, cap, width)


def plate_tesserae(seed=93, width=928):
    """IV. TESSERAE. Laid by the golden angle from the middle of the springing
    line; every sixth course in lapis; a ray lightens what it crosses. The tints are loaded dice: xorshift from the seed."""
    R = 262
    cx, cy = width / 2, 274
    c = 7.1
    N = int((R / c) ** 2)
    rnd = xorshift(seed)
    p0 = (cx - 340, 0)
    ang = math.radians(28)
    ux, uy = math.cos(ang), math.sin(ang)
    out = [f'<path d="M {f(cx - R - 12)} {cy} A {R + 12} {R + 12} 0 0 1 {f(cx + R + 12)} {cy}" fill="none" stroke="{RULE}" stroke-width="1.3"/>',
           f'<path d="M {f(cx - R - 17)} {cy} A {R + 17} {R + 17} 0 0 1 {f(cx + R + 17)} {cy}" fill="none" stroke="{CINNABAR}" stroke-width=".6"/>']
    s = c * .78
    for k in range(1, N):
        r = c * math.sqrt(k)
        a = math.radians(k * GOLDEN)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        roll = next(rnd)
        if y > cy - 4:
            continue
        dist = abs((x - p0[0]) * uy - (y - p0[1]) * ux)
        lit = dist < 26
        if int(math.sqrt(k)) % 6 == 0:
            col = LAPIS_LT if lit else LAPIS
        else:
            col = GOLD_PALE if lit else (GOLD if roll < .45 else GOLD_MID if roll < .8 else GOLD_LT)
        t = a
        pts = []
        for q in range(4):
            qa = t + math.pi / 4 + q * math.pi / 2
            pts.append((x + s / math.sqrt(2) * math.cos(qa), y + s / math.sqrt(2) * math.sin(qa)))
        d = 'M' + ' L'.join(f'{px:.1f} {py:.1f}' for px, py in pts) + 'Z'
        out.append(f'<path d="{d}" fill="{col}"/>')
    out.append(f'<line x1="{f(cx - R - 24)}" y1="{cy}" x2="{f(cx + R + 24)}" y2="{cy}" stroke="{RULE}" stroke-width="1.3"/>')
    out.append(f'<circle cx="{f(cx)}" cy="{cy}" r="4" fill="{CINNABAR}" stroke="{GOLD_DK}" stroke-width=".6"/>')
    hv = cy + 6
    svg = f'<svg viewBox="0 0 {width} {hv}" width="{width}" height="{hv}" role="img" aria-label="tesserae laid by the golden angle in a half-dome, crossed by a ray">\n' + '\n'.join(out) + '\n</svg>'
    cap = ('Tesserae laid by the golden angle: the n-th at a distance √n from the middle of the springing line, turned 137.5° from the one before, '
           'and the spirals come of themselves. Every sixth course is lapis; a ray from the window lightens what it crosses. '
           f'The golds are loaded dice (seed {seed}), falling the same way every time. Nothing is pictured: it is only laid, and seen.')
    return plate_wrap('VII', 'In aspectu', svg, cap, width)


def plain_bob():
    pn = ['x', '16'] * 5 + ['x', '12']
    row = [1, 2, 3, 4, 5, 6]
    rows = [row[:]]
    for lead in range(5):
        for p in pn:
            r = row[:]
            if p == 'x':
                pairs = [(0, 1), (2, 3), (4, 5)]
            elif p == '16':
                pairs = [(1, 2), (3, 4)]
            else:
                pairs = [(2, 3), (4, 5)]
            for a, b in pairs:
                r[a], r[b] = r[b], r[a]
            row = r
            rows.append(row[:])
    return rows


def plate_bob(width=928):
    """V. PLAIN BOB MINOR. Six bells, x16x16x16x16x16x12, five leads: sixty
    changes, none rung twice, home to rounds."""
    rows = plain_bob()
    assert rows[-1] == [1, 2, 3, 4, 5, 6] and len({tuple(r) for r in rows[:-1]}) == 60
    dx, dy = 15, 17.5
    colw = 6 * dx
    gapc = 62
    tot = 5 * colw + 4 * gapc
    x0 = (width - tot) / 2
    y0 = 30
    out = []
    for L in range(5):
        cx0 = x0 + L * (colw + gapc)
        out.append(f'<text x="{f(cx0 + colw / 2)}" y="14" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="12.5" fill="{RULE}">lead {L + 1}</text>')
        seg = rows[12 * L: 12 * L + 13]
        out.append(f'<rect x="{f(cx0 - 5)}" y="{f(y0 - 12)}" width="{f(colw + 10)}" height="16" rx="2" fill="{GOLD_PALE}" fill-opacity=".55"/>')
        for bell, col, wdt in ((1, CINNABAR, 1.6), (2, LAPIS, 2.4)):
            pts = [(cx0 + r.index(bell) * dx + dx / 2, y0 + i * dy - 4) for i, r in enumerate(seg)]
            d = 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pts)
            out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{wdt}" stroke-linejoin="round"/>')
        for i, r in enumerate(seg):
            y = y0 + i * dy
            for pos, bell in enumerate(r):
                x = cx0 + pos * dx + dx / 2
                if bell in (1, 2):
                    if i in (0, 12):
                        out.append(f'<circle cx="{f(x)}" cy="{f(y - 4)}" r="2.6" fill="{CINNABAR if bell == 1 else LAPIS}"/>')
                    continue
                out.append(f'<text x="{f(x)}" y="{f(y)}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{TEXT}" fill-opacity=".82">{bell}</text>')
    last_x = x0 + 4 * (colw + gapc) + colw + 10
    out.append(f'<text x="{f(last_x)}" y="{f(y0 + 12 * dy)}" font-family="{SERIF}" font-style="italic" font-size="13" fill="{CINNABAR}">rounds</text>')
    hv = y0 + 12 * dy + 10
    svg = f'<svg viewBox="0 0 {width} {f(hv)}" width="{width}" height="{f(hv)}" role="img" aria-label="Plain Bob Minor, five leads of twelve changes">\n' + '\n'.join(out) + '\n</svg>'
    cap = ('Plain Bob Minor: six bells, each row made from the one before by swapping neighbours, by the rule x 16 x 16 x 16 x 16 x 16 x 12. '
           'Sixty changes, no row rung twice, and home to rounds. The treble in cinnabar; the second’s path in lapis, the blue line a ringer learns. '
           'Nothing in it is left to chance and no two rows are alike: <i>omnia autem honeste et secundum ordinem fiant</i>.')
    return plate_wrap('IX', 'Secundum ordinem', svg, cap, width)


# ---------------------------------------------------------------- colophon
def colophon():
    rows = []
    plates = {0: 'I memoria', 1: 'II rota', 2: 'III fifths', 3: 'IV truchet', 4: 'V two openings', 5: 'VI cell', 6: 'VII tesserae', 7: 'VIII silentium', 8: 'IX plain bob'}
    for i, (file, label, n, word, src, quote) in enumerate(LEAVES):
        rows.append(f'<tr><td>{label}</td><td>{word}</td><td>{NOTE[KEYS[i]]}</td><td>{CUTS[i]}</td><td>{plates.get(i, "")}</td></tr>')
    hashes = []
    for i, (file, label, n, word, src, quote) in enumerate(LEAVES):
        hashes.append(f'<tr><td>{word}</td><td>{src}</td><td>{h12(quote)}</td></tr>')
    extra = [('I', '1 Cor 11:24, Vulg.', 'hoc facite in meam commemorationem'),
             ('II', 'Ez 1:16, Vulg.', 'quasi sit rota in medio rotae'),
             ('VI', 'MD 48', 'lex credendi legem statuat supplicandi'),
             ('VI', 'Jude 3, Vulg.', 'semel traditae sanctis fidei')]
    for num, src, q in extra:
        hashes.append(f'<tr><td>Tab. {num}</td><td>{src}</td><td>{h12(q)}</td></tr>')
    return f'''<div class="colophon">
<p class="lbl" style="color: {{{{rubric}}}}">Colophon · of the illumination</p>
<p class="lat">ex regula, non ex manu</p>
<p class="auct">Nothing on these leaves is painted. Each ornament is computed from a word of its leaf’s own text by a rule set down here, and the same word and the same seed give the same image. The rules are borrowed from the household’s tracks: the gates, the telegraph, the wheels, the divisions, the isorhythm, and the hashes by which a quotation can be checked.</p>
<table class="colo"><tr><th>leaf</th><th>word</th><th>key</th><th>cut</th><th>plate</th></tr>
{chr(10).join(rows)}
</table>
<p class="auct"><b>The gates</b>, in the inner margin: the word in ASCII, eight bits a letter, a filled cell a crossing and an empty one a waiting; it loops. <b>The telegraph</b>, at the head of the frame: the word in Morse, and again down the gutter from the initial. <b>The wheels</b>, at the corners, a wheel in the middle of a wheel: the ring of twelve holds the leaf’s key, its seven notes in gold and the tonic in cinnabar; the ring of four marks the corner’s beat, so the four corners are one bar; one in the middle. The keys go up by fifths and come home, G to B and back to G: my end is my beginning. <b>The divisions</b>, at the foot: the line cut five times and joined five times. <b>The isorhythm</b>, at the sides: a talea of E(k,16), k the letters of the word, carrying the strands in turn, down the left and backwards up the right. <b>The initials</b> stand on their own byte, turned one place a row.</p>
<p class="auct"><b>The seeds.</b> Tabula I takes n. 90: its cursor is on row 90 mod 8, counted from nought. Tabula VII takes n. 93 for its golds, which are loaded dice: xorshift from the seed, so they fall the same way every time. The other figures need none; the rule fixes them.</p>
<p class="auct"><b>The strands.</b> Lapis the prayer, cinnabar the law, gold the given, grey what has passed, ink the text. No figures of people; nothing pictured.</p>
<p class="auct"><b>The parents.</b> Each word keeps the first twelve hex of the sha256 of the words it is quoted from, so it can be checked.</p>
<table class="colo">
{chr(10).join(hashes)}
</table>
</div>'''


# ---------------------------------------------------------------- CSS
BASE_CSS = '''.regula{position:absolute;left:0;top:0;z-index:1;pointer-events:none;overflow:visible}
.tabula{display:flex;flex-direction:column;align-items:center;gap:6px;margin:0 auto}
.tabula svg{display:block;max-width:100%;height:auto}
.auct ~ .tabula, .lbl ~ .tabula{break-inside:avoid;margin:10px auto 14px}
.tab-cap{font-family:'EB Garamond',Georgia,serif;font-style:italic;font-size:13.5px;line-height:1.42;color:#5a4a36;text-align:center;margin:0;max-width:720px}
.droll{flex:1;min-height:0;overflow:hidden;display:flex;align-items:center;justify-content:center}
h2.rub::before,h2.rub::after{margin:0 6px 8px}'''

COLO_CSS = '''.colophon{break-before:column}
.colophon .auct{font-size:14.5px;line-height:1.42;margin-bottom:9px}
table.colo{width:100%;border-collapse:collapse;margin:2px 0 12px;font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.5px;color:#3d2c1c}
table.colo th{font-weight:500;text-align:left;color:#9b2a1a;border-bottom:1px solid #b07a1e;padding:2px 4px}
table.colo td{padding:2px 4px;border-bottom:1px dotted rgba(176,122,30,.5)}'''


def leaf_css(i):
    file, label, n, word, src, quote = LEAVES[i]
    css = [BASE_CSS]
    css.append(f'.lat + .auct:not(.ph)::first-letter{{background:url("{circulant(word[0])}") center/100% 100% no-repeat,linear-gradient(135deg,#f6dd8e 0%,#c9952f 38%,#f8e7ad 55%,#b07a1e 78%,#e9c766 100%) !important}}')
    css.append(f'.ini{{background:url("{circulant("X")}") center/100% 100% no-repeat,linear-gradient(135deg,#f6dd8e 0%,#c9952f 38%,#f8e7ad 55%,#b07a1e 78%,#e9c766 100%)}}')
    tail, hgt = morse_tail(word)
    css.append(f'.ini::after{{border-left:none;left:-15px;top:6px;width:6px;height:{f(hgt)}px;background:url("{tail}") no-repeat}}')
    css.append(f'.ini::before{{left:-16px;top:{f(hgt + 14)}px}}')
    return css


# ---------------------------------------------------------------- apply
def apply(src_dir, dst_dir):
    src_dir, dst_dir = pathlib.Path(src_dir), pathlib.Path(dst_dir)
    sys.path.insert(0, str(pathlib.Path(__file__).parent))
    import auct_plates as AP
    plates = {'Main': plate_refresh(90, 640), 'Folio2': plate_fifths(), 'Folio3': plate_slits(),
              'Folio4': plate_tesserae(93), 'Folio5': plate_bob(),
              'Auct1': AP.plate_rota(), 'Auct2': AP.plate_truchet(), 'Auct3': AP.plate_cell(), 'Auct4': AP.plate_staircase()}
    report = {}
    for i, (file, label, n, word, srcref, quote) in enumerate(LEAVES):
        s = (src_dir / f'{file}.dc.html').read_text()
        n0 = len(s)
        # 1. the vines and the striped bar go; the frame of rules comes in
        s, k1 = re.subn(r'<svg class="corner[^"]*"[^>]*>.*?</svg>\s*', '', s, flags=re.S)
        s, k2 = re.subn(r'<div class="bar" aria-hidden="true"></div>', lambda m: frame(i), s)
        assert k1 == 4 and k2 == 1, (file, k1, k2)
        # 2. the initials' grounds: each its own byte
        css = leaf_css(i)
        ini = re.search(r'<span class="ini"[^>]*>(\w)</span>', s)
        if ini:
            css[2] = f'.ini{{background:url("{circulant(ini.group(1))}") center/100% 100% no-repeat,linear-gradient(135deg,#f6dd8e 0%,#c9952f 38%,#f8e7ad 55%,#b07a1e 78%,#e9c766 100%)}}'
        else:
            css.pop(2); css.pop(2); css.pop(2)
        if file == 'Main':
            css.append(f'.illumbox{{background:url("{phyllo_ground()}") center/cover no-repeat,linear-gradient(135deg,#1b3363,#2f5aa6 50%,#1b3363)}}')
            css.append('.glossa{line-height:1.46}')
        if file == 'Auct5':
            css.append(COLO_CSS)
        s = re.sub(r'(\.bar\{[^\n]*\n)(\.bar::before[^\n]*\n)(\.bar::before\{[^\n]*\n)', '', s)
        s = re.sub(r'\.corner\{[^\n]*\n\.corner\.tl[^\n]*\n\.corner\.bl[^\n]*\n', '', s)
        s = s.replace('</style>', '\n'.join(css) + '\n</style>', 1)
        # 3. the drolleries go; the plates come in
        if file in ('Folio2', 'Folio3', 'Folio4', 'Folio5'):
            s, k3 = re.subn(r'<div class="droll">\s*<svg.*?</svg>\s*</div>', lambda m: f'<div class="droll">\n{plates[file]}\n</div>', s, flags=re.S)
            assert k3 == 1, (file, k3)
        if file == 'Main':
            s, k3 = re.subn(r'(</div>\s*)(</div>\s*)<div class="droll">\s*<svg.*?</svg>\s*</div>\s*',
                            lambda m: m.group(1) + f'<div style="grid-column: 2 / 4; grid-row: 2; align-self: end; padding-top: 14px">\n{plates["Main"]}\n</div>\n\n' + m.group(2) + '\n', s, count=1, flags=re.S)
            assert k3 == 1, (file, k3)
            s, k4 = re.subn(r'(<div style="display: flex; flex-direction: column; gap: 8px; border-right: 1px solid #c9b48a; padding-right: 14px)(">)',
                            r'\1; grid-row: 1 / span 2\2', s, count=1)
            assert k4 == 1
        if file in ('Auct1', 'Auct2', 'Auct3', 'Auct4'):
            s, k6 = re.subn(r'(column-count: 2.*?)(</div>\s*<div style="display: flex; justify-content: space-between; align-items: baseline; border-top)',
                            lambda m: m.group(1) + plates[file] + '\n' + m.group(2), s, count=1, flags=re.S)
            assert k6 == 1, (file, k6)
        if file == 'Auct5':
            s, k5 = re.subn(r'(fideliter serventur libri liturgici</p>\s*<p class="auct">.*?</p>\s*)(</div>)',
                            lambda m: m.group(1) + colophon() + '\n' + m.group(2), s, count=1, flags=re.S)
            assert k5 == 1, ('Auct5', k5)
        (dst_dir / f'{file}.dc.html').write_text(s)
        report[file] = (n0, len(s))
    return report


if __name__ == '__main__':
    for k, v in apply(sys.argv[1], sys.argv[2]).items():
        print(k, v)
