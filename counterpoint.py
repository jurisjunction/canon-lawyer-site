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
    python3 counterpoint.py --long     the same for the long form (with --check, --ly, --midi)

The score and the MIDI are written from the same lines, laid out bar for bar as the
track arranges them, and only if the track quotes every line as made.

The long form (section 5) takes the same subjects through the old procedures of the
fugue, a function each: the mirror, the Law held, the head in imitation, the entries
drawn close, the voices exchanged, and a pedal. Every section is audited.

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
ROMAN = "I II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI".split()
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

def write_ly(path, voices, sections, parts, repeats, template=None):
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
    path.write_text((template or LY).format(marks="\n  ".join(stream), music=music, staves="\n".join(staves)), encoding="utf-8")

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

def write_midi(folder, voices, sections, parts, repeats, stem="on-these-two-hang", title="On These Two Hang"):
    """The whole track's choir, bar for bar from bar 1, repeats played out."""
    tick, end = TPQ // 2, parts[-1][1] * TPQ // 2
    conductor = [(0, 0, meta(0x03, title.encode("ascii"))), (0, 0, meta(0x02, b"Dedicated to the public domain (CC0 1.0)")),
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
        (folder / f"{stem}-{v}.mid").write_bytes(smf([conductor, tracks[v]]))
    (folder / f"{stem}-SATB.mid").write_bytes(smf([conductor] + [tracks[v] for v in ORDER]))

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

def unquoted(lines, track=TRACK):
    """The lines the track does not quote exactly as made."""
    src = track.read_text(encoding="utf-8")
    return [k for k, v in lines.items() if not re.search(rf"^const {k} = '{re.escape(v)}'", src, re.M)]

# ---------------------------------------------------------------- 5. the long form, by the old procedures
# The same two subjects, carved the same way, taken through the procedures of the fugue,
# a function each, and every section audited:
#   caput()     the head the subjects share, in imitation between two voices, falling a step a bar
#   invert()    the mirror (1 Cor 13:12): the subject upside down about mi
#   augment()   the Law held: the first subject four times slower, in the bass
#   stretto()   the entries drawn closer together than in the exposition
#   duobus()    the two subjects at once, and with the voices exchanged (double counterpoint)
#   pedal       a long E in the bass under the last entries, and then the cadence
# The free voices are found by weave(): the search of harmonize(), by the same rules and
# costs, for a section in which a voice may be given for a while and free for the rest, and
# which goes on from the section before it, so the joins keep the rules too.

LONG = TRACK.with_name("on-these-two-hang.long.strudel.js")
MI = w_of("e4")                                     # mi, the final: the axis of the mirror
LEVELS = (0, 7, -7, 14, -14, 4, -4, 11, -11, 3, -3, 10, -10)   # unison and octaves, fifths, fourths
BREATH = 4                                          # a voice rests a half note before it enters
STEP_COST = {0: 2, 1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 9, 7: 4}   # score()'s, for a free voice's motion

def invert(subj):
    """The mirror: every step up a step down, about mi, on the white keys (diatonic
    inversion). E stays E; D and F change places, and so do C and G."""
    return [(None if w is None else 2 * MI - w, d) for w, d in subj]

def augment(subj, k=4):
    """The Law held: the same notes, each k times as long."""
    return [(w, k * d) for w, d in subj]

def span(seq):
    return sum(d for _, d in seq)

def pad(seq, eighths):
    """A line made up to its length with a rest."""
    assert span(seq) <= eighths, (span(seq), eighths)
    return seq + [(None, eighths - span(seq))] * (span(seq) < eighths)

def tidy(seq):
    """Rests that follow each other, as one."""
    out = []
    for w, d in seq:
        if out and w is None and out[-1][0] is None:
            out[-1] = (None, out[-1][1] + d)
        else:
            out.append((w, d))
    return out

def cut(seq, end):
    """A line up to eighth end; a note that runs past it is shortened."""
    out, t = [], 0
    for w, d in seq:
        if t < end:
            out.append((w, min(d, end - t)))
        t += d
    return out

def in_range(v, seq):
    ws = [w for w, _ in seq if w is not None]
    return w_of(RANGE[v][0]) <= min(ws) and max(ws) <= w_of(RANGE[v][1])

def bad_leap(a, b):                                 # a tritone, a seventh, more than an octave
    s = abs(midi(a) - midi(b))
    return s in (6, 10, 11) or s > 12

def leaps(seq):
    ws = [w for w, _ in seq if w is not None]
    return any(bad_leap(x, y) for x, y in zip(ws, ws[1:]))

def comfort(v, seq):
    """How far a line sits from the middle of its voice, in semitones."""
    ws = [midi(w) for w, _ in seq if w is not None]
    return abs(sum(ws) / len(ws) - (midi(w_of(RANGE[v][0])) + midi(w_of(RANGE[v][1]))) / 2)

def on_final(level):                                # an entry on E, the final, or on B, its fifth
    return level % 7 in (0, 4)

def clash(given):
    """The given against the given: what audit() finds between the given lines on the half
    notes (a line's own leaps are its own, and not counted)."""
    n = max(span(s) for s in given.values())
    return [f for f in audit({v: pad(s, n) for v, s in given.items()}) if ": leap " not in f]

def last_note(seq, t):
    """The last note a line struck before eighth t, across rests."""
    at, out = 0, None
    for w, d in seq:
        if at >= t:
            break
        out = w if w is not None else out
        at += d
    return out

def next_note(seq, t):
    """The first note a line strikes at or after eighth t."""
    at = 0
    for w, d in seq:
        if at >= t and w is not None:
            return w
        at += d
    return None

# ---------------------------------------------------------------- the search, for voices that change role
def weave(given, free, eighths, before=None, after=None, slot=4, end_perfect=True, width=300):
    """harmonize(), for a section in which a voice may be given for a while and free for the
    rest. given: {voice: line}, rests where it is not given; free: {voice: [(start, end)]},
    in eighths, on the half notes, where a voice is to be found; before: {voice: line}, the
    section before, so the search goes on from it by the same rules; after: {voice: note},
    what a voice sings next, after the section. The rules and the costs are score()'s. The
    beam keeps the cheapest path to each pair of last two chords. Returns {voice: [w or None,
    a slot each]} and the cost."""
    pre = span(before["S"]) if before else 0
    whole = {v: (before[v] if before else []) + given.get(v, [(None, eighths)]) for v in ORDER}
    slots = list(range(0, eighths, slot))
    n = len(slots)
    on = {v: [any(a <= t < b for a, b in free.get(v, ())) for t in slots] for v in ORDER}
    for v in ORDER:
        for i, t in enumerate(slots):
            assert not (on[v][i] and any(sounding(given.get(v, [(None, eighths)]), u)[0] is not None
                                         for u in range(t, t + slot))), (v, t)
    F = [tuple(v for v in ORDER if on[v][i]) for i in range(n)]
    def note(v, t):
        x = sounding(whole[v], pre + t) if pre + t >= 0 else None
        return x[0] if x else None
    cand = {v: list(range(w_of(RANGE[v][0]), w_of(RANGE[v][1]) + 1)) for v in free}
    steps = []
    for i, t in enumerate(slots):
        Fi, was = F[i], F[i - 1] if i else ()
        G = {v: note(v, t) for v in ORDER if v not in Fi}
        G = {v: w for v, w in G.items() if w is not None}
        backs = [t - slot] + ([t - 1] if i == 0 and before else [])   # at a join, the last chord too
        P = [{v: w for v in ORDER if v not in was for w in [note(v, b)] if w is not None} for b in backs]
        enter = {v: last_note(whole[v], pre + t) for v in Fi if v not in was}
        leave = {}
        for v in Fi:
            if i == n - 1 or not on[v][i + 1]:
                nx = next_note(whole[v], pre + t + slot)
                nx = nx if nx is not None else (after or {}).get(v)
                if nx is not None:
                    leave[v] = nx
        chords = []
        for combo in itertools.product(*(cand[v] for v in Fi)):
            now = dict(G); now.update(zip(Fi, combo))
            if any(bad_leap(now[v], leave[v]) for v in leave):
                continue
            c = chord_cost(now, Fi, whole, pre, t, slot, end_perfect and i == n - 1)
            if c is not None:
                chords.append((combo, now, c))
        if not chords:
            raise SystemExit(f"counterpoint.py: no chord for the free voices at eighth {t}")
        steps.append((Fi, was, P, enter, chords))
    beam = [((), 0)]
    for i, (Fi, was, P, enter, chords) in enumerate(steps):
        older = F[i - 2] if i > 1 else ()
        best = {}
        for path, cost in beam:
            prevs = [dict(p, **dict(zip(was, path[-1]))) if i else dict(p) for p in P]
            mel = {v: (path[-1][was.index(v)], path[-2][older.index(v)] if v in older else None)
                   if v in was else (enter.get(v), None) for v in Fi}
            for combo, now, c in chords:
                d = motion_cost(now, Fi, was, prevs, mel)
                if d is None:
                    continue
                key = (path[-1] if i else (), combo)
                if key not in best or cost + c + d < best[key][1]:
                    best[key] = (path + (combo,), cost + c + d)
        beam = sorted(best.values(), key=lambda x: x[1])[:width]
        if not beam:
            raise SystemExit(f"counterpoint.py: no counterpoint found at eighth {slots[i]}")
    path, cost = beam[0]
    out = {v: [None] * n for v in free}
    for i, combo in enumerate(path):
        for v, w in zip(F[i], combo):
            out[v][i] = w
    return out, cost

def chord_cost(now, Fi, whole, pre, t, slot, last):
    """score()'s rules for one chord: no crossing, every pair with a free voice consonant (a
    fourth between upper voices), spacing; a given note struck on a weak eighth that clashes
    with a free voice must pass by step; the last chord leans to fifths and octaves."""
    voices = [v for v in ORDER if v in now]
    low = voices[-1]
    cost = 0
    for a, b in itertools.combinations(voices, 2):
        if a not in Fi and b not in Fi:
            continue                                # the given against the given: not ours to change
        if midi(now[a]) < midi(now[b]):
            return None
        x = ic(now[a], now[b])
        if x == 5 and low not in (a, b):
            pass
        elif x not in CONS:
            return None
        if x == 0 and midi(now[a]) == midi(now[b]):
            cost += 3
    for hi, lo in zip(voices, voices[1:]):
        if midi(now[hi]) - midi(now[lo]) > (19 if lo == low else 12):
            cost += 3
    for u in range(t + 1, t + slot):
        for v in ORDER:
            x = sounding(whole[v], pre + u) if v not in Fi else None
            if not x or not x[1] or x[0] is None:
                continue
            for f in Fi:
                if ic(x[0], now[f]) not in CONS and not passing(whole[v], pre + u):
                    cost += 6
    if last:
        for v in Fi:
            if v != low and ic(now[v], now[low]) not in PERFECT:
                cost += 2
    return cost

def motion_cost(now, Fi, was, prevs, mel):
    """score()'s rules for the motion into a chord: no parallel fifths, octaves or unisons;
    hidden ones in the outer voices cost; a free voice does not leap a tritone, a seventh or
    more than an octave, prefers steps, and turns back by step after a leap."""
    voices = [v for v in ORDER if v in now]
    top, low = voices[0], voices[-1]
    moving = set(Fi) | set(was)
    cost = 0
    for k, prev in enumerate(prevs):
        for a, b in itertools.combinations(voices, 2):
            if a not in prev or b not in prev or not {a, b} & moving:
                continue
            p, q = ic(prev[a], prev[b]), ic(now[a], now[b])
            da, db = now[a] - prev[a], now[b] - prev[b]
            if p in PERFECT and p == q and da and db and (da > 0) == (db > 0):
                return None
            if k == 0 and q in PERFECT and da and db and (da > 0) == (db > 0) and (a, b) == (top, low) \
                    and abs(now[top] - prev[top]) > 1:
                cost += 4
    for v in Fi:
        m1, m2 = mel[v]
        if m1 is None:
            continue
        if bad_leap(m1, now[v]):
            return None
        d = now[v] - m1
        cost += STEP_COST.get(abs(d), 9)
        if m2 is not None:
            d0 = m1 - m2
            if abs(d0) >= 3 and not (abs(d) == 1 and (d > 0) != (d0 > 0)):
                cost += 3
    for v in was:
        if v not in Fi and v in now and v in prevs[0] and bad_leap(prevs[0][v], now[v]):
            return None
    return cost

def assemble(given, found, eighths, slot=4):
    """Each voice's line: its given notes, and the notes found for it where it was free."""
    out = {}
    for v in ORDER:
        line, t = [], 0
        for w, d in given.get(v, [(None, eighths)]):
            end = t + d
            if w is not None or v not in found:
                line.append((w, d)); t = end; continue
            while t < end:
                i, nt = t // slot, min(end, (t // slot + 1) * slot)
                if t % slot == 0 and nt == t + slot and found[v][i] is not None:
                    line.append((found[v][i], slot))
                else:
                    line.append((None, nt - t))
                t = nt
        out[v] = tidy(line)
        assert span(out[v]) == eighths, (v, span(out[v]), eighths)
    return out

# ---------------------------------------------------------------- a section's plan
class Plan:
    """The given notes of a section, where its voices are free, and what is sung to which words.
    entries: {voice: [(start, notes)]}; said: {voice: [(start, TEXTS key, notes)]}, the words
    under a statement; ring: [(start, notes)], the statements the bells ring over."""
    def __init__(self, eighths):
        self.eighths, self.entries, self.said, self.ring, self.free = eighths, {v: [] for v in ORDER}, \
            {v: [] for v in ORDER}, [], {}
    def enter(self, v, t, notes, key=None, count=None, ring=True):
        assert all(t >= a + span(n) or t + span(notes) <= a for a, n in self.entries[v]), (v, t)
        self.entries[v].append((t, notes))
        if key:
            self.said[v].append((t, key, count or len(notes)))
        if ring:
            self.ring.append((t, notes))
    def line(self, v):
        out, t = [], 0
        for a, notes in sorted(self.entries[v], key=lambda e: e[0]):
            out = pad(out, a) + notes
        return tidy(pad(out, self.eighths))
    def breathe(self, v, lead_in=True, tail=True, breath=BREATH):
        """Where a voice is free: between its entries, but for a half note's rest before each;
        before its first entry only if it sings on from the section before (lead_in); after its
        last one if tail. A voice with no entries is free throughout."""
        spans, t = [], 0
        es = sorted(self.entries[v], key=lambda e: e[0])
        for k, (a, notes) in enumerate(es):
            if (k or lead_in) and a - breath > t:
                spans.append((t, a - breath))
            t = a + span(notes)
        if tail and t < self.eighths:
            spans.append((t, self.eighths))
        self.free[v] = spans

def ring_over(ring, eighths):
    """The bells: over each statement, from its entry until the next one enters, by the rule
    of tintinnabuli()."""
    out, ring = [], sorted(ring, key=lambda r: r[0])
    for k, (t, notes) in enumerate(ring):
        stop = ring[k + 1][0] if k + 1 < len(ring) else eighths
        out = pad(out, t) + cut(tintinnabuli(notes), stop - t)
    return tidy(pad(out, eighths))

def make(plan, before=None, after=None):
    """A section from its plan: the free voices found by weave(), the whole audited."""
    given = {v: plan.line(v) for v in ORDER}
    free = {v: s for v, s in plan.free.items() if s}
    found, _ = weave(given, free, plan.eighths, before, after) if free else ({}, 0)
    lines = assemble(given, found, plan.eighths)
    return {"lines": lines, "said": plan.said, "bells": ring_over(plan.ring, plan.eighths), "audit": audit(lines)}

def fixed(lines, said, ring, slot=4):
    """A section made before, as it is."""
    return {"lines": lines, "said": said, "bells": ring_over(ring, span(lines["S"])), "audit": audit(lines, slot=slot)}

def joined(*made):
    """Sections one after another, as one."""
    out, t = {"lines": {v: [] for v in ORDER}, "said": {v: [] for v in ORDER}, "bells": []}, 0
    for m in made:
        for v in ORDER:
            out["lines"][v] = tidy(out["lines"][v] + m["lines"][v])
            out["said"][v] += [(a + t, k, c) for a, k, c in m["said"][v]]
        out["bells"] = tidy(out["bells"] + m["bells"])
        t += span(m["lines"]["S"])
    out["audit"] = audit(out["lines"])
    return out

def lasts(lines, within=8):
    """What each voice sang last in a section, if it sings in its last bar."""
    n = span(lines["S"])
    return {v: last_note(lines[v], n) for v in ORDER
            if any((sounding(lines[v], t) or (None,))[0] is not None for t in range(n - within, n))}

def firsts(made, within=8):
    """What each voice sings first in a section, if it sings in its first bar: the note a
    voice of the section before must reach without a bad leap."""
    out = {}
    for v in ORDER:
        x = next_note(made["lines"][v], 0)
        at = 0
        for w, d in made["lines"][v]:
            if w is not None:
                break
            at += d
        if x is not None and at < within:
            out[v] = x
    return out

# ---------------------------------------------------------------- 4'. the procedures
HEAD = 6                                            # mi mi re sol mi ut: the head the subjects share

def caput(S, lead, follow, before=None, after=None, most=5, late=4):
    """An episode: the head the subjects share (mi mi re sol mi ut, "Diliges Domi-" and
    "Diliges proxi-") in imitation, the leader falling a step each bar and the follower after
    it by a half note at a fixed interval, holding its last note. The leader's level and the
    interval are found by search: both in range, no bad leap inside a line or from the note
    before it (before: {voice: note}) or, for the follower's held note, into the note after it
    (after); then the fewest clashes, then the most heads (five at most, three at least), then
    the leader nearest the middle of its voice. The leader sings the
    first commandment's words, the follower the second's. The other voices are free; the
    leader is free when its heads are done; the follower rests until it enters."""
    head = S["DILIGES"][:HEAD]
    assert head == S["SIMILE"][:HEAD]
    before, after = before or {}, after or {}
    def falling(level, heads, start, hold):
        seq = []
        for u in range(heads):
            seq += transpose(head, level - u)
        if hold:
            seq[-1] = (seq[-1][0], seq[-1][1] + 8 * (heads + 1) - start - span(seq))
        return seq
    best = None
    for heads in range(most, 2, -1):
        for level in range(-21, 15):
            for gap in LEVELS:
                a, b = falling(level, heads, 0, False), falling(level + gap, heads, late, True)
                if not in_range(lead, a) or not in_range(follow, b) or leaps(a) or leaps(b):
                    continue
                if (lead in before and bad_leap(before[lead], a[0][0])) or (follow in before and bad_leap(before[follow], b[0][0])) \
                        or (follow in after and bad_leap(b[-1][0], after[follow])):
                    continue
                key = (len(clash({lead: a, follow: [(None, late)] + b})), -heads, comfort(lead, a), level, gap)
                if best is None or key < best[0]:
                    best = (key, a, b)
    (clashes, heads, _, level, gap), a, b = best
    heads = -heads
    eighths = 8 * (heads + 1)
    plan = Plan(eighths)
    for u in range(heads):
        plan.enter(lead, 8 * u, a[HEAD * u:HEAD * (u + 1)], "DILIGES", HEAD, ring=False)
        plan.enter(follow, late + 8 * u, b[HEAD * u:HEAD * (u + 1)], "SIMILE", HEAD, ring=False)
    plan.ring.append((0, a))                        # the bells ring over the leader
    for v in ORDER:
        plan.breathe(v, lead_in=v != follow)
    return plan, {"lead": lead, "follow": follow, "level": level, "gap": gap, "heads": heads, "clashes": clashes}

def stretto(forms, voices, distances, hold=None, after=None):
    """Entries of the subjects in forms, one after another, each the same number of half notes
    after the one before, in the voices in turn. The distance, the order of the voices, and
    each entry's level (from the first: unison, octave, fifth or fourth, LEVELS) are found by
    search, so that the given lines clash least on the half notes: no clash if there is a way,
    then the closest distance, then entries on E or B, then lines nearest the middle of their
    voices. hold: {voice: note} held under it all (a pedal); after: {voice: note}, what a voice
    sings next if its last entry ends the section. No entry may leap badly inside itself, nor
    from one entry straight into the next or into what comes after. Returns (clashes found,
    distance, [(start, voice, level)], eighths)."""
    hold = hold or {}
    results, cols_cache = [], {}
    def columns(seq, n):
        return [(sounding(seq, t) or (None,))[0] for t in range(0, n, 4)]
    def pair(x, y):                                 # x above y; the clashes a third voice cannot cure
        k = 0
        for i in range(len(x)):
            if x[i] is None or y[i] is None:
                continue
            q = ic(x[i], y[i])
            k += (q not in CONS and q != 5) + (midi(x[i]) < midi(y[i]))
            if i and x[i - 1] is not None and y[i - 1] is not None:
                p, da, db = ic(x[i - 1], y[i - 1]), x[i] - x[i - 1], y[i] - y[i - 1]
                k += p in PERFECT and p == q and da and db and (da > 0) == (db > 0)
        return k
    for limit in range(9):                          # no clash if there can be none; else as few as can be
        for k in distances:
            for order in itertools.permutations(voices):
                who = [order[j % len(order)] for j in range(len(forms))]
                starts = [4 * k * j for j in range(len(forms))]
                ends = [s + span(f) for s, f in zip(starts, forms)]
                if any(who[i] == who[j] and starts[j] < ends[i] for i in range(len(forms)) for j in range(i + 1, len(forms))):
                    continue
                n = -(-max(ends) // 8) * 8
                held = {v: [(w, n)] for v, w in hold.items()}
                hcols = {v: columns(s, n) for v, s in held.items()}
                def options(j, l0):
                    ls = range(-21, 15) if j == 0 else [l0 + r for r in LEVELS]
                    return [l for l in ls if (j or l % 7 in (0, 3, 4)) and in_range(who[j], transpose(forms[j], l))
                            and not leaps(transpose(forms[j], l))]
                def col(j, l):
                    key = (k, j, l)
                    if key not in cols_cache:
                        cols_cache[key] = columns([(None, starts[j])] * bool(starts[j]) + transpose(forms[j], l), n)
                    return cols_cache[key]
                def above(a, b):
                    return ORDER.index(a) < ORDER.index(b)
                def dfs(j, levels, bound):
                    if j == len(forms):
                        lines = {}
                        for jj, l in enumerate(levels):
                            v = who[jj]
                            lines[v] = pad(lines.get(v, []), starts[jj]) + transpose(forms[jj], l)
                        for jj in range(1, len(forms)):    # a voice that goes straight on from one entry to the next
                            prev = [i for i in range(jj) if who[i] == who[jj]]
                            if prev and ends[prev[-1]] == starts[jj] and bad_leap(
                                    transpose(forms[prev[-1]], levels[prev[-1]])[-1][0], transpose(forms[jj], levels[jj])[0][0]):
                                return
                        for jj, l in enumerate(levels):
                            if ends[jj] == n and who[jj] in (after or {}) and bad_leap(transpose(forms[jj], l)[-1][0], after[who[jj]]):
                                return
                        lines.update(held)
                        c = len(clash(lines))
                        if c <= limit:
                            off = sum(not on_final(l) for l in levels)
                            ease = sum(comfort(who[jj], transpose(forms[jj], l)) for jj, l in enumerate(levels))
                            results.append(((c, k, off, round(ease, 3), order, tuple(levels)), [(s, v, l) for s, v, l in zip(starts, who, levels)], n))
                        return
                    for l in options(j, levels[0] if levels else None):
                        x = col(j, l)
                        b = bound
                        for i, li in enumerate(levels):
                            if who[i] != who[j]:
                                y = col(i, li)
                                b += pair(x, y) if above(who[j], who[i]) else pair(y, x)
                        for v, y in hcols.items():
                            b += pair(x, y) if above(who[j], v) else pair(y, x)
                        if b <= limit:
                            dfs(j + 1, levels + [l], b)
                dfs(0, [], 0)
        if results:
            break
    if not results:
        raise SystemExit("counterpoint.py: no stretto with fewer than nine clashes")
    key, entries, n = min(results, key=lambda r: r[0])
    return key[0], key[1], entries, n

def section_stretti(S, parts, hold=None, lead_in=False, after=None):
    """Stretti one after another, as one section: parts [(forms, keys, voices, distances)].
    The voices rest before their first entry unless lead_in, are free between entries but
    for a breath, and after their last."""
    found, t, plans = [], 0, []
    for forms, keys, voices, distances in parts:
        clashes, k, entries, n = stretto(forms, voices, distances, hold, after)
        found.append({"clashes": clashes, "distance": k, "entries": entries, "bars": n // 8,
                      "voices": "".join(v for _, v, _ in entries)})
        plans.append((t, forms, keys, entries))
        t += n
    plan = Plan(t)
    for t0, forms, keys, entries in plans:
        for (s, v, l), f, key in zip(entries, forms, keys):
            plan.enter(v, t0 + s, transpose(f, l), key)
    for v, w in (hold or {}).items():
        plan.enter(v, 0, [(w, t)], ring=False)
    for v in ORDER:
        if v in (hold or {}):
            plan.free[v] = []
        else:
            plan.breathe(v, lead_in=lead_in)
    return plan, found

def lex(S, voices="TAS", gap=16):
    """The Law held: the first subject in long notes, each four times longer, as a cantus firmus
    in the bass, an octave down, with its words. Over it, entries of the second subject and its
    mirror in their own values: each as soon as it can come without a clash against the Law or
    the entries before it, at least gap eighths after the last, in the voices in turn and the two
    forms in turn, on E or B before A, nearest the middle of the voice. The other voices are free."""
    law = transpose(augment(S["DILIGES"]), -7)
    n = span(law)
    plan = Plan(n)
    plan.enter("B", 0, law, "DILIGES")
    forms = (("rectus", S["SIMILE"]), ("inversus", invert(S["SIMILE"])))
    taken, t, turn, form, done = [], 0, 0, 0, {v: -BREATH for v in voices}
    while t + span(S["SIMILE"]) <= n:
        hit = None
        for dv in range(len(voices)):
            v = voices[(turn + dv) % len(voices)]
            if done[v] + BREATH > t:
                continue
            for df in range(2):
                fname, f = forms[(form + df) % 2]
                levels = sorted((l for l in range(-21, 15) if l % 7 in (0, 3, 4) and in_range(v, transpose(f, l))
                                 and not leaps(transpose(f, l))),
                                key=lambda l: (not on_final(l), comfort(v, transpose(f, l)), l))
                for l in levels:
                    given = {u: plan.line(u) for u in ORDER if plan.entries[u]}
                    trial = dict(given)
                    trial[v] = tidy(pad(cut(given.get(v, []), t), t) + transpose(f, l))
                    if not clash(trial):
                        hit = (v, fname, f, l); break
                if hit: break
            if hit: break
        if hit:
            v, fname, f, l = hit
            plan.enter(v, t, transpose(f, l), "SIMILE")
            taken.append((t, v, fname, l))
            done[v] = t + span(f)
            turn, form = voices.index(v) + 1, [x for x, _ in forms].index(fname) + 1
            t += gap
        else:
            t += 4
    for v in ORDER:
        if v != "B":
            plan.breathe(v)
    return plan, taken

def duobus(first, first_key, second, second_key, top_first, offsets=(4, 8, 0, 12)):
    """Both subjects at once, the second entering a little after the first, one in the soprano
    and one in the bass: top_first puts the first subject on top. The levels and the entry of
    the second are found by search, so that the two clash least: no clash, then the second a
    half note after the first (as in the short form), then entries on E or B, then lines nearest
    the middle of their voices. The alto and tenor are free. Returns the plan and what was found."""
    hi_v, lo_v = ("S", "B")
    best = None
    for la in range(-21, 15):
        for lb in range(-21, 15):
            for off in offsets:
                a, b = transpose(first, la), transpose(second, lb)
                va, vb = (hi_v, lo_v) if top_first else (lo_v, hi_v)
                if not in_range(va, a) or not in_range(vb, b) or leaps(a) or leaps(b) or off + span(b) > 32:
                    continue
                c = len(clash({va: pad(a, 32), vb: pad([(None, off)] * bool(off) + b, 32)}))
                key = (c, off != offsets[0], (not on_final(la)) + (not on_final(lb)),
                       round(comfort(va, a) + comfort(vb, b), 3), la, lb, off)
                if best is None or key < best[0]:
                    best = (key, va, vb, a, b, off, la, lb)
    key, va, vb, a, b, off, la, lb = best
    plan = Plan(32)
    plan.enter(va, 0, a, first_key, ring=va == "S")
    plan.enter(vb, off, b, second_key, ring=vb == "S")
    for v in "AT":
        plan.breathe(v)
    return plan, {"clashes": key[0], "offset": off, "levels": (la, lb), "first in": va}

# ---------------------------------------------------------------- the long form
VERE_PARTS = (("DUO", 2), ("TRIO", 2), ("TUTTI", 4))   # the short track's V. Vere, as it arranges it

def build_long():
    """Every line of the long form, its sections made and audited. Returns the lines, the
    audit of each section and of each join, the sections, and what each search found."""
    keep = {}
    lines, findings = build(keep)
    S = keep["subjects"]
    I, II = S["DILIGES"], S["SIMILE"]
    Ii, IIi = invert(I), invert(II)
    lines.update(DILIGES_INV=mini(Ii), SIMILE_INV=mini(IIi), DILIGES_AUG=mini(augment(I)), CAPUT=mini(I[:HEAD]))
    notes, made = {}, {}
    # II. Diliges and IV. Simile: the expositions of the short form, as they are
    for key in ("DILIGES", "SIMILE"):
        exp, entries = keep[key]
        size = span(S[key])
        made[key] = fixed(exp, {v: [(k * size, key, len(S[key])) for k, (u, _) in enumerate(entries) if u == v] for v in ORDER},
                          [(k * size, transpose(S[key], shift)) for k, (_, shift) in enumerate(entries)])
    # VI. Speculum, the mirror: the first exposition inverted, the voices' order mirrored too
    # (the tenor leads where the alto led, and the bass answers where the soprano did); then the
    # second subject inverted, from the top down, over voices that go on singing
    mirror1 = [("T", -7), ("B", -10), ("A", 0), ("S", 4)]
    spec1 = fixed(section_exposition(Ii, mirror1),
                  {v: [(k * 32, "DILIGES", len(Ii)) for k, (u, _) in enumerate(mirror1) if u == v] for v in ORDER},
                  [(k * 32, transpose(Ii, s)) for k, (_, s) in enumerate(mirror1)])
    mirror2 = [("S", 4), ("A", 0), ("T", -3), ("B", -7)]
    plan = Plan(96)
    for k, (v, s) in enumerate(mirror2):
        plan.enter(v, 24 * k, transpose(IIi, s), "SIMILE")
    for v in ORDER:
        plan.breathe(v)
    spec2 = make(plan, before=spec1["lines"])
    made["SPECULUM"] = joined(spec1, spec2)
    notes["SPECULUM"] = {"first": mirror1, "second": mirror2}
    # V. Vere, as in the short form
    ref = keep["VERE"]
    parts = [(ref[p], b // 2) for p, b in VERE_PARTS]
    made["VERE"] = {"lines": {v: tidy(sum((r.get(v, [(None, 16)]) * k for r, k in parts), [])) for v in ORDER},
                    "said": {v: [] for v in ORDER}, "bells": [], "audit": [f for r, _ in parts for f in audit(r, slot=2)]}
    t = 0
    for r, k in parts:
        for _ in range(k):
            made["VERE"]["said"]["S"].append((t, "VERE", len(S["VERE"]))); t += 16
    # VII. Lex: the Law held
    plan, taken = lex(S)
    notes["LEX"] = taken
    lex_plan = plan
    # XI. In unum: the first subject in stretto, then the second, then both
    plan, found = section_stretti(S, [
        ((I,) * 4, ("DILIGES",) * 4, "SATB", range(1, 8)),             # closer than the exposition's 8 half notes
        ((II,) * 4, ("SIMILE",) * 4, "SATB", range(1, 6)),             # closer than its 6
        ((I, II, I, II), ("DILIGES", "SIMILE") * 2, "SATB", range(1, 8)),
    ])
    notes["IN_UNUM"] = found
    unum_plan = plan
    # XIII. Fundamentum: a pedal on E, the final, held by the bass; over it the second subject
    # and its mirror in turn, in stretto, in the upper voices
    amen = {"B": w_of("f2"), "T": w_of("c3"), "A": w_of("a3"), "S": w_of("d4")}   # the cadence's first chord
    plan, found = section_stretti(S, [((II, IIi) * 3, ("SIMILE",) * 6, "SAT", range(2, 6))], hold={"B": w_of("e2")},
                                  lead_in=True, after=amen)
    notes["FUNDAMENTUM"] = found
    fund_plan = plan
    # XII. Duobus: as in the short form; then in the mirror; then with the voices exchanged
    comb = keep["DUOBUS"]
    rectus = fixed(comb, {"S": [(4, "SIMILE", len(II))], "B": [(0, "DILIGES", len(I))], "A": [], "T": []},
                   [(4, transpose(II, 4))])
    # the episodes: the four ways the head falls in imitation, each once
    capita = {}
    def episode(name, lead, follow, before, after_made):
        plan, found = caput(S, lead, follow, lasts(before), firsts(after_made))
        capita[name] = found
        made[name] = make(plan, before=before, after=firsts(after_made))
        lines.update({f"{name}_{v}": mini(made[name]["lines"][v]) for v in ORDER}, **{f"{name}_TIN": mini(made[name]["bells"])})
    episode("CAPUT_I", "S", "T", made["DILIGES"]["lines"], made["SIMILE"])
    episode("CAPUT_II", "A", "B", made["SIMILE"]["lines"], made["SPECULUM"])
    made["LEX"] = make(lex_plan, before=made["SPECULUM"]["lines"],
                       after={"S": S["ELI"][0][0]})
    unum_first = {"lines": {v: unum_plan.line(v) for v in ORDER}}
    episode("CAPUT_III", "T", "B", made["VERE"]["lines"], unum_first)
    made["IN_UNUM"] = make(unum_plan, before=made["CAPUT_III"]["lines"])
    episode("CAPUT_IV", "S", "B", made["IN_UNUM"]["lines"], rectus)
    plan, found = duobus(Ii, "DILIGES", IIi, "SIMILE", top_first=False)
    notes["DUOBUS_M"] = found
    mirror = make(plan, before=rectus["lines"])
    plan, found = duobus(I, "DILIGES", II, "SIMILE", top_first=True)
    notes["DUOBUS_X"] = found
    fund_first = {"lines": {v: fund_plan.line(v) for v in ORDER}}
    exchanged = make(plan, before=mirror["lines"], after=firsts(fund_first))
    made["DUOBUS"] = joined(rectus, mirror, exchanged)
    made["DUOBUS"]["parts"] = (rectus, mirror, exchanged)
    made["FUNDAMENTUM"] = make(fund_plan, before=exchanged["lines"], after=amen)
    for name, m in (("DUOBUS_M", mirror), ("DUOBUS_X", exchanged)):
        lines.update({f"{name}_{v}": mini(m["lines"][v]) for v in ORDER}, **{f"{name}_TIN": mini(m["bells"])})
    for name in ("SPECULUM", "LEX", "IN_UNUM", "FUNDAMENTUM"):
        lines.update({f"{name}_{v}": mini(made[name]["lines"][v]) for v in ORDER}, **{f"{name}_TIN": mini(made[name]["bells"])})
    notes.update(capita)
    long_findings = {k: made[k]["audit"] for k in LONG_ORDER if k in made}
    for (a, b) in zip(LONG_ORDER, LONG_ORDER[1:]):
        if a in made and b in made:
            long_findings[f"{a}/{b}"] = seam(made[a]["lines"], made[b]["lines"])
    end = made["FUNDAMENTUM"]["lines"]               # into the cadence: its chords are given, so only the leaps
    long_findings["FUNDAMENTUM/AMEN"] = [f"{v}: leap {name(last_note(end[v], span(end[v])))}-{name(w)}"
                                         for v, w in amen.items() if bad_leap(last_note(end[v], span(end[v])), w)]
    made["keep"] = keep
    return lines, long_findings, made, notes

LONG_ORDER = ("DILIGES", "CAPUT_I", "SIMILE", "CAPUT_II", "SPECULUM", "LEX", "GOLGOTHA", "VERE",
              "CAPUT_III", "IN_UNUM", "CAPUT_IV", "DUOBUS", "FUNDAMENTUM")

def seam(a, b, width=8):
    """The join of two sections: the last bar of one and the first of the next, audited as one."""
    window = {v: cut(list(reversed(cut(list(reversed(a[v])), width))), width) + cut(b[v], width) for v in ORDER}
    return audit(window)

# ---------------------------------------------------------------- the long form, as a score and as MIDI
TITLES = {"secPENDET": "Pendet", "secDILIGES": "Diliges", "secSIMILE": "Simile", "secSPECULUM": "Speculum",
          "secLEX": "Lex", "secGOLGOTHA": "Golgotha", "secVERE": "Vere", "secIN_UNUM": "In unum",
          "secDUOBUS": "Duobus", "secFUNDAMENTUM": "Fundamentum", "secAMEN": "Amen",
          **{f"secCAPUT_{r}": "Caput" for r in ("I", "II", "III", "IV")}}
DUOBUS_PARTS = ("DUOBUS_S", "DUOBUS_M_S", "DUOBUS_X_S")   # as it is, in the mirror, with the voices exchanged

def misarranged(made, src):
    """What the long track arranges otherwise than the sections were made."""
    bad, order = [], []
    for bars, sec in arrangement(src):
        key = sec[3:]
        order.append(key)
        if sec not in TITLES:
            bad.append(f"{sec} is not a section of the long form")
        elif key in made and span(made[key]["lines"]["S"]) != 8 * bars:
            bad.append(f"{sec} is {bars} bars, but was made {span(made[key]['lines']['S']) // 8}")
    if [k for k in order if k in LONG_ORDER] != list(LONG_ORDER):
        bad.append("the sections are not in the order they were made: " + " ".join(order))
    if [(p.split("_")[1], b) for b, p in arrangement(src, "secVERE")] != list(VERE_PARTS):
        bad.append("V. Vere is not arranged as in the short form")
    if [p for _, p in arrangement(src, "secDUOBUS")] != list(DUOBUS_PARTS):
        bad.append("Duobus is not arranged as made")
    return bad

def piece_long():
    """The choir's part of the long form, from its first bar, as piece() gives the short one."""
    lines, findings, made, _ = build_long()
    src = LONG.read_text(encoding="utf-8")
    if any(findings.values()) or unquoted(lines, LONG) or misarranged(made, src):
        raise SystemExit("counterpoint.py: the long form breaks a rule or its track does not quote it as made; run --long --check")
    keep = made["keep"]
    S, refrains = keep["subjects"], keep["VERE"]
    sung = {"ELI": (S["ELI"], "ELI"), "ELIAM": (S["ELIAM"], "ELIAM"), "CONSUMMATUM": (S["CONSUMMATUM"], "CONSUMMATUM"),
            "VERE_SOLO_S": (refrains["SOLO"]["S"], "VERE")}
    voices, sections, parts = {v: [] for v in ORDER}, [], []
    clock, marked = 0, False

    def part(bars, lines, said=None, over=None, free=False):
        """One stretch of the track. lines: {voice: [(pitch, eighths)]}; said: {voice: [(start,
        TEXTS key, notes)]}, the words under each statement; the voices not in lines are silent."""
        nonlocal clock, marked
        made = {}
        for v in ORDER:
            seq = lines.get(v, [(None, 8 * bars)])
            assert sum(d for _, d in seq) == 8 * bars, (v, bars)
            starts = {a: (k, c) for a, k, c in (said or {}).get(v, ())}
            t, left, events = 0, [], []
            for i, (p, d) in enumerate(seq):
                if t in starts:
                    assert not left, (v, t)
                    k, c = starts.pop(t)
                    left = underlay(k)[:c]
                syl = left.pop(0) if p is not None and left else None
                events.append([clock + t, p, d, syl, over[1] if i == 0 and over and over[0] == v else None])
                t += d
            assert not left and not starts, (v, left, starts)
            made[v] = events
        if free and not marked:                         # the first free note in time is marked, once
            loose = [(e[0], ORDER.index(v), e) for v in ORDER for e in made[v] if e[1] is not None and e[3] is None]
            if loose:
                min(loose, key=lambda x: x[:2])[2][4], marked = FREE, True
        for v in ORDER:
            voices[v] += made[v]
        parts.append((clock, clock + 8 * bars))
        clock += 8 * bars

    def notes(seq):
        return [(pitch(w), d) for w, d in seq]

    for n, (bars, sec) in enumerate(arrangement(src)):
        start, key = clock, sec[3:]
        sections.append((clock, f"{ROMAN[n]}. {TITLES[sec]}"))
        if sec == "secGOLGOTHA":                        # the solo lines, between silences, as in the short form
            for b, p in arrangement(src, "secGOLGOTHA"):
                body = re.search(rf"^const {p} = (.*)$", src, re.M)
                line = next((x for x in re.findall(r"\b[A-Z][A-Z_]+\b", body.group(1)) if x in sung), None) if body else None
                if line:
                    seq, k = sung[line]
                    part(b, {"S": notes(seq)}, said={"S": [(0, k, len(underlay(k)))]}, over=("S", GOLGOTHA[p]))
                else:
                    part(b, {}, over=("S", GOLGOTHA[p]))
        elif sec == "secAMEN":                          # the phrygian cadence, a note to a voice
            for b, p in arrangement(src, "secAMEN"):
                chord = re.search(rf'\b{p} = "\[(.*?)\]"', src)
                part(b, {v: [(pitch_of(x), 8 * b)] for v, x in zip("BTAS", chord.group(1).split(","))} if chord else {})
        elif key in made:                               # a section made by rule
            m = made[key]
            part(bars, {v: notes(m["lines"][v]) for v in ORDER}, said=m["said"], free=True)
        else:                                           # the instruments alone
            part(bars, {})
        assert clock - start == 8 * bars, (sec, (clock - start) / 8, bars)
    return voices, sections, parts, []

LY_LONG = LY.replace(
    "% On These Two Hang: the choir's lines, for SATB\n% The choir's part of the track at canon-lawyer.ca/music/, bar for bar.\n"
    "% Written by counterpoint.py --ly from the lines the track plays; do not edit by hand.\n"
    "% Engrave with GNU LilyPond: lilypond on-these-two-hang.ly",
    "% On These Two Hang, the long form: the choir's lines, for SATB\n% The choir's part of the long form at canon-lawyer.ca/music/, bar for bar.\n"
    "% Written by counterpoint.py --long --ly from the lines the track plays; do not edit by hand.\n"
    "% Engrave with GNU LilyPond: lilypond on-these-two-hang-long.ly").replace(
    'subtitle = "A double fugue for the household"', 'subtitle = "The long form: a double fugue for the household"').replace(
    'composer = "Notes made by rule: counterpoint.py"', 'composer = "Notes made by rule: counterpoint.py --long"')
LY_LONG = re.sub(r"\\markup \\justify \{\{\n.*?\n\}\}\n", lambda m: r"""\markup \justify {{
  The choir's part of the long form, bar for bar, in mode III, E phrygian. The notes are written out by counterpoint.py
  from the same lines the track plays, and the bar numbers are the track's. The first eight bars, I. Pendet, belong to
  the instruments and to the lawyer's question, so the score begins at bar 9. The two subjects are carved from their
  Latin words, a note to a syllable, as in the short form, and are taken through the old procedures of the fugue: the
  head they share in imitation, falling a step a bar (Caput); both subjects upside down about mi, the mirror (Speculum);
  the first subject four times slower in the bass, the Law held (Lex); the entries drawn closer together (In unum); the
  two subjects at once, in the mirror, and with the voices exchanged (Duobus); and a long E in the bass under the last
  entries (Fundamentum). Every statement, upright, inverted or long, has its words under it; in Caput the leader sings
  the first commandment's words and the follower the second's. The free voices were found by a search under Fux's
  rules; they have no text yet. In Golgotha the choir rests through the darkness, the veil and the tomb.
}}
""", LY_LONG, count=1, flags=re.S)
LY_LONG = re.sub(r"\\markup \\small \\italic \\justify \{\{\n.*?\n\}\}\n", lambda m: r"""\markup \small \italic \justify {{
  Matthew 22:37, 22:39, 27:46, 27:47 and 27:54; John 19:30 (Vulgate). The heading is Matthew 22:40 (King James Version).
  Speculum: “For now we see through a glass, darkly” (1 Corinthians 13:12). In unum: “that also he should gather together
  in one the children of God that were scattered abroad” (John 11:52). Fundamentum: “For other foundation can no man lay
  than that is laid, which is Jesus Christ” (1 Corinthians 3:11). After the cadence the track keeps four bars of
  silence, and in them “If ye love me, keep my commandments” (John 14:15).
}}
""", LY_LONG, count=1, flags=re.S)

def engrave_long():
    def arg(flag):
        k = sys.argv.index(flag)
        if k + 1 >= len(sys.argv):
            sys.exit(f"counterpoint.py: {flag} needs a path")
        return Path(sys.argv[k + 1])
    made = piece_long()
    if "--ly" in sys.argv:
        write_ly(arg("--ly"), *made, template=LY_LONG)
        print(f"counterpoint.py: the long form's score, in LilyPond, at {arg('--ly')}")
    if "--midi" in sys.argv:
        write_midi(arg("--midi"), *made, stem="on-these-two-hang-long", title="On These Two Hang, the long form")
        print(f"counterpoint.py: the long form in MIDI, a file to a voice and one for all four, in {arg('--midi')}")

def main_long():
    if "--ly" in sys.argv or "--midi" in sys.argv:
        return engrave_long()
    lines, findings, made, found = build_long()
    for sec, f in findings.items():
        what = "join" if "/" in sec else "audit"
        print(f"// {what} {sec}: " + ("every half note keeps the rules" if not f else "; ".join(f)), file=sys.stderr)
    for sec, f in found.items():
        print(f"// found {sec}: {f}", file=sys.stderr)
    if "--check" in sys.argv:
        bad = unquoted(lines, LONG)
        if bad:
            sys.exit("counterpoint.py: the long track does not quote these as made: " + ", ".join(bad))
        wrong = misarranged(made, LONG.read_text(encoding="utf-8"))
        if wrong:
            sys.exit("counterpoint.py: " + "; ".join(wrong))
        if any(findings.values()):
            sys.exit("counterpoint.py: the long form breaks a rule; see the audit above")
        print(f"counterpoint.py: the long form, {len(lines)} lines, each carved or found by rule, quoted as made, "
              f"every section and join audited")
        return
    for k, v in lines.items():
        print(f"const {k} = '{v}'")

def main():
    if "--long" in sys.argv:
        return main_long()
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
