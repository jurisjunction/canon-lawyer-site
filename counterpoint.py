#!/usr/bin/env python3
"""counterpoint.py: the notes of "On These Two Hang", made by rule.

Two rules, both older than the printing press, make every note in the
track's voices; this script is the proof that they were followed, and the
only place the notes come from.

1. Soggetto cavato. Each subject is carved out of its words, as Josquin
   carved the Mass "Hercules Dux Ferrariae" out of a duke's name (Zarlino
   gave the device its name, 1558). Each syllable's vowel picks the
   solmization syllable with the same vowel: u ut, e re, i mi, o sol, and
   a fa, as Josquin read it. The words are the Vulgate's. A stressed
   syllable is a quarter note, an unstressed one an eighth, and the last
   is held to the end of its bar. So the text writes the tune, and it
   writes the thesis too: "Diliges Dominum" and "Diliges proximum" have
   the same vowels, so the two commandments begin with the same notes.
   The second is like unto it.

2. Fux. The voices around each subject are found by search, in the
   strict style of Fux's "Gradus ad Parnassum" (1725): at every half
   note all the voices are consonant (a fourth only between upper
   voices), no two voices move in parallel fifths, octaves or unisons,
   no voice leaps by a tritone or a seventh, a leap turns back by step,
   no voice crosses another. The search is a beam search over the half
   notes, scored by the cost of each motion; the same input gives the
   same notes.

3. Tintinnabuli. Above the subject a second voice keeps to the mode's
   triad (E, G, B): for every note of the melody it takes the nearest
   note of the triad above it. This is the rule Arvo Part has used since
   1976 (a technique, not his notes): a melody that moves by step and a
   voice that never leaves the triad, sounding as one. Here the melody
   is the commandment and the triad voice its light.

The mode is E phrygian, mode III (the mode of the Corpus Christi
"Pange lingua"), white keys only: the family moves up by fifths, and E
is next after A. Solmization is on the natural hexachord, so mi is E,
the mode's own final.

    python3 counterpoint.py            prints every voice as Strudel mini-notation
    python3 counterpoint.py --check    checks that the track quotes them as made

Standard library only. Dedicated to the public domain (CC0 1.0).
"""
import itertools, re, sys
from pathlib import Path

TRACK = Path(__file__).parent / "docs" / "assets" / "music" / "on-these-two-hang.strudel.js"

# ---------------------------------------------------------------- pitch
STEP_PC = [0, 2, 4, 5, 7, 9, 11]                    # white keys, C to B
NAME = "cdefgab"
def midi(w):                                        # white-key index -> midi (w = 7*octave + step, C-1 = 0)
    o, s = divmod(w, 7)
    return 12 * o + STEP_PC[s]
def name(w):
    o, s = divmod(w, 7)
    return f"{NAME[s]}{o - 1}"
def w_of(n):                                        # 'e4' -> white-key index
    return 7 * (int(n[1:]) + 1) + NAME.index(n[0])

# ---------------------------------------------------------------- 1. soggetto cavato
SOLM = {"ut": 0, "re": 1, "mi": 2, "fa": 3, "sol": 4}                # natural hexachord, on C
VOWEL = {"u": "ut", "e": "re", "i": "mi", "a": "fa", "o": "sol"}      # a is fa, as Josquin read it

def vowel(syl):
    s = syl.lower().replace("ae", "e").replace("oe", "e")
    return next(c for c in s if c in VOWEL)

def carve(words, start, bars):
    """words: syllables, stressed ones in capitals. -> [(white-key index, eighths)]"""
    syls = words.split()
    out, prev = [], None
    for syl in syls:
        step = SOLM[VOWEL[vowel(syl)]]
        near = w_of(start) if prev is None else prev   # the nearest octave: the smallest leap
        w = min((7 * o + step for o in range(10)), key=lambda c: (abs(c - near), c))
        out.append([w, 2 if syl[0].isupper() else 1])
        prev = w
    total = sum(d for _, d in out)
    out[-1][1] += 8 * bars - total                  # the last syllable is held to the bar
    assert out[-1][1] >= 1, (words, total)
    return [tuple(x) for x in out]

TEXTS = {
    # Matthew 22:37, 22:39, 27:46, 27:47, 27:54; John 19:30 (Vulgate)
    "DILIGES":  ("DI li ges DO mi num DE um TU um EX TO to COR de TU o", 4),   # Diliges Dominum Deum tuum ex toto corde tuo
    "SIMILE":   ("DI li ges PRO xi mum TU um SI cut te IP sum", 3),           # Diliges proximum tuum sicut teipsum
    "ELI":      ("E li E li LAM ma sa BAC tha ni", 2),                         # Eli, Eli, lamma sabacthani
    "ELIAM":    ("e LI am VO cat IS te", 2),                                   # Eliam vocat iste
    "CONSUMMATUM": ("con sum MA tum EST", 1),                                  # Consummatum est
    "VERE":     ("VE re FI li us DE i E rat IS te", 2),                        # Vere Filius Dei erat iste
}

def transpose(subj, k):                             # by k steps of the mode: like, with a difference
    return [(w + k, d) for w, d in subj]

# ---------------------------------------------------------------- 2. Fux, by search
RANGE = {"S": ("c4", "g5"), "A": ("g3", "d5"), "T": ("c3", "g4"), "B": ("e2", "c4")}
ORDER = "SATB"
CONS = {0, 3, 4, 7, 8, 9}                           # unison/octave, thirds, fifth, sixths
PERFECT = {0, 7}

def ic(a, b):
    return abs(midi(a) - midi(b)) % 12

def sounding(voice, t):
    """The note a fixed voice is holding at eighth t: (w, attacked_now) or None."""
    at = 0
    for w, d in voice:
        if at <= t < at + d:
            return w, at == t
        at += d
    return None

def harmonize(fixed, free, eighths, slot=4, end_perfect=True, carry=None):
    """fixed: {voice: [(w, eighths), ...], w None while it rests}; free: voices to find;
    carry: the last note each free voice sang before, so the line goes on smoothly.
    Returns {voice: [w per slot]} for the free voices, and the cost."""
    slots = list(range(0, eighths, slot))
    cand = {v: list(range(w_of(RANGE[v][0]), w_of(RANGE[v][1]) + 1)) for v in free}
    beam = [((), 0)]
    for i, t in enumerate(slots):
        fixed_now = {v: sounding(s, t) for v, s in fixed.items()}
        fixed_now = {v: x[0] for v, x in fixed_now.items() if x and x[0] is not None}
        nxt = []
        for prefix, cost in beam:
            prev = prefix[-1] if prefix else (tuple(carry[v] for v in free) if carry and all(v in carry for v in free) else None)
            for combo in itertools.product(*(cand[v] for v in free)):
                now = dict(fixed_now); now.update(zip(free, combo))
                c = score(now, prev and dict(zip(free, prev)), prefix, free, fixed, t, i, len(slots), slot, end_perfect)
                if c is not None:
                    nxt.append((prefix + (combo,), cost + c))
        nxt.sort(key=lambda x: x[1])
        beam = nxt[:300]
        if not beam:
            raise SystemExit(f"counterpoint.py: no counterpoint found at eighth {t}")
    best, cost = beam[0]
    return {v: [combo[k] for combo in best] for k, v in enumerate(free)}, cost

def score(now, prev_free, prefix, free, fixed, t, i, n, slot, end_perfect):
    voices = [v for v in ORDER if v in now]
    # no crossing: S above A above T above B
    for hi, lo in zip(voices, voices[1:]):
        if midi(now[hi]) < midi(now[lo]):
            return None
    low = voices[-1]
    cost = 0
    for a, b in itertools.combinations(voices, 2):
        if a in fixed and b in fixed:
            continue                                # the given against the given: not ours to change
        x = ic(now[a], now[b])
        if x == 5 and low not in (a, b):
            pass                                    # a fourth between upper voices
        elif x not in CONS:
            return None
        if x == 0 and midi(now[a]) == midi(now[b]):
            cost += 3                               # a unison: allowed, not loved
    # spacing
    for hi, lo in zip(voices, voices[1:]):
        gap = midi(now[hi]) - midi(now[lo])
        if gap > (19 if lo == low else 12):
            cost += 3
    # the weak eighths inside this slot: a given note that strikes a dissonance must pass by step
    for u in range(t + 1, t + slot):
        for v, s in fixed.items():
            x = sounding(s, u)
            if not x or not x[1] or x[0] is None:
                continue
            w = x[0]
            for f in free:
                if ic(w, now[f]) not in CONS and not passing(s, u):
                    cost += 6
    if prev_free:
        prev_now = {}
        for v in voices:
            if v in fixed:
                x = sounding(fixed[v], t - slot) if t >= slot else None
                if x and x[0] is not None:
                    prev_now[v] = x[0]
            else:
                prev_now[v] = prev_free[v]
        # parallels: perfect to the same perfect, both moving, same direction
        for a, b in itertools.combinations(voices, 2):
            if a in fixed and b in fixed or a not in prev_now or b not in prev_now:
                continue
            p, q = ic(prev_now[a], prev_now[b]), ic(now[a], now[b])
            da, db = now[a] - prev_now[a], now[b] - prev_now[b]
            if p in PERFECT and p == q and da and db and (da > 0) == (db > 0):
                return None
            if q in PERFECT and da and db and (da > 0) == (db > 0) and {a, b} == {voices[0], low} \
                    and abs(now[voices[0]] - prev_now[voices[0]]) > 1:
                cost += 4                           # hidden fifths or octaves in the outer voices
        # melody of each free voice
        for v in free:
            d = now[v] - prev_free[v]
            semis = abs(midi(now[v]) - midi(prev_free[v]))
            if semis in (6, 10, 11) or semis > 12:
                return None                         # tritone, sevenths, more than an octave
            cost += {0: 2, 1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 9, 7: 4}.get(abs(d), 9)
            if len(prefix) >= 2:
                before = prefix[-2][free.index(v)]
                d0 = prev_free[v] - before
                if abs(d0) >= 3 and not (abs(d) == 1 and (d > 0) != (d0 > 0)):
                    cost += 3                       # a leap should turn back by step
    if i == n - 1 and end_perfect:
        for v in free:
            if ic(now[v], now[low]) not in PERFECT and v != low:
                cost += 2                           # the last chord leans to fifths and octaves
    return cost

def passing(voice, t):
    """Is the given note struck at t approached and left by step?"""
    at, notes = 0, []
    for w, d in voice:
        notes.append((at, w)); at += d
    for k, (a, w) in enumerate(notes):
        if a == t:
            before = notes[k - 1][1] if k else None
            after = notes[k + 1][1] if k + 1 < len(notes) else None
            return None not in (w, before, after) and abs(w - before) == 1 and abs(after - w) == 1
    return False

# ---------------------------------------------------------------- the sections
def subjects():
    S = {k: carve(words, "e4", bars) for k, (words, bars) in TEXTS.items()}
    return S

def section_exposition(subj, entries):
    """entries: [(voice, transposition)], one statement after another; each new
    statement adds a voice and the voices already in go on in free counterpoint."""
    bars = sum(d for _, d in subj) // 8
    out = {v: [] for v in ORDER}
    for k, (voice, shift) in enumerate(entries):
        given = transpose(subj, shift)
        free = [v for v, _ in entries[:k]]
        free = [v for v in ORDER if v in free]
        carry = {v: [w for w, _ in out[v] if w is not None][-1] for v in free}
        found, _ = harmonize({voice: given}, free, 8 * bars, carry=carry) if free else ({}, 0)
        for v in ORDER:
            if v == voice:
                out[v] += given
            elif v in found:
                out[v] += [(w, 4) for w in found[v]]
            else:
                out[v] += [(None, 8 * bars)]
    return out

def octave(subj, k):
    """The same notes, k octaves up or down."""
    return transpose(subj, 7 * k)

def section_combined(S1, S2):
    """Both commandments at once: S1 in the bass, S2 above, a bar later, so that they end together;
    the alto and tenor between them are found by search."""
    s1 = octave(S1, -1)
    best = None
    for level, offset in itertools.product((0, 4, 3, 5, 7, 2), (8, 4, 0)):
        s2 = [(None, offset)] * bool(offset) + transpose(S2, level) + [(None, 8 - offset)] * bool(8 - offset)
        try:
            found, cost = harmonize({"B": s1, "S": s2rest(s2)}, ["A", "T"], 32)
        except SystemExit:
            continue
        clash = clashes(s1, s2rest(s2))
        if best is None or (clash, -offset, cost) < best[0]:
            best = ((clash, -offset, cost), level, s2, found)
    _, level, s2, found = best
    return {"S": s2, "A": [(w, 4) for w in found["A"]], "T": [(w, 4) for w in found["T"]], "B": s1}, level

def s2rest(s):
    """A voice with a leading rest, for sounding(): the rest is a held None, skipped."""
    return [(w, d) for w, d in s]

def clashes(a, b):
    n = 0
    for t in range(0, 32, 4):
        x, y = sounding(a, t), sounding(b, t)
        if x and y and x[0] is not None and y[0] is not None and ic(x[0], y[0]) not in CONS:
            n += 1
    return n

def section_refrain(R, voices):
    """The centurion's line on top and the voices beneath it, one voice more each time (Figaro's finale)."""
    given = octave(R, 1)
    top = voices[0]
    free = voices[1:]
    found, _ = harmonize({top: given}, free, 16, slot=2) if free else ({}, 0)
    out = {top: given}
    for v in free:
        out[v] = [(w, 2) for w in found[v]]
    return out

# ---------------------------------------------------------------- 3. tintinnabuli
TRIAD = {2, 4, 6}                                   # E, G, B (white-key steps)

def tintinnabuli(seq, floor="e5"):
    """The triad voice: for each note, the nearest triad note above it, then raised by
    octaves so the voice starts at or above floor. Rests stay rests."""
    out, k = [], None
    for w, d in seq:
        if w is None:
            out.append((None, d)); continue
        t = w + 1
        while t % 7 not in TRIAD:
            t += 1
        if k is None:
            k = 0
            while t + 7 * k < w_of(floor):
                k += 1
        out.append((t + 7 * k, d))
    return out

def statements(subj, entries):
    """The subject as it enters, statement by statement: the melody the triad voice follows."""
    seq = []
    for _, shift in entries:
        seq += tintinnabuli(transpose(subj, shift))
    return seq

# ---------------------------------------------------------------- the audit
def audit(section, slot=4):
    """Every rule at every half note, for every pair of voices, the given included.
    Returns a list of findings; the given against the given is reported as such."""
    voices = [v for v in ORDER if v in section]
    span = max(sum(d for _, d in section[v]) for v in voices)
    found, last = [], None
    for t in range(0, span, slot):
        now = {}
        for v in voices:
            x = sounding(section[v], t)
            if x and x[0] is not None:
                now[v] = x[0]
        order = [v for v in voices if v in now]
        low = order[-1] if order else None
        for a, b in itertools.combinations(order, 2):
            x = ic(now[a], now[b])
            if x not in CONS and not (x == 5 and low not in (a, b)):
                found.append(f"eighth {t}: {a}-{b} {name(now[a])}/{name(now[b])} dissonant")
            if midi(now[a]) < midi(now[b]):
                found.append(f"eighth {t}: {a} below {b}")
            if last and a in last and b in last:
                p, q = ic(last[a], last[b]), x
                da, db = now[a] - last[a], now[b] - last[b]
                if p in PERFECT and p == q and da and db and (da > 0) == (db > 0):
                    found.append(f"eighth {t}: {a}-{b} parallel {'octaves' if p == 0 else 'fifths'}")
        last = now
    for v in voices:
        notes = [w for w, _ in section[v] if w is not None]
        for x, y in zip(notes, notes[1:]):
            semis = abs(midi(y) - midi(x))
            if semis in (6, 10, 11) or semis > 12:
                found.append(f"{v}: leap {name(x)}-{name(y)}")
    return found

# ---------------------------------------------------------------- mini-notation
def mini(seq):
    toks = []
    for w, d in seq:
        toks.append(("~" if w is None else name(w)) + (f"@{d}" if d != 1 else ""))
    return " ".join(toks)

def build():
    S = subjects()
    lines, findings = {}, {}
    for k in S:
        lines[k] = mini(S[k])
    # the left wing: "Diliges Dominum", four entries, alto first, the answer a fifth up
    entries1 = [("A", 0), ("S", 4), ("T", -7), ("B", -10)]
    exp1 = section_exposition(S["DILIGES"], entries1)
    lines["DILIGES_TIN"] = mini(statements(S["DILIGES"], entries1))
    for v in ORDER:
        lines[f"DILIGES_{v}"] = mini(exp1[v])
    findings["DILIGES"] = audit(exp1)
    # the second wing: "Diliges proximum", the same head, entering from the bass up
    exp2 = section_exposition(S["SIMILE"], [("B", -7), ("T", -3), ("A", 0), ("S", 4)])
    for v in ORDER:
        lines[f"SIMILE_{v}"] = mini(exp2[v])
    findings["SIMILE"] = audit(exp2)
    comb, level = section_combined(S["DILIGES"], S["SIMILE"])
    lines["DUOBUS_TIN"] = mini(tintinnabuli(comb["S"]))
    for v in ORDER:
        lines[f"DUOBUS_{v}"] = mini(comb[v])
    findings["DUOBUS"] = audit(comb)
    for k, voices in (("SOLO", "S"), ("DUO", "SB"), ("TRIO", "SAB"), ("TUTTI", "SATB")):
        ref = section_refrain(S["VERE"], list(voices))
        for v in voices:
            lines[f"VERE_{k}_{v}"] = mini(ref[v])
        findings[f"VERE_{k}"] = audit(ref, slot=2)
    lines["VERE_TIN"] = mini(tintinnabuli(octave(S["VERE"], 1), floor="g5"))
    return lines, findings

def main():
    lines, findings = build()
    for sec, f in findings.items():
        print(f"// audit {sec}: " + ("every half note keeps the rules" if not f else "; ".join(f)), file=sys.stderr)
    if "--check" in sys.argv:
        src = TRACK.read_text(encoding="utf-8")
        bad = [k for k, v in lines.items() if not re.search(rf"^const {k} = '{re.escape(v)}'", src, re.M)]
        if bad:
            sys.exit("counterpoint.py: the track does not quote these as made: " + ", ".join(bad))
        print(f"counterpoint.py: {len(lines)} lines, each carved or found by rule, quoted as made")
        return
    for k, v in lines.items():
        print(f"const {k} = '{v}'")

if __name__ == "__main__":
    main()
