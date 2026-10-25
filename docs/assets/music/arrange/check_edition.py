#!/usr/bin/env python3
"""check_edition.py: read the organ edition back and compare it with the track and the choir.

    python3 arrange/check_edition.py --site PATH [--long] [--dir DIR]

It reads what LilyPond made from the edition, not the code that wrote it:
  * <stem>-organ.mid, LilyPond's MIDI of the edition (a track to a staff, and the lyrics);
  * <stem>-organ.ly, only for what MIDI cannot carry: the words' hyphens, the section
    marks and the spoken line;
and compares them with
  * the published choir parts, <stem>-S.mid ... -B.mid (notes and words, note for note);
  * Strudel's engine, every event of every layer the track plays (arrange/events.mjs),
    sorted into layers here by its own reading of the track's orbits.
It prints one line per check with its numbers, and exits 1 if a check fails. Standard
library only; Node 18+ for the engine.
"""
import json, re, subprocess, sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
Q = 4                                               # sixteenths to a quarter
BAR = 16
failed = []

def report(ok, line):
    print(("ok    " if ok else "FAIL  ") + line)
    if not ok:
        failed.append(line)

# ---------------------------------------------------------------- MIDI, read independently
def smf(path):
    b = Path(path).read_bytes()
    assert b[:4] == b"MThd"
    ntr, div = int.from_bytes(b[10:12], "big"), int.from_bytes(b[12:14], "big")
    i, tracks = 8 + int.from_bytes(b[4:8], "big"), []
    def vlq(i):
        n = 0
        while True:
            c = b[i]; i += 1; n = (n << 7) | (c & 0x7F)
            if c < 0x80:
                return n, i
    for _ in range(ntr):
        end = i + 8 + int.from_bytes(b[i + 4:i + 8], "big"); i += 8
        t, st, ev = 0, None, []
        while i < end:
            dt, i = vlq(i); t += dt
            if b[i] == 0xFF:
                k = b[i + 1]; n, i = vlq(i + 2); ev.append((t, "meta", k, b[i:i + n])); i += n
            elif b[i] in (0xF0, 0xF7):
                n, i = vlq(i + 1); i += n
            else:
                if b[i] & 0x80:
                    st = b[i]; i += 1
                n = 1 if st & 0xF0 in (0xC0, 0xD0) else 2
                ev.append((t, "midi", st, tuple(b[i:i + n]))); i += n
        tracks.append(ev)
    return div, tracks

def notes_of(track, div):
    """[(onset, key, length)] in sixteenths."""
    unit, on, out = div // Q, defaultdict(list), []
    for t, kind, st, d in track:
        if kind != "midi" or st & 0xF0 not in (0x80, 0x90):
            continue
        key = (st & 15, d[0])
        if st & 0xF0 == 0x90 and d[1]:
            on[key].append(t)
        elif on[key]:
            s = on[key].pop(0)
            assert s % unit == 0 and (t - s) % unit == 0, ("off the sixteenth grid", s, t)
            out.append((s // unit, d[0], (t - s) // unit))
    return sorted(out)

def name_of(track):
    return next((d.decode() for _, k, s, d in track if k == "meta" and s == 3), "")

# ---------------------------------------------------------------- the track, read independently
def engine(track, bars):
    out = subprocess.run(["node", str(HERE / "events.mjs"), str(track), str(bars)],
                         capture_output=True, text=True, check=True).stdout
    ev = []
    for e in json.loads(out):
        v = e["value"]
        t, z = Fraction(e["begin"]) * BAR, Fraction(e["end"]) * BAR
        assert t.denominator == 1 and z.denominator == 1
        ev.append((int(t), int(z - t), v))
    return ev

def layer(v):
    """The track's orbits, as its own comment names them: 1 the clock, 2 the wheel, 3 the
    chanted lines, 4 organ, 5 the veil and the earth, 6 choir, 7 bells."""
    o, s = v.get("orbit"), v.get("s")
    if o == 6:
        return {0.62: "S", 0.42: "A", 0.56: "T", 0.48: "B", 0.5: "S"}.get(v.get("pan"), "chord")
    if o == 4:
        if v["attack"] == 0.05:
            return "organ-loud" if v["gain"] > 0.15 else "organ"
        return {0.4: "viri", 1: "pedal", 0.1: "amen-organ"}[v["attack"]]
    if o == 7:
        return "canticle" if s == "gm_recorder" else "bells"
    if o == 2:
        return "wheel"
    if o == 1:
        return {"bd": "kick", "hh": "hats", "rim": "hammer"}[s]
    if o == 5:
        return {"rim": "rocks", "gm_timpani": "timpani", "white": "veil", "brown": "quake",
                "sine": "quake-tone", "pink": "whirlwind"}[s]
    if o == 3:
        return "vox"
    raise SystemExit(f"check_edition.py: an event on no orbit it knows: {v}")

def held(notes):
    """Notes of one pitch that follow without a gap, joined: a drone struck every bar."""
    out = []
    for t, k, d in sorted(notes, key=lambda x: (x[1], x[0])):
        if out and out[-1][1] == k and out[-1][0] + out[-1][2] == t:
            out[-1] = (out[-1][0], k, out[-1][2] + d)
        else:
            out.append((t, k, d))
    return sorted(out)

def bars(xs):
    return sorted({t // BAR + 1 for t in xs})

def runs(bs):
    out = []
    for b in bs:
        if out and b == out[-1][1] + 1:
            out[-1][1] = b
        else:
            out.append([b, b])
    return ", ".join(f"{a}-{z}" if z > a else f"{a}" for a, z in out) or "none"

# ---------------------------------------------------------------- the checks
def main():
    args = sys.argv[1:]
    site = Path(args[args.index("--site") + 1])
    long_form = "--long" in args
    music = site / "docs" / "assets" / "music"
    stem = "on-these-two-hang-long" if long_form else "on-these-two-hang"
    track = music / ("on-these-two-hang.long.strudel.js" if long_form else "on-these-two-hang.strudel.js")
    folder = Path(args[args.index("--dir") + 1]) if "--dir" in args else music / "scores"
    src = track.read_text(encoding="utf-8")
    plan = re.search(r"^arrange\((.*?)\n\)", src, re.S | re.M).group(1)
    sections = [(int(n), name) for n, name in re.findall(r"\[(\d+),\s*(sec\w+)\]", plan)]
    N = sum(n for n, _ in sections)
    print(f"== {stem}: {N} bars in the track's arrangement")

    div, tracks = smf(folder / f"{stem}-organ.mid")
    by = {name_of(t).split(":")[0]: t for t in tracks if name_of(t)}
    mine = {k: notes_of(t, div) for k, t in by.items()}
    ly = (folder / f"{stem}-organ.ly").read_text(encoding="utf-8")

    # 1. the choir, against the published parts
    print("-- 1. the choir is unchanged")
    words_ly = {}
    for v, var in zip("SATB", ("soprano", "alto", "tenor", "bass")):
        block = re.search(rf"^{var}Words = \\lyricmode {{(.*?)^}}", ly, re.S | re.M).group(1)
        toks = re.findall(r'"((?:[^"\\]|\\.)*)"|(--)|\\repeat unfold (\d+)', block)
        syl = []
        for word, hy, skip in toks:
            if word:
                syl.append([word, False])
            elif hy:
                syl[-1][1] = True
        words_ly[v] = [tuple(x) for x in syl]
    lyric_tracks = [[(t // (div // Q), d.decode()) for t, k, s, d in tr if k == "meta" and s == 5]
                    for tr in tracks if any(k == "meta" and s == 5 for _, k, s, _ in tr)]
    for v, staff in zip("SATB", ("Soprano", "Alto", "Tenor", "Bass")):
        pdiv, ptr = smf(music / "scores" / f"{stem}-{v}.mid")
        pub = notes_of(ptr[1], pdiv)
        pwords = [(t // (pdiv // Q), d.decode()) for t, k, s, d in ptr[1] if k == "meta" and s == 5]
        got = mine[staff]
        onsets = {t for t, _, _ in got}
        lt = [x for x in lyric_tracks if x and all(t in onsets for t, _ in x) and len(x) == len(pwords)]
        lt = next((x for x in lt if [w for _, w in x] == [w.rstrip("-") for _, w in pwords]), lt[0] if lt else [])
        same_words = [(t, w) for t, w in lt] == [(t, w.rstrip("-")) for t, w in pwords]
        same_hyphens = words_ly[v] == [(w.rstrip("-"), w.endswith("-")) for _, w in pwords]
        diff = next((k for k, (a, b) in enumerate(zip(got, pub)) if a != b), None)
        report(got == pub and same_words and same_hyphens,
               f"{v}: {len(got)} notes against {len(pub)} published, identical: {got == pub}"
               + (f" (first difference at note {diff})" if diff is not None else "")
               + f"; {len(lt)} syllables at the same onsets: {same_words}; hyphens as published: {same_hyphens}")

    # 2. the instruments, layer by layer, against the engine
    print("-- 2. the edition plays what the track plays")
    ev = engine(track, N)
    L = defaultdict(list)
    for t, d, v in ev:
        L[layer(v)].append((t, v.get("midi"), d, v))
    # The organ, staff by staff: its strokes (onset, key), and how long each key is held.
    # A key struck again while it is held (two voices on one note in one hand) cannot be
    # paired note by note in MIDI, so a note of the track is found by its stroke and by
    # the key being held for its whole length.
    org = {k: mine[k] for k in ("Organ right hand", "Organ left hand", "Organ pedal")}
    strokes = {s: Counter((t, k) for t, k, d in org[s]) for s in org}
    cover = {s: defaultdict(list) for s in org}
    for s in org:
        for t, k, d in sorted(org[s]):
            iv = cover[s][k]
            if iv and t <= iv[-1][1]:
                iv[-1][1] = max(iv[-1][1], t + d)
            else:
                iv.append([t, t + d])
    used = Counter()
    def take(t, k, d, staves=("Organ right hand", "Organ left hand", "Organ pedal"), shorter=False):
        for s in staves:
            if used[(s, t, k)] < strokes[s][(t, k)]:
                end = next((z for a, z in cover[s][k] if a <= t < z), t)
                if end >= t + d or shorter:
                    used[(s, t, k)] += 1
                    return s if end >= t + d else (s, "shorter")
        return None
    # the wheel, exact, on the left hand
    w = [(t, k, d) for t, k, d, _ in L["wheel"]]
    got = [x for x in w if take(*x, staves=("Organ left hand",))]
    report(len(got) == len(w), f"wheel: {len(got)} of {len(w)} notes on the organ's left hand, same onset, pitch and length; "
                               f"bars {runs(bars(t for t, _, _ in w))}")
    cuts = Counter((v["cutoff"], v["gain"]) for *_, v in L["wheel"])
    print(f"      the wheel's low-pass and gain in the track: {dict(cuts)}")
    # the household: viri and canticle
    for name in ("canticle", "viri"):
        xs = [(t, k, d) for t, k, d, _ in L[name]]
        got = [x for x in xs if take(*x, staves=("Organ right hand", "Organ left hand"))]
        missing = [x for x in xs if x not in got]
        print(f"{'ok   ' if name == 'canticle' and not missing else 'note '} {name}: {len(got)} of {len(xs)} notes on the manuals, exact; "
              f"not played: bars {runs(bars(t for t, _, _ in missing))}")
        if name == "canticle" and missing:
            failed.append("canticle")
    # the pedal's fifth, held
    fifth = held([(t, k, d) for t, k, d, _ in L["pedal"]])
    got = [x for x in fifth if take(*x, staves=("Organ pedal",))]
    report(len(got) == len(fifth), f"pedal fifth: {len(got)} of {len(fifth)} held notes (the track strikes it each bar) on the pedal; "
                                   f"bars {runs(bars(u for t, _, d in fifth for u in range(t, t + d, BAR)))}")
    # the quake's tone: a sine on E1, the pedal's E on 16' (written an octave up)
    qt = held([(t, k + 12, d) for t, k, d, _ in L["quake-tone"]])
    got = [x for x in qt if take(*x, staves=("Organ pedal",))]
    print(f"note  quake tone (E1): {len(got)} of {len(qt)} on the pedal (E, 16'); the rest under the bass: bars "
          f"{runs(bars(x[0] for x in qt if x not in got))}")
    # the choir doubled: each organ() event of the track, by voice
    choir = defaultdict(list)
    for t, d, v in ev:
        if v.get("orbit") == 6 and "pan" in v:
            choir[(t, v["midi"], d)].append(layer(v))
    doubled = Counter(); short = Counter(); left = defaultdict(list)
    loud = [(t, k, d) for t, k, d, _ in L["organ-loud"]]
    voiced = [(t, k, d, choir[(t, k, d)].pop(0) if choir[(t, k, d)] else "?") for t, k, d, v in L["organ"]]
    later = []
    for t, k, d, voice in voiced:                   # first every note held its whole length ...
        if take(t, k, d):
            doubled[voice] += 1
        else:
            later.append((t, k, d, voice))
    for t, k, d, voice in later:                    # ... then the same stroke, held less: the hand moves on at a bar line
        if take(t, k, d, shorter=True):
            short[voice] += 1
        else:
            left[voice].append(t)
    total = Counter(choir_v for t, k, d, v in L["organ"] for choir_v in [None])
    for v in "SATB":
        n = doubled[v] + short[v] + len(left[v])
        line = (f"choir doubled, {v}: {doubled[v] + short[v]} of {n} organ notes of the track on the organ "
                f"({short[v]} shortened at a bar line); left to the choir: {len(left[v])}, bars {runs(bars(left[v]))}")
        if v == "B":
            inside = [t for t in left[v] if any(x[0] <= t < x[0] + x[2] and x[1] == 40 for x in fifth)]
            report(len(inside) == len(left[v]), line + (f" (held in the pedal's fifth: {len(inside)})" if inside else ""))
        else:
            print("note  " + line)
    print(f"      the Law held (organ(LEX_B) louder): {len(loud)} notes, all on the pedal with the bass: "
          f"{all(any(x[0] == t and x[1] == k for x in org['Organ pedal']) for t, k, d in loud)}")
    # the Amen
    amen = [(t, k, d) for t, k, d, _ in L["amen-organ"]]
    chord = [(t, k, d) for t, k, d, v in L["chord"]]
    got = [x for x in chord if take(*x)]
    report(len(got) == len(chord), f"Amen: {len(got)} of {len(chord)} chord notes on the organ (the track's organ has "
                                   f"{len(amen)}, the second chord; the first is added under the choir)")
    # nothing else on the organ
    extra = [(s, x, n - used[(s,) + x]) for s in org for x, n in strokes[s].items() if used[(s,) + x] < n]
    report(not extra, f"organ: every note it plays is a note of the track: {sum(len(x) for x in org.values())} notes, "
                      f"{len(extra)} unexplained {extra[:5] if extra else ''}")
    # the bells
    bl = sorted((t, k, d) for t, k, d, _ in L["bells"])
    mb = sorted(mine["Bells"])
    report(bl == mb, f"bells: {len(mb)} notes against the track's {len(bl)} (tintinnabuli and the Amen's chord), identical: {bl == mb}")
    # the percussion: onsets, by instrument
    drums = next(notes_of(tr, div) for tr in tracks if name_of(tr).startswith("Percussion"))
    keys = Counter(k for _, k, _ in drums)
    on = defaultdict(list)
    for t, k, d in drums:
        on[k].append((t, d))
    def onsets(k):
        return {t for t, _ in on[k]}
    plays = lambda name, key: [t for t, _, _, _ in L[name] if t in onsets(key)]
    for name, key, what in (("kick", 36, "bass drum"), ("hats", 76, "woodblock"), ("hammer", 77, "temple block"),
                            ("rocks", 77, "temple block"), ("timpani", 41, "timpani (E)"), ("veil", 51, "suspended cymbal"),
                            ("whirlwind", 49, "wind machine"), ("quake", 36, "bass drum roll")):
        xs = [t for t, _, _, _ in L[name]]
        got = plays(name, key)
        if name == "quake":
            got = [t for t in xs if any(s == t and d >= BAR for s, d in on[key])]
        if name == "whirlwind":
            got = [t for t in xs if any(s <= t < s + d for s, d in on[key])]
        miss = sorted(set(xs) - set(got))
        print(f"note  {name} -> {what}: {len(got)} of {len(xs)} onsets; not played: bars {runs(bars(miss))}")
    stray = [(t, k) for t, k, d in drums if not any(t == x[0] for n in ("kick", "hats", "hammer", "rocks", "timpani", "veil",
                                                                          "whirlwind", "quake") for x in L[n])]
    report(not stray, f"percussion: every stroke is on an onset of the track: {len(drums)} strokes, {len(stray)} not")
    vox = Counter(v["s"] for *_, v in L["vox"])
    print(f"note  recorded voices dropped: {sum(vox.values())} ({', '.join(sorted(vox))})")

    # 3. bars and times
    print("-- 3. bars and times")
    end = max(t for tr in tracks for t, *_ in tr) // (div * 4)
    tempo = [60_000_000 // int.from_bytes(d, "big") for tr in tracks for t, k, s, d in tr if k == "meta" and s == 0x51]
    report(end == N and tempo == [120], f"MIDI: {end} bars at {tempo} BPM, track {N} bars, {N * 2 // 60}:{N * 2 % 60:02d}")
    marks = re.search(r"^marks = {(.*?)^}", ly, re.S | re.M).group(1)
    at, found = 0, []
    for tok in re.finditer(r"s1\*(\d+)|s16\*(\d+)|\\sectionLabel \\markup \\line { \\bold \"([^\"]+)\" \\hspace #1 \\italic \"bar (\d+) \((\d+):(\d+)\)\"|If ye love me", marks):
        if tok.group(1):
            at += int(tok.group(1)) * BAR
        elif tok.group(2):
            at += int(tok.group(2))
        elif tok.group(3):
            found.append((tok.group(3), at // BAR + 1, int(tok.group(4)), int(tok.group(5)) * 60 + int(tok.group(6))))
        else:
            spoken = at // BAR + 1
    at, want = 1, []
    for n, sec in sections:
        want.append((at, (at - 1) * 2)); at += n
    ok = [(b, s) for _, b, lb, s in found] == want and all(b == lb for _, b, lb, _ in found)
    report(ok, f"section marks: {len(found)} of {len(sections)}, each at its bar and time: "
               + "; ".join(f"{name} {b} ({s // 60}:{s % 60:02d})" for name, b, _, s in found))
    vb = [t // BAR + 1 for t, k, d, v in L["vox"] if v["s"] == "if_ye_love_me"]
    report(vb == [spoken], f"the spoken line at bar {spoken}, where the track's recording of it is (bar {vb})")

    # 5. ranges
    print("-- 5. ranges (MIDI note numbers; middle C = 60 = C4)")
    nm = lambda m: "C C# D D# E F F# G G# A A# B".split()[m % 12] + str(m // 12 - 1)
    for k in ("Soprano", "Alto", "Tenor", "Bass", "Organ right hand", "Organ left hand", "Organ pedal", "Bells"):
        ks = [x[1] for x in mine[k]]
        extra = ""
        if k == "Organ pedal":
            extra = f"; within C2-G4 (36-67): {36 <= min(ks) and max(ks) <= 67}"
        if k.startswith("Organ") and k != "Organ pedal":
            extra = f"; within a manual's C2-C7: {36 <= min(ks) and max(ks) <= 96}"
        if k == "Bells":
            # the glockenspiel reads the 8va passages without the 8va: every note above C6 must be under one
            block = re.search(r"^bells = {(.*?)^}", ly, re.S | re.M).group(1)
            high, under, over = False, 0, 0
            step = {"c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11}
            for tok in re.finditer(r"\\ottava #(\d)|(?<![\\\w])([a-g])(is|es)?([',]*)(?=[\d~ >])", block):
                if tok.group(1) is not None:
                    high = tok.group(1) == "1"; continue
                m = 48 + step[tok.group(2)] + {"is": 1, "es": -1, None: 0}[tok.group(3)] \
                    + 12 * (tok.group(4).count("'") - tok.group(4).count(","))
                if m > 84:
                    under += high; over += not high
            extra = (f"; pitches {' '.join(nm(m) for m in sorted(set(ks)))}; 3-octave handbells (C4-C7 written): "
                     f"{60 <= min(ks) and max(ks) <= 96}; 2-octave (G4-G6): below G4 {sum(1 for m in ks if m < 67)} notes, "
                     f"above G6 {sum(1 for m in ks if m > 91)}; glockenspiel (G3-C6 written): above C6 "
                     f"{sum(1 for m in ks if m > 84)} notes, written as {under + over} signs (ties count twice): {under} under 8va, {over} not")
            if over:
                failed.append("bells above C6 outside 8va")
        print(f"      {k}: {nm(min(ks))}-{nm(max(ks))} ({min(ks)}-{max(ks)}){extra}")
        if k == "Organ pedal" and not (36 <= min(ks) and max(ks) <= 67):
            failed.append("pedal range")
    print(f"      Percussion keys: {dict(sorted(keys.items()))} (36 bass drum, 41 timpani E, 49 wind, 51 cymbal, 76 woodblock, 77 temple block)")
    print(("FAILED: " + "; ".join(failed)) if failed else "all checks pass")
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()
