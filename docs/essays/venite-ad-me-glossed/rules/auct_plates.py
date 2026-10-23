"""The four plates of the auctoritates leaves (imported by illum.py)."""
import math
from illum import (euclid, bits, f, plate_wrap, INK, TEXT, LAPIS, CINNABAR, GOLD, GOLD_LT,
                   GOLD_PALE, GOLD_DK, RULE, MATTER, MONO, SERIF)


def plate_rota(num='II', width=420):
    """THE WHEEL: rings of 16, 12, 8 and 4 steps, each E(k,n), spokes to the hub."""
    c = width / 2
    rings = [(16, 7, 186, GOLD), (12, 5, 140, LAPIS), (8, 3, 94, CINNABAR), (4, 1, 50, GOLD)]
    out, spokes = [], []
    for n, k, r, col in rings:
        out.append(f'<circle cx="{f(c)}" cy="{f(c)}" r="{r}" fill="none" stroke="{RULE}" stroke-width=".9"/>')
        for i, on in enumerate(euclid(k, n)):
            a = math.radians(-90 + 360 * i / n)
            x, y = c + r * math.cos(a), c + r * math.sin(a)
            if on:
                spokes.append(f'<line x1="{f(c)}" y1="{f(c)}" x2="{f(x)}" y2="{f(y)}" stroke="{RULE}" stroke-opacity=".55" stroke-width=".8"/>')
                out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="7" fill="{col}" stroke="{GOLD_DK}" stroke-width=".8"/>')
            else:
                out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="2" fill="{INK}" fill-opacity=".55"/>')
        out.append(f'<text x="{f(c + 6)}" y="{f(c - r + 15)}" font-family="{MONO}" font-size="9" fill="{RULE}">E({k},{n})</text>')
    out.append(f'<circle cx="{f(c)}" cy="{f(c)}" r="13" fill="none" stroke="{CINNABAR}" stroke-width="1.4"/>')
    out.append(f'<circle cx="{f(c)}" cy="{f(c)}" r="7.5" fill="{GOLD}" stroke="{GOLD_DK}" stroke-width=".8"/>')
    svg = (f'<svg viewBox="0 0 {width} {width}" width="{width}" height="{width}" role="img" aria-label="nested Euclidean rings with spokes to the hub">\n'
           + '\n'.join(spokes + out) + '\n</svg>')
    cap = ('<i>Quasi sit rota in medio rotae</i> (Ez 1:16, Vulgate). Rings of sixteen, twelve, eight and four steps, each with its strokes '
           'spread as evenly as they can be, and one in the middle. Every spoke runs to the hub and runs from it: <i>culmen et fons</i> (SC 10).')
    return plate_wrap(num, 'Rota in medio rotae', svg, cap, width)


def plate_truchet(num='IV', width=420, word='APTATIO'):
    """ONE TILE, FOUR LAWS: a Truchet tile laid all alike, by row and column,
    by the diagonals, and by the bits of the word."""
    t = 29
    n = 6
    pw = n * t
    gap = (width - 2 * pw) / 1
    stream = ''.join(bits(word))
    rules = [('all alike', lambda i, j, q: 0),
             ('by row and column', lambda i, j, q: 2 * (i % 2) + (j % 2)),
             ('by the diagonals', lambda i, j, q: 0 if (i + j) % 2 == 0 else 2),
             (f'by the bits of {word}', lambda i, j, q: int(stream[(2 * q) % len(stream)] + stream[(2 * q + 1) % len(stream)], 2))]
    out = []
    for p, (lab, rule) in enumerate(rules):
        ox = (p % 2) * (pw + gap)
        oy = (p // 2) * (pw + 40)
        for i in range(n):
            for j in range(n):
                q = i * n + j
                o = rule(i, j, q)
                x, y = ox + j * t, oy + i * t
                corners = [(x, y), (x + t, y), (x + t, y + t), (x, y + t)]
                a, b, cc = corners[o], corners[(o + 1) % 4], corners[(o + 3) % 4]
                out.append(f'<rect x="{f(x)}" y="{f(y)}" width="{t}" height="{t}" fill="{GOLD_LT}"/>')
                out.append(f'<path d="M {f(a[0])} {f(a[1])} L {f(b[0])} {f(b[1])} L {f(cc[0])} {f(cc[1])} Z" fill="{LAPIS}"/>')
        out.append(f'<rect x="{f(ox)}" y="{f(oy)}" width="{pw}" height="{pw}" fill="none" stroke="{GOLD_DK}" stroke-width="1.2"/>')
        out.append(f'<text x="{f(ox + pw / 2)}" y="{f(oy + pw + 17)}" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{INK}">{lab}</text>')
    hv = 2 * pw + 40 + 24
    svg = (f'<svg viewBox="0 0 {width} {hv}" width="{width}" height="{hv}" role="img" aria-label="one Truchet tile laid by four rules">\n'
           + '\n'.join(out) + '\n</svg>')
    cap = ('One tile, half lapis and half gold, laid by four laws: all alike; turned by row and column; turned by the diagonals; '
           f'turned by the bits of {word}, two at a time. The tile is never altered, only the law of its laying. '
           'Not a rigid uniformity, and still one tile (SC 37–38).')
    return plate_wrap(num, 'Aptatio', svg, cap, width)


def plate_cell(num='VI', width=420):
    """A MEMORY CELL: two buffers in a ring, each feeding the other. Pushed
    once on CREDENDI, SUPPLICANDI follows a step later, and both stay."""
    out = []
    L, R_ = 70, width - 70
    yt, yb = 62, 150
    ym = (yt + yb) / 2

    def buf(x, y, right=True, s=34):
        if right:
            d = f'M {f(x - s / 2)} {f(y - s / 2)} L {f(x + s / 2)} {f(y)} L {f(x - s / 2)} {f(y + s / 2)} Z'
        else:
            d = f'M {f(x + s / 2)} {f(y - s / 2)} L {f(x - s / 2)} {f(y)} L {f(x + s / 2)} {f(y + s / 2)} Z'
        return f'<path d="{d}" fill="{GOLD_PALE}" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/>'
    mx = width / 2
    wire = f'stroke="{INK}" stroke-width="1.4" fill="none"'
    out.append(f'<path d="M {L} {f(ym)} L {L} {yt} L {f(mx - 17)} {yt} M {f(mx + 17)} {yt} L {R_} {yt} L {R_} {f(ym)}" {wire}/>')
    out.append(f'<path d="M {R_} {f(ym)} L {R_} {yb} L {f(mx + 17)} {yb} M {f(mx - 17)} {yb} L {L} {yb} L {L} {f(ym)}" {wire}/>')
    out.append(buf(mx, yt, True))
    out.append(buf(mx, yb, False))
    out.append(f'<text x="{f(mx)}" y="{yt - 24}" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="12.5" fill="{RULE}">Indiculus 8: statuat</text>')
    out.append(f'<text x="{f(mx)}" y="{yb + 34}" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="12.5" fill="{RULE}">Mediator Dei 48: statuat</text>')
    for x, lab, col, anc, dx in ((L, 'SUPPLICANDI', LAPIS, 'start', 10), (R_, 'CREDENDI', GOLD_DK, 'end', -10)):
        out.append(f'<circle cx="{x}" cy="{f(ym)}" r="6" fill="{GOLD}" stroke="{GOLD_DK}" stroke-width=".8"/>')
        out.append(f'<text x="{x + dx}" y="{f(ym + 4)}" text-anchor="{anc}" font-family="{MONO}" font-size="10" fill="{col}">{lab}</text>')
    # the push, into CREDENDI from the right
    out.append(f'<path d="M {R_ + 46} {f(ym)} L {R_ + 9} {f(ym)} M {R_ + 16} {f(ym - 5)} L {R_ + 9} {f(ym)} L {R_ + 16} {f(ym + 5)}" stroke="{CINNABAR}" stroke-width="1.4" fill="none"/>')
    out.append(f'<text x="{R_ + 28}" y="{f(ym - 10)}" text-anchor="middle" font-family="{MONO}" font-size="9" fill="{CINNABAR}">push</text>')
    # the timing: sixteen steps
    tx0, tx1 = 92, width - 12
    st = (tx1 - tx0) / 16
    rows = [('push', CINNABAR, lambda s: 1 if s == 2 else 0),
            ('credendi', GOLD_DK, lambda s: 1 if s >= 2 else 0),
            ('supplicandi', LAPIS, lambda s: 1 if s >= 3 else 0)]
    ty = 222
    for s in range(17):
        x = tx0 + s * st
        out.append(f'<line x1="{f(x)}" y1="{ty - 18}" x2="{f(x)}" y2="{ty + 3 * 30 - 14}" stroke="{RULE}" stroke-opacity=".35" stroke-width=".6"/>')
    for r, (lab, col, fn) in enumerate(rows):
        y = ty + r * 30
        out.append(f'<text x="{tx0 - 8}" y="{y + 2}" text-anchor="end" font-family="{MONO}" font-size="9.5" fill="{col}">{lab}</text>')
        pts, prev = [], None
        for s in range(16):
            v = fn(s)
            yy = y - 12 * v + 6
            x = tx0 + s * st
            if prev is not None and prev != yy:
                pts.append((x, prev))
            pts.append((x, yy))
            pts.append((x + st, yy))
            prev = yy
        d = 'M' + ' L'.join(f'{f(px)} {f(py)}' for px, py in pts)
        out.append(f'<path d="{d}" stroke="{col}" stroke-width="1.8" fill="none" stroke-linejoin="round"/>')
    hv = ty + 3 * 30 - 6
    svg = (f'<svg viewBox="0 0 {width} {hv}" width="{width}" height="{hv}" role="img" aria-label="two buffers in a ring holding one bit">\n'
           + '\n'.join(out) + '\n</svg>')
    cap = ('Two buffers in a ring, each feeding the other: the Indiculus has the law of praying establish the law of believing, '
           'Mediator Dei 48 has the law of believing establish the law of praying. A cell like this holds its bit only because each half keeps '
           'telling the other what it is. Pushed once, on <i>credendi</i>, the other follows a step later and both stay: <i>semel traditae sanctis fidei</i> (Jude 3).')
    return plate_wrap(num, 'Semel tradita', svg, cap, width)


def plate_staircase(num='VIII', width=420, mark=9):
    """EVERY RHYTHM OF SIXTEEN: E(k,16), k = 0 to 16. The first row is silence;
    the row of the leaf's word (its letters) is the talea at its sides."""
    cell = 19.5
    x0, y0 = 46, 4
    out = []
    for k in range(17):
        y = y0 + k * cell
        pat = euclid(k, 16)
        if k == 0:
            out.append(f'<rect x="{f(x0 - 3)}" y="{f(y - 2)}" width="{f(16 * cell + 3)}" height="{f(cell + 1)}" rx="2" fill="{GOLD_PALE}" fill-opacity=".7" stroke="{GOLD}" stroke-width="1"/>')
        if k == mark:
            out.append(f'<rect x="{f(x0 - 3)}" y="{f(y - 2)}" width="{f(16 * cell + 3)}" height="{f(cell + 1)}" rx="2" fill="none" stroke="{CINNABAR}" stroke-width="1.3"/>')
        out.append(f'<text x="{x0 - 10}" y="{f(y + cell / 2 + 3)}" text-anchor="end" font-family="{MONO}" font-size="9.5" fill="{CINNABAR if k == mark else INK}">{k}</text>')
        for i, on in enumerate(pat):
            x = x0 + i * cell
            if on:
                out.append(f'<rect x="{f(x + 1.5)}" y="{f(y + 1.5)}" width="{f(cell - 4)}" height="{f(cell - 4)}" rx="1.5" fill="{LAPIS}"/>')
            else:
                out.append(f'<circle cx="{f(x + cell / 2 - .5)}" cy="{f(y + cell / 2 - .5)}" r="2.2" fill="none" stroke="{INK}" stroke-opacity=".45" stroke-width=".8"/>')
    out.append(f'<text x="{f(x0 + 16 * cell + 6)}" y="{f(y0 + cell / 2 + 3)}" font-family="{SERIF}" font-style="italic" font-size="12" fill="{GOLD_DK}">silentium</text>')
    out.append(f'<text x="{f(x0 + 16 * cell + 6)}" y="{f(y0 + mark * cell + cell / 2 + 3)}" font-family="{SERIF}" font-style="italic" font-size="12" fill="{CINNABAR}">this leaf</text>')
    wv = width
    hv = y0 + 17 * cell + 4
    svg = (f'<svg viewBox="0 0 {wv} {f(hv)}" width="{wv}" height="{f(hv)}" role="img" aria-label="every Euclidean rhythm of sixteen steps">\n'
           + '\n'.join(out) + '\n</svg>')
    cap = ('Every rhythm of sixteen steps, from no stroke to sixteen, each spreading its strokes as evenly as it can among its rests. '
           f'The first row is all silence; row {mark}, for the {mark} letters of SILENTIUM, is the talea at the sides of this leaf. '
           '<i>Suo quoque tempore sacrum silentium servetur</i> (SC 30).')
    return plate_wrap(num, 'Silentium', svg, cap, width)
