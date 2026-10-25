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
    python3 counterpoint.py --ly PATH  writes the choir's part as a LilyPond score, SATB
    python3 counterpoint.py --midi DIR writes it as MIDI: a file to a voice, and one for all four

The score and the MIDI are written from the same lines, laid out bar for bar as the
track arranges them, and only if the track quotes every line as made.

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

def build(keep=None):
    """Every line, as mini-notation, and the audit of each section. If keep is a dict,
    the sections themselves go in it too, for the score and the MIDI."""
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
    entries2 = [("B", -7), ("T", -3), ("A", 0), ("S", 4)]
    exp2 = section_exposition(S["SIMILE"], entries2)
    lines["SIMILE_TIN"] = mini(statements(S["SIMILE"], entries2))
    for v in ORDER:
        lines[f"SIMILE_{v}"] = mini(exp2[v])
    findings["SIMILE"] = audit(exp2)
    comb, level = section_combined(S["DILIGES"], S["SIMILE"])
    lines["DUOBUS_TIN"] = mini(tintinnabuli(comb["S"]))
    for v in ORDER:
        lines[f"DUOBUS_{v}"] = mini(comb[v])
    findings["DUOBUS"] = audit(comb)
    refrains = {}
    for k, voices in (("SOLO", "S"), ("DUO", "SB"), ("TRIO", "SAB"), ("TUTTI", "SATB")):
        ref = refrains[k] = section_refrain(S["VERE"], list(voices))
        for v in voices:
            lines[f"VERE_{k}_{v}"] = mini(ref[v])
        findings[f"VERE_{k}"] = audit(ref, slot=2)
    lines["VERE_TIN"] = mini(tintinnabuli(octave(S["VERE"], 1), floor="g5"))
    if keep is not None:
        keep.update(subjects=S, DILIGES=(exp1, entries1), SIMILE=(exp2, entries2),
                    DUOBUS=comb, VERE=refrains)
    return lines, findings

# ---------------------------------------------------------------- 4. the score and the MIDI
# The choir's part of the track, bar for bar, for people to sing: a LilyPond score
# (--ly) and Standard MIDI Files (--midi). Nothing is typed twice. The notes are
# build()'s, and the order of the parts and their lengths are read from the track.

WORDS = {   # the words of TEXTS as words, so the underlay knows where each one ends
    "DILIGES": "Diliges Dominum Deum tuum ex toto corde tuo",
    "SIMILE": "Diliges proximum tuum sicut teipsum",
    "ELI": "Eli, Eli, lamma sabacthani",
    "ELIAM": "Eliam vocat iste",
    "CONSUMMATUM": "Consummatum est",
    "VERE": "Vere Filius Dei erat iste",
}
VOICE = {"S": "Soprano", "A": "Alto", "T": "Tenor", "B": "Bass"}
ROMAN = "I II III IV V VI VII VIII IX X".split()
GOLGOTHA = {   # what is written over each part of Golgotha
    "dark": "darkness: the clock alone",
    "cry": "Solo: the cry",
    "elias": "Sopranos: the crowd",
    "finished": "Solo",
    "rent": "the veil and the earth",
    "centurion": "Solo: the centurion",
    "silence": "the tomb",
}
FREE = "free voices: text to be set"

def underlay(key):
    """The syllables of a subject as they are sung, one to a note: [(syllable, word goes on)]."""
    syls, out = TEXTS[key][0].split(), []
    for word in WORDS[key].split():
        letters, got = re.sub(r"[^A-Za-z]", "", word).lower(), []
        while "".join(got).lower() != letters:
            assert len(out) + len(got) < len(syls), (key, word)
            got.append(syls[len(out) + len(got)])
        at = 0
        for k, s in enumerate(got):
            last = k == len(got) - 1
            out.append((word[at:] if last else word[at:at + len(s)], not last))
            at += len(s)
    assert len(out) == len(syls), key
    return out

def octave_marks(o):                                # c4 is c' in LilyPond
    return "'" * (o - 3) if o >= 3 else "," * (3 - o)

def pitch(w):                                       # white-key index -> (midi, LilyPond name)
    return None if w is None else (midi(w), NAME[w % 7] + octave_marks(w // 7 - 1))

def pitch_of(n):                                    # 'g#3' -> (midi, 'gis')
    m = re.fullmatch(r"([a-g])(#|b)?(\d)", n)
    acc = m.group(2) or ""
    return (12 * (int(m.group(3)) + 1) + STEP_PC[NAME.index(m.group(1))] + {"#": 1, "b": -1, "": 0}[acc],
            m.group(1) + {"#": "is", "b": "es", "": ""}[acc] + octave_marks(int(m.group(3))))

def arrangement(src, const=None):
    """The [bars, part] items of one of the track's arrange(...) calls (the last one, if no const)."""
    head = rf"^const {const} = (?:stack\()?arrange\(" if const else r"^arrange\("
    block = re.search(head + r"(.*?)\n\)", src, re.S | re.M).group(1)
    items = []
    for m in re.finditer(r"\[(\d+),\s*", block):
        part = next(t for t in re.findall(r"[A-Za-z_]\w*", block[m.end():]) if t not in ("stack", "satb", "note"))
        items.append((int(m.group(1)), part))
    return items

def chunks(notes, size):
    """A voice cut into its statements, size eighths each."""
    out, cur, at = [], [], 0
    for w, d in notes:
        cur.append((w, d)); at += d
        if at % size == 0:
            out.append(cur); cur = []
    assert not cur
    return out

def piece():
    """The choir's part of the whole track, from its first bar. Returns the events of each
    voice, [time, pitch or None, eighths, (syllable, word goes on) or None, words over it],
    the sections as (time, name), the parts as (start, end), and the repeats as
    (start, end of the first time, end of the second); time is in eighths."""
    keep = {}
    lines, findings = build(keep)
    if any(findings.values()) or unquoted(lines):
        raise SystemExit("counterpoint.py: the lines break a rule or the track does not quote them as made; run --check")
    src = TRACK.read_text(encoding="utf-8")
    S, refrains, comb = keep["subjects"], keep["VERE"], keep["DUOBUS"]
    sung = {"ELI": (S["ELI"], "ELI"), "ELIAM": (S["ELIAM"], "ELIAM"), "CONSUMMATUM": (S["CONSUMMATUM"], "CONSUMMATUM"),
            "VERE_SOLO_S": (refrains["SOLO"]["S"], "VERE")}
    voices, sections, parts, repeats = {v: [] for v in ORDER}, [], [], []
    clock, marked = 0, False

    def part(bars, lines, over=None, free=False):
        """One stretch of the track. lines: {voice: (notes, TEXTS key or None)}; the others are silent."""
        nonlocal clock, marked
        for v in ORDER:
            seq, key = lines.get(v, ([(None, 8 * bars)], None))
            assert sum(d for _, d in seq) == 8 * bars, (v, bars)
            syls, t, first = iter(underlay(key) if key else ()), clock, True
            for p, d in seq:
                words = None
                if first and over and over[0] == v:
                    words = over[1]
                elif free and p is not None and not key and not marked:
                    words, marked = FREE, True
                voices[v].append([t, p, d, next(syls) if p is not None and key else None, words])
                t, first = t + d, False
            assert next(syls, None) is None, key
        parts.append((clock, clock + 8 * bars))
        clock += 8 * bars
        return tuple((v,) + tuple(lines[v]) for v in ORDER if v in lines)

    def notes(seq):
        return [(pitch(w), d) for w, d in seq]

    for n, (bars, sec) in enumerate(arrangement(src)):
        start = clock
        sections.append((clock, f"{ROMAN[n]}. {sec[3:].title()}"))
        if sec in ("secDILIGES", "secSIMILE"):          # the expositions, a statement at a time
            key = sec[3:]
            exp, entries = keep[key]
            size = sum(d for _, d in S[key])
            cut = {v: chunks(exp[v], size) for v in ORDER}
            for k, (who, _) in enumerate(entries):
                part(size // 8, {v: (notes(cut[v][k]), key if v == who else None) for v in ORDER}, free=True)
        elif sec == "secGOLGOTHA":                      # the solo lines, between silences
            for b, p in arrangement(src, "secGOLGOTHA"):
                body = re.search(rf"^const {p} = (.*)$", src, re.M)
                line = next((x for x in re.findall(r"\b[A-Z][A-Z_]+\b", body.group(1)) if x in sung), None) if body else None
                part(b, {"S": (notes(sung[line][0]), sung[line][1])} if line else {}, over=("S", GOLGOTHA[p]))
        elif sec == "secVERE":                          # the centurion's line, a voice more each time
            for b, p in arrangement(src, "secVERE"):
                ref = refrains[p.split("_")[1]]
                size = sum(d for _, d in ref["S"]) // 8
                for _ in range(b // size):
                    part(size, {v: (notes(ref[v]), "VERE" if v == "S" else None) for v in ref}, free=True)
        elif sec == "secDUOBUS":                        # both subjects at once; sung again, a repeat
            last = None
            for b, p in arrangement(src, "secDUOBUS"):
                was = clock
                same = part(b, {"S": (notes(comb["S"]), "SIMILE"), "A": (notes(comb["A"]), None),
                                "T": (notes(comb["T"]), None), "B": (notes(comb["B"]), "DILIGES")}, free=True)
                if same == last:
                    repeats.append((was - 8 * b, was, clock))
                last = same
        elif sec == "secAMEN":                          # the phrygian cadence, a note to a voice
            for b, p in arrangement(src, "secAMEN"):
                chord = re.search(rf'\b{p} = "\[(.*?)\]"', src)
                part(b, {v: ([(pitch_of(x), 8 * b)], None) for v, x in zip("BTAS", chord.group(1).split(","))} if chord else {})
        else:                                           # the instruments alone: the choir is silent
            part(bars, {})
        assert clock - start == 8 * bars, (sec, (clock - start) / 8, bars)
    return voices, sections, parts, repeats

# ---------------------------------------------------------------- the score, in LilyPond
DUR = {1: "8", 2: "4", 3: "4.", 4: "2", 6: "2.", 7: "2..", 8: "1"}   # eighths -> LilyPond

def fits(o, n):
    """May a note of n eighths stand as one sign at eighth o of the bar? Not across the bar
    line, and not across the middle of the bar unless it starts on a beat, or is the
    quarter of a syncopation (eighth, quarter, eighth)."""
    return n in DUR and o + n <= 8 and (o == 0 or o + n <= 4 or o >= 4 or (o == 2 and n in (4, 6)) or n == 2)

def sign(t, n, rest=False):
    """The first sign of a note (or rest) of n eighths from eighth t; the rest is tied on."""
    o = t % 8
    return max(k for k in range(1, min(n, 8 - o) + 1) if (o % k == 0 and k in (1, 2, 4, 8) if rest else fits(o, k)))

def ly_text(s):
    return '"' + s.replace('"', "'") + '"'

def ly_voice(events, sections, repeats, edges):
    """One voice's notes, a bar to a line, with a comment at the head of each section;
    repeats: (start, end); edges: where the whole choir falls silent or comes back."""
    out, heads = [], dict(sections)
    opens, closes = {a for a, _ in repeats}, {b for _, b in repeats}
    merged = []                                     # rests that follow each other, as one
    for e in events:
        if merged and e[1] is None and merged[-1][1] is None and not e[4] \
                and e[0] not in heads and e[0] not in opens and e[0] not in closes and e[0] not in edges:
            merged[-1] = merged[-1][:2] + [merged[-1][2] + e[2]] + merged[-1][3:]
        else:
            merged.append(list(e))
    for t, p, d, _, words in merged:
        if t in heads:
            out.append(f"\n  % {heads[t]}\n ")
        if t in opens:
            out.append(" \\repeat volta 2 {")
        at, left = t, d
        while left:
            if p is None and at % 8 == 0 and left >= 8:
                n = 8 * (left // 8)
                tok = "R1" + (f"*{n // 8}" if n > 8 else "")
            else:
                n = sign(at, left, rest=p is None)
                tok = ("r" if p is None else p[1]) + DUR[n]
            if at == t and words:
                tok += f"^\\markup \\small \\italic {ly_text(words)}"
            out.append(" " + tok + ("~" if p is not None and n < left else ""))
            at, left = at + n, left - n
            if at % 8 == 0:
                out.append(" |\n ")
        if t + d in closes:
            out.append(" }")
    return "".join(out).rstrip()

def ly_words(events):
    out, skip = [], 0
    for _, p, _, syl, _ in events:
        if p is None:
            continue
        if syl is None:
            skip += 1; continue
        if skip:
            out.append(f"\\repeat unfold {skip} {{ \\skip 1 }}"); skip = 0
        out.append(ly_text(syl[0]) + (" --" if syl[1] else ""))
    if skip:
        out.append(f"\\repeat unfold {skip} {{ \\skip 1 }}")
    lines, cur = [], []
    for tok in out:                                     # a line of text to a line of the file
        cur.append(tok)
        if not tok.endswith("--") and (tok.strip('"').endswith(",") or len(" ".join(cur)) > 70 or tok.startswith("\\repeat")):
            lines.append(" ".join(cur)); cur = []
    return "\n  ".join(lines + [" ".join(cur)] if cur else lines)

def write_ly(path, voices, sections, parts, repeats):
    """The score: from the first sung note to the last, a repeat written once. The bar
    numbers and the times over the sections are the track's."""
    sung = [(t, t + d) for v in ORDER for t, p, d, *_ in voices[v] if p is not None]
    first, end = min(a for a, _ in sung), max(b for _, b in sung)
    gone = [(b, c) for _, b, c in repeats]               # the second time, not written again
    def at(t):
        return t - sum(c - b for b, c in gone if t >= c)
    def shown(t):
        return first <= t < end and not any(b <= t < c for b, c in gone)
    keep = {v: [[at(t)] + e for t, *e in voices[v] if shown(t)] for v in ORDER}
    heads = [(at(t), name, t) for t, name in sections if shown(t)]
    quiet = [(at(a), at(b)) for a, b in parts if shown(a)
             and all(p is None for v in ORDER for t, p, *_ in voices[v] if a <= t < b)]
    loops = [(at(a), at(b)) for a, b, _ in repeats]
    marks = [(at(first), 1, f"\\tempo 4 = 120 \\set Score.currentBarNumber = #{first // 8 + 1}")]
    for t, name, real in heads:
        num, title = name.split(" ", 1)
        bar, sec = real // 8 + 1, (real // 8) * 2
        label = (f"\\sectionLabel \\markup \\line {{ \\bold {ly_text(num + ' ' + title)} "
                 f"\\hspace #2 \\italic {ly_text(f'bar {bar} ({sec // 60}:{sec % 60:02d})')} }}")
        marks.append((t, 2, ("\\section " if t > at(first) else "") + label))
    for a, b in quiet:
        marks += [(a, 1, "\\set Score.skipBars = ##t"), (b, 1, "\\set Score.skipBars = ##f")]
    for (_, b), (_, _, c) in zip(loops, repeats):  # after a repeat, the track's bar number again
        marks.append((b, 1, f"\\set Score.currentBarNumber = #{c // 8 + 1}"))
    marks.append((at(end), 2, '\\bar "|."'))
    stream, now = [], at(first)
    for t, _, code in sorted(marks, key=lambda m: m[:2]):
        if t > now:
            stream.append(f"s8*{t - now}"); now = t
        stream.append(code)
    names = dict(zip(ORDER, ("soprano", "alto", "tenor", "bass")))
    staves = []
    for v, clef in zip(ORDER, ("treble", "treble", "treble_8", "bass")):
        staves.append(
            f"    \\new Staff \\with {{ instrumentName = {ly_text(VOICE[v])} shortInstrumentName = {ly_text(v + '.')} }} <<\n"
            + ("      \\marks\n" if v == "S" else "")
            + f"      \\new Voice = {ly_text(v)} {{ \\global \\clef {ly_text(clef)} \\{names[v]} }}\n"
            f"    >>\n"
            f"    \\new Lyrics \\lyricsto {ly_text(v)} {{ \\{names[v]}Words }}")
    secs = [(t, name) for t, name, _ in heads]
    edges = {t for q in quiet for t in q}
    music = "\n\n".join(f"{names[v]} = {{{ly_voice(keep[v], secs, loops, edges)}\n}}\n"
                         f"{names[v]}Words = \\lyricmode {{\n  {ly_words(keep[v])}\n}}" for v in ORDER)
    path.write_text(LY.format(marks="\n  ".join(stream), music=music, staves="\n".join(staves)), encoding="utf-8")

LY = r"""% On These Two Hang: the choir's lines, for SATB
% The choir's part of the track at canon-lawyer.ca/music/, bar for bar.
% Written by counterpoint.py --ly from the lines the track plays; do not edit by hand.
% Engrave with GNU LilyPond: lilypond on-these-two-hang.ly
% Dedicated to the public domain (CC0 1.0).

\version "2.24.0"

#(set-global-staff-size 18)

\paper {{
  #(set-paper-size "letter")
  top-margin = 16\mm
  bottom-margin = 14\mm
  left-margin = 20\mm
  right-margin = 20\mm
  markup-system-spacing.padding = 2
  score-markup-spacing.padding = 2
  system-system-spacing.padding = 2
  print-page-number = ##t
  print-first-page-number = ##f
}}

\header {{
  title = "On These Two Hang"
  subtitle = "A double fugue for the household"
  subsubtitle = \markup \italic {{ "“On these two commandments hang all the law and the prophets” (Matthew 22:40)" }}
  poet = "Words: the Vulgate"
  composer = "Notes made by rule: counterpoint.py"
  copyright = "Dedicated to the public domain (CC0 1.0)"
  tagline = \markup \small {{ "canon-lawyer.ca/music/ · Dedicated to the public domain (CC0 1.0) · Made by Claude + Richard" }}
}}

\markup \justify {{
  The choir's part of the track, bar for bar, in mode III, E phrygian. The notes are written out by counterpoint.py
  from the same lines the track plays, and the bar numbers are the track's. The first eight bars, I. Pendet,
  belong to the instruments and to the lawyer's question, so the score begins at bar 9. Each subject is carved from
  its Latin words, a note to a syllable, and its words are set under every statement. The free voices around the
  subjects were found by a search under Fux's rules; they have no text yet. In Golgotha the choir rests through the
  darkness, the veil and the tomb. The last chords are the track's phrygian cadence, a note to a voice.
}}

global = {{ \key e \phrygian \numericTimeSignature \time 4/4 }}

marks = {{
  {marks}
}}

{music}

\score {{
  \new ChoirStaff <<
{staves}
  >>
  \layout {{
    \context {{ \Staff \RemoveEmptyStaves }}
    \context {{ \Lyrics
      \override LyricText.font-size = #0.5
      \override LyricHyphen.minimum-distance = #1.2
      \override LyricSpace.minimum-distance = #1.0
    }}
  }}
}}

\markup \small \italic \justify {{
  Matthew 22:37, 22:39, 27:46, 27:47 and 27:54; John 19:30 (Vulgate). The heading is Matthew 22:40 (King James Version).
  After the cadence the track keeps four bars of silence, and in them “If ye love me, keep my commandments” (John 14:15).
}}
"""

# ---------------------------------------------------------------- the MIDI, by hand
TPQ = 480                                           # ticks to a quarter; an eighth is TPQ // 2

def vlq(n):                                         # a variable-length quantity
    out = [n & 0x7F]
    while n > 0x7F:
        n >>= 7
        out.append(0x80 | (n & 0x7F))
    return bytes(reversed(out))

def meta(kind, data):
    return bytes([0xFF, kind]) + vlq(len(data)) + data

def mtrk(events, end):
    """events: [(tick, order, bytes)]; at the same tick a lower order goes first (a note
    ends before the next one starts). end: the tick where the track ends."""
    out, now = b"", 0
    for tick, _, ev in sorted(events, key=lambda e: e[:2]):
        out += vlq(tick - now) + ev; now = tick
    out += vlq(end - now) + b"\xff\x2f\x00"
    return b"MTrk" + len(out).to_bytes(4, "big") + out

def smf(tracks):                                    # format 1, TPQ ticks to a quarter
    return b"MThd" + (6).to_bytes(4, "big") + (1).to_bytes(2, "big") + len(tracks).to_bytes(2, "big") \
        + TPQ.to_bytes(2, "big") + b"".join(tracks)

def write_midi(folder, voices, sections, parts, repeats):
    """The whole track's choir, bar for bar from bar 1, repeats played out."""
    tick, end = TPQ // 2, parts[-1][1] * TPQ // 2
    conductor = [(0, 0, meta(0x03, b"On These Two Hang")), (0, 0, meta(0x02, b"Dedicated to the public domain (CC0 1.0)")),
                 (0, 0, meta(0x58, bytes([4, 2, 24, 8]))), (0, 0, meta(0x51, (60_000_000 // 120).to_bytes(3, "big")))]
    conductor += [(t * tick, 1, meta(0x06, name.encode("ascii"))) for t, name in sections]
    conductor = mtrk(conductor, end)
    tracks = {}
    for ch, v in enumerate(ORDER):
        ev = [(0, -1, meta(0x03, VOICE[v].encode("ascii"))), (0, -1, bytes([0xC0 | ch, 52]))]   # 52: choir aahs
        for t, p, d, syl, _ in voices[v]:
            if p is None:
                continue
            if syl:
                ev.append((t * tick, 1, meta(0x05, (syl[0] + "-" * syl[1]).encode("ascii"))))
            ev += [(t * tick, 2, bytes([0x90 | ch, p[0], 80])), ((t + d) * tick, 0, bytes([0x80 | ch, p[0], 0]))]
        tracks[v] = mtrk(ev, end)
    folder.mkdir(parents=True, exist_ok=True)
    for v in ORDER:
        (folder / f"on-these-two-hang-{v}.mid").write_bytes(smf([conductor, tracks[v]]))
    (folder / "on-these-two-hang-SATB.mid").write_bytes(smf([conductor] + [tracks[v] for v in ORDER]))

def engrave():
    def arg(flag):
        k = sys.argv.index(flag)
        if k + 1 >= len(sys.argv):
            sys.exit(f"counterpoint.py: {flag} needs a path")
        return Path(sys.argv[k + 1])
    made = piece()
    if "--ly" in sys.argv:
        write_ly(arg("--ly"), *made)
        print(f"counterpoint.py: the score, in LilyPond, at {arg('--ly')}")
    if "--midi" in sys.argv:
        write_midi(arg("--midi"), *made)
        print(f"counterpoint.py: MIDI, a file to a voice and one for all four, in {arg('--midi')}")

def unquoted(lines):
    """The lines the track does not quote exactly as made."""
    src = TRACK.read_text(encoding="utf-8")
    return [k for k, v in lines.items() if not re.search(rf"^const {k} = '{re.escape(v)}'", src, re.M)]

def main():
    if "--ly" in sys.argv or "--midi" in sys.argv:
        return engrave()
    lines, findings = build()
    for sec, f in findings.items():
        print(f"// audit {sec}: " + ("every half note keeps the rules" if not f else "; ".join(f)), file=sys.stderr)
    if "--check" in sys.argv:
        bad = unquoted(lines)
        if bad:
            sys.exit("counterpoint.py: the track does not quote these as made: " + ", ".join(bad))
        print(f"counterpoint.py: {len(lines)} lines, each carved or found by rule, quoted as made")
        return
    for k, v in lines.items():
        print(f"const {k} = '{v}'")

if __name__ == "__main__":
    main()
