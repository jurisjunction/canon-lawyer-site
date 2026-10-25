#!/usr/bin/env python3
"""organ_edition.py: "On These Two Hang" for a parish, arranged by rule from the track.

The track is techno: a 909 kick, hi-hats, a square-wave arpeggio. No parish choir will
sing it as techno. This makes a church edition from what the track plays: SATB choir and
organ, with optional bells and optional percussion, one player each.

    python3 arrange/organ_edition.py --site PATH [--long] [--out DIR] [--engrave]

It reads three things and nothing else:
  1. every event the track plays, from Strudel's own engine (arrange/events.mjs);
  2. the published choir parts, the MIDI that counterpoint.py --midi wrote beside the
     choir score (<stem>-S.mid ... -B.mid), for the choir's notes and their Latin. They
     are checked against the engine's choir, note for note, before they are used;
  3. the track's text, for the names of its sections and their parts (arrange(...)).
It writes <stem>-organ.ly (DIR defaults to the site's docs/assets/music/scores/): one
LilyPond file with three books, the full score with a preface (<stem>-organ.pdf), the
bells part (-bells.pdf) and the percussion part (-percussion.pdf), and a MIDI file with a
track to a staff (<stem>-organ.mid). With --engrave it runs LilyPond on it.

The choir is not arranged. Its notes, its words, its markings and the way they are
engraved are the published score's (the engraving rules are counterpoint.py's, copied
below). The edition writes out the short form's repeat, because the instruments differ
the second time, and adds bars 1-8 and the four bars of silence after the Amen.

Everything else is arranged by the rules in section 4 below, and NOTE.md says why.
Standard library only, and Node 18+ for the engine. Made 25 October 2026, by Claude
with Richard Verver.
"""
import json, re, shutil, subprocess, sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORDER = "SATB"
VOICE = {"S": "Soprano", "A": "Alto", "T": "Tenor", "B": "Bass"}
BAR = 16                                            # the edition counts in sixteenths: a bar is 16

# ---------------------------------------------------------------- 1. what the track plays
def track_events(track, bars):
    """Every event with an onset in bars [0, bars), from Strudel's engine."""
    node = shutil.which("node") or sys.exit("organ_edition.py: needs node (18+) for Strudel's engine")
    out = subprocess.run([node, str(HERE / "events.mjs"), str(track), str(bars)],
                         capture_output=True, text=True, check=True).stdout
    return [dict(begin=Fraction(e["begin"]), end=Fraction(e["end"]), value=e["value"]) for e in json.loads(out)]

# The track names its own orbits: 1 the clock, 2 the wheel, 3 the chanted lines, 4 organ,
# 5 the veil and the earth, 6 choir, 7 bells. An event's orbit and sound say what layer it
# belongs to; on the organ's orbit the envelope tells its four uses apart. Anything not
# named here stops the arranger: it does not guess.
PAN = {0.62: "S", 0.42: "A", 0.56: "T", 0.48: "B", 0.5: "solo"}
ORGAN_BY_ATTACK = {0.05: "organ", 0.4: "viri", 1: "pedal", 0.1: "amen-organ"}
PERC = {(1, "bd"): "kick", (1, "hh"): "hats", (1, "rim"): "hammer", (5, "rim"): "rocks",
        (5, "gm_timpani"): "timpani", (5, "white"): "veil", (5, "brown"): "quake",
        (5, "sine"): "quake-tone", (5, "pink"): "whirlwind"}

def layer_of(v):
    s, orbit = v.get("s"), v.get("orbit")
    if orbit == 6 and s == "gm_choir_aahs":
        return "choir:" + (PAN[v["pan"]] if "pan" in v else "chord")
    if orbit == 4 and s == "gm_church_organ":
        return ORGAN_BY_ATTACK[v["attack"]]
    if orbit == 7 and s == "gm_celesta":
        return "bells" if "pan" in v else "amen-bells"
    if orbit == 7 and s == "gm_recorder":
        return "canticle"
    if orbit == 2 and s == "square":
        return "wheel"
    if (orbit, s) in PERC:
        return PERC[(orbit, s)]
    if orbit == 3:
        return "vox:" + s
    raise SystemExit(f"organ_edition.py: an event it has no rule for: {v}")

class Note:
    """One sound in the edition, in sixteenths from bar 1, with the event it came from."""
    def __init__(self, t, d, midi, layer, value=None):
        self.t, self.d, self.midi, self.layer, self.value = t, d, midi, layer, value or {}
    @property
    def end(self):
        return self.t + self.d
    def __repr__(self):
        return f"<{self.layer} {self.t}+{self.d} {self.midi}>"

def sixteenths(x):
    t = x * BAR
    if t.denominator != 1:
        raise SystemExit(f"organ_edition.py: an event off the sixteenth grid at bar {float(x) + 1}")
    return int(t)

def layers(events):
    out = defaultdict(list)
    for e in events:
        name = layer_of(e["value"])
        t, end = sixteenths(e["begin"]), sixteenths(e["end"])
        out[name].append(Note(t, end - t, e["value"].get("midi"), name, e["value"]))
    for v in out.values():
        v.sort(key=lambda n: (n.t, n.midi or 0))
    return out

# ---------------------------------------------------------------- 2. the form, from the track's text
ROMAN = "I II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI".split()

def arrangement(src, const=None):
    """The [bars, part] items of one of the track's arrange(...) calls (the last one, if no
    const). As counterpoint.py reads them."""
    head = rf"^const {const} = (?:stack\()?arrange\(" if const else r"^arrange\("
    block = re.search(head + r"(.*?)\n\)", src, re.S | re.M).group(1)
    items = []
    for m in re.finditer(r"\[(\d+),\s*", block):
        part = next(t for t in re.findall(r"[A-Za-z_]\w*", block[m.end():]) if t not in ("stack", "satb", "note"))
        items.append((int(m.group(1)), part))
    return items

def title(sec):
    name = re.sub(r"_(I|II|III|IV|V)$", "", sec[3:]).replace("_", " ").lower()
    return name[0].upper() + name[1:]

def form(src):
    """The sections [(first bar, bars, const, title, numeral)] and the parts inside the
    sections that are arrangements of parts [(first bar, bars, section const, part)]."""
    secs, parts, at = [], [], 0
    for n, (bars, sec) in enumerate(arrangement(src)):
        secs.append((at, bars, sec, title(sec), ROMAN[n]))
        if re.search(rf"^const {sec} = (?:stack\()?arrange\(", src, re.M):
            k = at
            for b, p in arrangement(src, sec):
                parts.append((k, b, sec, p)); k += b
        at += bars
    return secs, parts, at

def clock(bar0):
    s = 2 * bar0                                    # 120 to the quarter, 4/4: a bar is two seconds
    return f"{s // 60}:{s % 60:02d}"

# ---------------------------------------------------------------- 3. the choir, as published
def read_smf(path):
    """A small reader for Standard MIDI Files: (division, [[(tick, kind, status, data)]])."""
    b = Path(path).read_bytes()
    assert b[:4] == b"MThd", path
    ntr, div = int.from_bytes(b[10:12], "big"), int.from_bytes(b[12:14], "big")
    def vlq(i):
        n = 0
        while True:
            c = b[i]; i += 1; n = (n << 7) | (c & 0x7F)
            if not c & 0x80:
                return n, i
    i, tracks = 8 + int.from_bytes(b[4:8], "big"), []
    for _ in range(ntr):
        assert b[i:i + 4] == b"MTrk", path
        end = i + 8 + int.from_bytes(b[i + 4:i + 8], "big"); i += 8
        t, ev, status = 0, [], None
        while i < end:
            dt, i = vlq(i); t += dt
            if b[i] == 0xFF:
                kind = b[i + 1]; n, i = vlq(i + 2)
                ev.append((t, "meta", kind, b[i:i + n])); i += n
            elif b[i] in (0xF0, 0xF7):
                n, i = vlq(i + 1); i += n
            else:
                if b[i] & 0x80:
                    status = b[i]; i += 1
                size = 1 if status & 0xF0 in (0xC0, 0xD0) else 2
                ev.append((t, "midi", status, tuple(b[i:i + size]))); i += size
        tracks.append(ev)
    return div, tracks

def midi_notes(track, unit):
    """[(onset, key, length)] of one track, in units of `unit` ticks."""
    on, out = {}, []
    for t, kind, st, data in track:
        if kind != "midi" or st & 0xF0 not in (0x80, 0x90):
            continue
        key = (st & 0x0F, data[0])
        if st & 0xF0 == 0x90 and data[1] > 0:
            on.setdefault(key, []).append(t)
        elif on.get(key):
            s = on[key].pop(0)
            out.append((s, data[0], t - s))
    assert not any(on.values()), "a note that never ends"
    if any(s % unit or d % unit for s, _, d in out):
        sys.exit("organ_edition.py: a note off the grid in the published MIDI")
    return sorted((s // unit, k, d // unit) for s, k, d in out)

def published_choir(stem):
    """{voice: [(t8, midi, d8, (syllable, word goes on) or None)]} from <stem>-S.mid etc."""
    out = {}
    for v in ORDER:
        div, tracks = read_smf(f"{stem}-{v}.mid")
        tr = tracks[1]
        eighth = div // 2
        words = {t // eighth: d.decode("utf-8") for t, kind, st, d in tr if kind == "meta" and st == 0x05}
        notes = midi_notes(tr, eighth)
        out[v] = [(t, k, d, (words[t].rstrip("-"), words[t].endswith("-")) if t in words else None) for t, k, d in notes]
        assert len(words) == sum(1 for n in out[v] if n[3]), (v, "a syllable on no note")
    return out

def engine_choir(L):
    """The choir as the engine plays it: {voice: [(t8, midi, d8)]}; the Amen's chords a note
    to a voice, from the bass up."""
    out = {v: [] for v in ORDER}
    for name, notes in L.items():
        if not name.startswith("choir:"):
            continue
        who = name.split(":")[1]
        if who == "chord":
            at = defaultdict(list)
            for n in notes:
                at[n.t].append(n)
            for t, ch in at.items():
                assert len(ch) == 4, ("the Amen's chord is not four notes", t)
                for v, n in zip("BTAS", sorted(ch, key=lambda n: n.midi)):
                    out[v].append((n.t // 2, n.midi, n.d // 2))
        else:
            for n in notes:
                assert n.t % 2 == 0 and n.d % 2 == 0, n
                out["S" if who == "solo" else who].append((n.t // 2, n.midi, n.d // 2))
    return {v: sorted(x) for v, x in out.items()}

# ---------------------------------------------------------------- 4. the arrangement, by rule
WHEEL_DYN = {500: "pp", 1800: "p", 2400: "mp"}      # the wheel's low-pass, as dynamics on the organ

def merged(notes):
    """A drone the track strikes again every bar, as one held note: contiguous notes of
    the same pitch joined."""
    out = []
    for n in sorted(notes, key=lambda n: (n.midi, n.t)):
        if out and out[-1].midi == n.midi and out[-1].end == n.t:
            out[-1] = Note(out[-1].t, out[-1].d + n.d, n.midi, n.layer, out[-1].value)
        else:
            out.append(Note(n.t, n.d, n.midi, n.layer, n.value))
    return sorted(out, key=lambda n: (n.t, n.midi))

def bars_of(notes):
    """The bars a set of notes sounds in."""
    return {b for n in notes for b in range(n.t // BAR, (n.end - 1) // BAR + 1)}

class Edition:
    """The arrangement: every staff's notes, and a log of what the rules did."""

    def __init__(self, L, choir, secs, parts, total, long_form):
        self.L, self.choir, self.secs, self.parts, self.N, self.long = L, choir, secs, parts, total, long_form
        self.log = defaultdict(list)
        self.part_at = {p: (b0, b) for b0, b, _, p in parts}
        self.organ()
        self.bells()
        self.percussion()

    def part(self, name, k=0):
        """The first bar and length of a part of a section (k: which, if it comes more than once)."""
        found = [(b0, b) for b0, b, _, p in self.parts if p == name]
        return found[k]

    # ---------------- the organ
    def organ(self):
        L, N = self.L, self.N
        # the colla parte doubling: each organ() event is a choir note; find its voice
        sung = defaultdict(list)
        for v in ORDER:
            for n in L.get("choir:" + v, []):
                sung[(n.t, n.end, n.midi)].append(v)
        bass = {k for k, vs in sung.items() if "B" in vs}
        dbl = defaultdict(list)
        self.reinforced = []                       # organ(LEX_B, .07): the Law held, louder
        for n in L["organ"]:
            key = (n.t, n.end, n.midi)
            if n.value.get("gain", 0) > 0.15:
                assert key in bass, n
                self.reinforced.append(n); continue
            v = sung[key].pop(0)                    # a unison: one organ note to each voice
            dbl[v].append(Note(n.t, n.d, n.midi, "organ:" + v, n.value))
        # the Amen: both chords under the choir, a note to a voice
        amen = defaultdict(list)
        for n in L.get("choir:chord", []):
            amen[n.t].append(n)
        self.amen = {}
        for t, ch in sorted(amen.items()):
            for v, n in zip("BTAS", sorted(ch, key=lambda n: n.midi)):
                self.amen.setdefault(v, []).append(Note(n.t, n.d, n.midi, "amen:" + v))
        self.amen_full = {n.t for n in L.get("amen-organ", [])}   # the chord the track gives the organ
        fifth = merged(L.get("pedal", []))
        quake = merged([Note(n.t, n.d, n.midi + 12, "quake-tone", n.value) for n in L.get("quake-tone", [])])
        viri, cant, wheel = L.get("viri", []), L.get("canticle", []), L.get("wheel", [])
        sounding = {
            "wheel": bars_of(wheel), "viri": bars_of(viri), "canticle": bars_of(cant),
            "fifth": bars_of(fifth), **{v: bars_of(dbl[v]) for v in ORDER},
            "amen": bars_of([n for x in self.amen.values() for n in x]),
            "bells": bars_of(L.get("bells", [])),
        }
        cue = self.cue_bars(sounding)
        subject = {(v, 2 * t) for v in ORDER for t, _, _, syl in self.choir[v] if syl}
        plan, prev = [], {}
        for b in range(N):
            has = lambda k: b in sounding[k]
            ped, lh, rh = [], [], []
            if has("amen"):
                ped, lh, rh = ["amen:B"], ["amen:T"], ["amen:S", "amen:A"]
            else:
                if has("B"):                        # the bass at 16' (the fifth holds it in Fundamentum)
                    ped = ["fifth"] if has("fifth") else ["B"]
                elif has("fifth"):
                    ped = ["fifth"]
                if has("wheel"):                    # the clock's wheel comes first, whole
                    lh = ["wheel"]
                elif has("viri"):
                    lh = ["viri"]
                if has("canticle"):                 # then the household
                    rh = ["canticle"]
                elif has("viri") and "viri" not in lh:
                    rh = ["viri"]
                free = [h for h, x in (("RH", rh), ("LH", lh)) if not x]
                if b in cue and "LH" in free:       # the right hand is the bells' cue; the choir to the left
                    free = ["LH"]
                got = self.choose(b, [v for v in "SAT" if has(v)], free, dbl, subject, prev)
                rh, lh = rh or got.get("RH", []), lh or got.get("LH", [])
                prev = got
            plan.append({"RH": rh, "LH": lh, "Ped": ped})
        # the quake's tone (a sine on E1) to the pedal at 16', where the pedal is free
        for n in quake:
            if all(not plan[b]["Ped"] for b in range(n.t // BAR, (n.end - 1) // BAR + 1)):
                for b in range(n.t // BAR, (n.end - 1) // BAR + 1):
                    plan[b]["Ped"] = ["quake"]
            else:
                self.log["quake-tone"].append(f"bar {n.t // BAR + 1}: the pedal has the bass; the quake's E1 is left to the bass drum")
        self.plan = plan
        source = {"wheel": wheel, "viri": viri, "canticle": cant, "fifth": fifth, "quake": quake,
                  **{v: dbl[v] for v in ORDER}, **{"amen:" + v: self.amen.get(v, []) for v in ORDER}}
        # each layer's notes to the hand the plan gives it in the bar where they start; a
        # held note stops at the bar where its hand is given something else
        hands = {"RH": [], "LH": [], "Ped": []}
        placed = set()
        for k, notes in source.items():
            for n in notes:
                b = n.t // BAR
                where = [h for h in hands if k in plan[b][h]]
                if not where:
                    continue
                h = where[0]
                end = n.end
                for c in range(b + 1, (n.end - 1) // BAR + 1):
                    if plan[c][h] and k not in plan[c][h]:
                        end = c * BAR; break
                if end < n.end:
                    self.log["shortened"].append(f"{k} bar {b + 1}: held into bar {end // BAR + 1}, where the {h} has another line")
                hands[h].append(Note(n.t, end - n.t, n.midi, k, n.value))
                placed.add(id(n))
        for k, notes in source.items():
            for n in notes:
                if id(n) not in placed:
                    self.log["left out of the organ"].append((k, n.t // BAR + 1))
        # the hand's span: two notes at once in one hand more than an octave apart cannot be held
        self.span(hands, "RH", plan)
        self.span(hands, "LH", plan)
        self.hands = hands
        self.voices = {h: self.allocate(hands[h], plan, h) for h in hands}
        self.cue = [Note(n.t, n.d, n.midi, "cue", n.value) for n in L.get("bells", []) if n.t // BAR in cue]
        self.cues = sorted(cue)

    def allocate(self, notes, plan, h):
        """A hand's notes to the two voices of its staff: the higher line of the bar's plan
        in the first voice, the lower in the second; a chord (the Amen, the fifth) in
        one. A voice already holding a note at that moment gives the note to the other."""
        units = defaultdict(list)
        for n in notes:
            chordal = n.layer.startswith("amen") or n.layer == "fifth"
            units[(n.t, n.d, "chord" if chordal else n.layer)].append(n)
        voices = ([], [])
        busy = lambda v, a, z: any(m.t < z and a < m.end for m in voices[v])
        for (t, d, k), ch in sorted(units.items(), key=lambda u: (u[0][0], -max(n.midi for n in u[1]))):
            job = plan[t // BAR][h]
            order = sorted(job, key=lambda x: ORDER.index(x) if x in ORDER else -1)
            want = order.index(k) if k in order else 0
            for v in (want, 1 - want):
                if not busy(v, t, t + d):
                    voices[v].extend(ch); break
            else:
                self.log["no voice free"].append(f"{h} {k} bar {t // BAR + 1}")
        return voices

    def choose(self, b, voices, free, dbl, subject, prev):
        """Which of the upper voices each free hand doubles in bar b. A hand holds two
        voices at most, never more than an octave apart at any moment, and the right
        hand's voices lie above the left's. Of the ways that fit, the one that doubles
        the most notes of a subject (the notes with words), then the most notes, then
        the same as the bar before, then the higher voices."""
        a, z = b * BAR, (b + 1) * BAR
        inbar = {v: [n for n in dbl[v] if n.t < z and a < n.end] for v in voices}
        def fit(vs):
            for t in range(a, z):
                now = [n.midi for v in vs for n in inbar[v] if n.t <= t < n.end]
                if now and max(now) - min(now) > 12:
                    return False
            return True
        def subsets(xs):
            return [()] + [(x,) for x in xs] + [(x, y) for i, x in enumerate(xs) for y in xs[i + 1:]]
        best, key = {}, None
        for rh in (subsets(voices) if "RH" in free else [()]):
            rest = [v for v in voices if v not in rh]
            for lh in (subsets(rest) if "LH" in free else [()]):
                if rh and lh and max(ORDER.index(v) for v in rh) > min(ORDER.index(v) for v in lh):
                    continue
                if not fit(rh) or not fit(lh):
                    continue
                on = [n for v in rh + lh for n in inbar[v] if n.t >= a]
                k = (sum((n.layer[-1], n.t) in subject for n in on), len(on),
                     (list(rh), list(lh)) == (prev.get("RH", []), prev.get("LH", [])),
                     [-ORDER.index(v) for v in rh])
                if key is None or k > key:
                    best, key = {"RH": list(rh), "LH": list(lh)}, k
        return best

    def span(self, hands, h, plan):
        """Two notes at once in one hand more than an octave apart cannot be held: the
        lower goes to the left hand if the left hand has nothing in those bars, or is
        left to the choir."""
        notes = sorted(hands[h], key=lambda n: (n.t, -n.midi))
        drop = []
        for a in notes:
            for b in notes:
                if b is a or b.midi >= a.midi or any(b is x for x in drop):
                    continue
                if a.t < b.end and b.t < a.end and a.midi - b.midi > 12:
                    drop.append(b)
        for b in drop:
            hands[h].remove(b)
            bars = range(b.t // BAR, (b.end - 1) // BAR + 1)
            if h == "RH" and all(not plan[c]["LH"] and not any(n.t < (c + 1) * BAR and c * BAR < n.end for n in hands["LH"])
                                 for c in bars):
                hands["LH"].append(Note(b.t, b.d, b.midi, b.layer, b.value))
                self.log["to the left hand (beyond the right hand's span)"].append(f"{b.layer} bar {b.t // BAR + 1}")
            else:
                self.log["beyond the hand's span, left to the choir"].append(f"{b.layer} bar {b.t // BAR + 1}")

    def cue_bars(self, sounding):
        """Where the organ cues the bells, if there are none: only where the bells carry
        something no one else has. Their first entrance (the first four bars of Diliges,
        over the alto's subject alone, the triad's light first heard), and their return
        after the tomb in Vere, high over the centurion's confession. Everywhere else
        their line shadows a subject the choir and organ already have."""
        bells = sorted(sounding["bells"])
        first = [b for b in bells if b < bells[0] + 4]
        vere = next(b0 for b0, b, sec, *_ in self.secs if sec == "secVERE")
        back = [b for b in bells if vere <= b < vere + 8]
        return set(first) | set(back)

    # ---------------- the bells
    def bells(self):
        self.bell = sorted(self.L.get("bells", []) + self.L.get("amen-bells", []), key=lambda n: (n.t, n.midi))

    # ---------------- the percussion: one player, two hands
    def percussion(self):
        L, N = self.L, self.N
        hands = defaultdict(set)                    # bar -> what the hands are busy with
        for k in ("hammer", "rocks", "timpani", "veil", "quake", "whirlwind"):
            for n in L.get(k, []):
                hands[n.t // BAR].add(k)
        up, down = [], []
        rent0, _ = self.part("rent")
        for n in L.get("kick", []):
            b = n.t // BAR
            if "quake" in hands[b]:
                self.log["percussion"].append(f"bar {b + 1}: the kick is inside the bass drum's roll (the quake)")
                continue
            down.append(Note(n.t, 4, None, "kick"))
        for n in L.get("hats", []):
            b = n.t // BAR
            if "hammer" in hands[b]:
                self.log["hats left to the organ's wheel (the hands have the hammer)"].append(b + 1)
                continue
            if "quake" in hands[b]:
                self.log["hats left out (the hands roll the bass drum: the stone)"].append(b + 1)
                continue
            up.append(Note(n.t, 2, None, "hats"))
        for n in L.get("hammer", []):
            up.append(Note(n.t, n.d, None, "hammer"))
        for n in L.get("rocks", []):
            if n.t // BAR == rent0:                 # the first bar of the rent: both hands roll the veil
                self.log["percussion"].append(f"bar {n.t // BAR + 1}: rocks (temple block) left out; the cymbal roll needs both hands")
                continue
            up.append(Note(n.t, 2, None, "rocks"))
        for n in L.get("timpani", []):
            up.append(Note(n.t, 2, 40, "timpani"))
        veil = L.get("veil", [])
        if veil:
            up.append(Note(veil[0].t, BAR, None, "veil"))   # rolled through the first bar, then let ring
            for n in veil[1:]:
                self.log["percussion"].append(f"bar {n.t // BAR + 1}: the veil goes on as the cymbal rings (l.v.)")
        for n in L.get("quake", []):
            if n.t // BAR in (rent0, rent0 + 1):
                self.log["percussion"].append(f"bar {n.t // BAR + 1}: the quake's rumble is left out (no hand free); its low E is on the organ's pedal")
                continue
            down.append(Note(n.t, n.d, None, "quake"))
        for n in merged([Note(n.t, n.d, 0, "whirlwind") for n in L.get("whirlwind", [])]):
            up.append(Note(n.t, n.d, None, "whirlwind"))     # one roll, bar after bar
        self.perc_up = sorted(up, key=lambda n: (n.t, n.layer))
        self.perc_down = sorted(down, key=lambda n: n.t)

# ---------------------------------------------------------------- 5. engraving: the choir, as counterpoint.py does it
# Copied from counterpoint.py (canon-lawyer-site, CC0), so the choir is engraved by the same
# rules as the published score: DUR, fits, sign, ly_text and the voice and words writers.
DUR = {1: "8", 2: "4", 3: "4.", 4: "2", 6: "2.", 7: "2..", 8: "1"}   # eighths -> LilyPond

def fits(o, n):
    return n in DUR and o + n <= 8 and (o == 0 or o + n <= 4 or o >= 4 or (o == 2 and n in (4, 6)) or n == 2)

def sign(t, n, rest=False):
    o = t % 8
    return max(k for k in range(1, min(n, 8 - o) + 1) if (o % k == 0 and k in (1, 2, 4, 8) if rest else fits(o, k)))

def ly_text(s):
    return '"' + s.replace('"', "'") + '"'

PC_NAME = {0: "c", 2: "d", 4: "e", 5: "f", 7: "g", 8: "gis", 9: "a", 11: "b"}

def lyname(m):
    name = PC_NAME.get(m % 12) or sys.exit(f"organ_edition.py: a pitch outside the mode: {m}")
    o = m // 12 - 1
    return name + ("'" * (o - 3) if o >= 3 else "," * (3 - o))

def ly_voice(events, heads):
    """One choir voice: [t8, (midi, name) or None, d8, syllable, words over it]; heads: {t: section}."""
    out = []
    for t, p, d, _, words in events:
        if t in heads:
            out.append(f"\n  % {heads[t]}\n ")
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
    for tok in out:
        cur.append(tok)
        if not tok.endswith("--") and (tok.strip('"').endswith(",") or len(" ".join(cur)) > 70 or tok.startswith("\\repeat")):
            lines.append(" ".join(cur)); cur = []
    return "\n  ".join(lines + [" ".join(cur)] if cur else lines)

FREE = "free voices: text to be set"
GOLGOTHA_WORDS = {"dark": "darkness: the clock alone", "cry": "Solo: the cry", "elias": "Sopranos: the crowd",
                  "finished": "Solo", "rent": "the veil and the earth", "centurion": "Solo: the centurion",
                  "silence": "the tomb"}

def choir_events(choir, secs, parts, total8):
    """The published choir as counterpoint.py's events, from bar 1 to the end, rests
    between the notes, split where its score splits them."""
    golgotha = [(b0 * 8, p) for b0, b, sec, p in parts if sec == "secGOLGOTHA"]
    over = {t: GOLGOTHA_WORDS[p] for t, p in golgotha}
    heads = {b0 * 8 for b0, *_ in secs}
    quiet = set()
    for b0, b, sec, p in parts:                     # parts where the whole choir is silent
        a, z = b0 * 8, (b0 + b) * 8
        if not any(a < t + d and t < z for v in ORDER for t, _, d, _ in choir[v]):
            quiet |= {a, z}
    sung = [(t, v) for v in ORDER for t, _, _, syl in choir[v] if syl is None]
    first_free = min(sung) if sung else None
    out = {}
    for v in ORDER:
        ev, at = [], 0
        cuts = sorted(heads | quiet | (set(over) if v == "S" else set()) | {total8})
        def rest(a, z):
            for c in [x for x in cuts if a < x < z] + [z]:
                ev.append([a, None, c - a, None, over.get(a) if v == "S" else None]); a = c
        for t, m, d, syl in choir[v]:
            if t > at:
                rest(at, t)
            words = over.get(t) if v == "S" else None
            if (t, v) == first_free:
                words = FREE
            ev.append([t, (m, lyname(m)), d, syl, words]); at = t + d
        if at < total8:
            rest(at, total8)
        out[v] = ev
    return out

# ---------------------------------------------------------------- 6. engraving: the instruments
DUR16 = {1: "16", 2: "8", 3: "8.", 4: "4", 6: "4.", 8: "2", 12: "2.", 14: "2..", 16: "1"}

def fits16(o, n):
    if n not in DUR16 or o + n > BAR:
        return False
    if o % 2 == 0 and n % 2 == 0:
        return fits(o // 2, n // 2)                 # on the eighth grid, the choir's rule
    return o // 4 == (o + n - 1) // 4               # a value in sixteenths keeps to its beat

def sign16(t, n, rest=False):
    o = t % BAR
    return max(k for k in range(1, min(n, BAR - o) + 1)
               if ((o % k == 0 and k in (1, 2, 4, 8, 16)) if rest else fits16(o, k)))

def chord_name(keys):
    return keys[0] if len(keys) == 1 else "<" + " ".join(keys) + ">"

def ly_line(notes, total, name=lambda n: lyname(n.midi), spacer=frozenset(), edges=frozenset(), before=None,
            after=None, roll=lambda n: "", cues=None, start=0):
    """One voice of an instrument: notes [Note] that do not overlap (notes at the same time
    and length are a chord). spacer: bars where the voice is invisible (another voice has
    the staff); edges: times where a run of rests is broken (a section, a part).
    before[t]: commands before the token at t; after[t]: what is attached to the note at t."""
    before, after, cues = before or {}, after or {}, cues or {}
    groups = defaultdict(list)
    for n in notes:
        groups[(n.t, n.d)].append(n)
    seq = sorted(groups.items())
    out, at = [], start
    def emit(tok, t):
        if t in before:
            out.extend(" " + c for c in before[t])
        out.append(" " + tok)
    def rests(a, z):
        while a < z:
            b = a // BAR
            if a % BAR == 0 and b in spacer:
                emit("s1", a); a += BAR
            elif a % BAR == 0 and a in cues and z - a >= cues[a][1] * BAR:
                quote, k, label = cues[a]
                emit(f"\\cueDuring #\"{quote}\" #UP {{ R1" + (f"*{k}" if k > 1 else "")
                     + f"^\\markup \\tiny \\italic {ly_text(label)} }}", a)
                a += k * BAR
            elif a % BAR == 0 and z - a >= BAR:
                n = BAR
                while a + n < z and a + n + BAR <= z and (a + n) not in edges and (a + n) not in before \
                        and (a + n) not in after and (a + n) not in cues and (a + n) // BAR not in spacer:
                    n += BAR
                emit("R1" + (f"*{n // BAR}" if n > BAR else "") + after.get(a, ""), a); a += n
            else:
                k = sign16(a, min(z, (b + 1) * BAR) - a, rest=True)
                emit(("s" if b in spacer else "r") + DUR16[k], a); a += k
            if a % BAR == 0:
                out.append(" |\n ")
    for (t, d), ch in seq:
        if t < at:
            raise ValueError(f"overlapping notes at {t}: {ch}")
        rests(at, t)
        keys = sorted({name(n) for n in ch}, key=lambda k: next(n.midi or 0 for n in ch if name(n) == k))
        left, a = d, t
        while left:
            k = sign16(a, left)
            tok = chord_name(keys) + DUR16[k] + roll(ch[0])
            if a == t:
                tok += after.get(t, "")
            emit(tok + ("~" if k < left else ""), a)
            a, left = a + k, left - k
            if a % BAR == 0:
                out.append(" |\n ")
        at = t + d
    rests(at, total)
    return "".join(out).rstrip()

def two_voices(v1, v2, total):
    """The bars where each of a staff's two voices has the staff to itself, or shares it."""
    a1, a2 = bars_of(v1), bars_of(v2)
    cmd1, cmd2, spacer1, spacer2 = {}, {}, set(), set()
    state1 = state2 = None
    for b in range(total // BAR):
        if b in a1 and b in a2:
            s1, s2 = "\\voiceOne", "\\voiceTwo"
        elif b in a2:
            s1, s2 = None, "\\oneVoice"; spacer1.add(b)
        else:
            s1, s2 = "\\oneVoice", None; spacer2.add(b)
        if s1 and s1 != state1:
            cmd1.setdefault(b * BAR, []).append(s1); state1 = s1
        if s2 and s2 != state2:
            cmd2.setdefault(b * BAR, []).append(s2); state2 = s2
    return cmd1, cmd2, spacer1, spacer2

# ---------------------------------------------------------------- 7. the organ's staves
MANUAL = {"wheel": "II", "canticle": "II", "cue": "II"}  # everything else on I; the pedal is the pedal

def registrations(E):
    """{(hand, time): [markup]}: registration, manual and dynamics, set by the track's own
    values: the wheel's low-pass, the Law held louder, the chord the track gives the organ."""
    out = defaultdict(list)
    def say(h, t, text):
        out[(h, t)].append(text)
    lex = {n.t for n in E.reinforced}
    once = set()                                    # said once in the whole organ part
    for h in ("RH", "LH", "Ped"):
        notes = sorted(E.hands[h], key=lambda n: (n.t, -n.midi))
        man, last_at, last_cut, seen = None, {}, None, set()
        for n in notes:
            k = n.layer
            m = "Ped" if h == "Ped" else MANUAL.get(k, "I")
            gap = n.t - last_at.get(k, -10 * BAR)
            if h != "Ped" and m != man:
                say(h, n.t, f"\\bold {m}")
                man = m
            if k == "canticle" and gap > BAR:
                say(h, n.t, "\"Gedackt 8', Flute 4': solo, legato\"")
            if k == "viri" and gap > BAR:
                say(h, n.t, "\"Principal 8' (soft): long notes\"")
            if k == "wheel":
                cut = n.value.get("cutoff")
                if cut != last_cut or gap > 2 * BAR:
                    text = {500: "\"Gedackt 8' alone, box closed\"",
                            1800: "\"Gedackt 8', Flute 4': the wheel, staccato\"",
                            2400: "\"Gedackt 8', Flute 4', staccato\""}[cut]
                    say(h, n.t, text + f" \\dynamic {WHEEL_DYN[cut]}")
                    last_cut = cut
            if k in "SAT" and "colla" not in once and n.t == min(m.t for x in E.hands.values() for m in x if m.layer in "SAT"):
                say(h, n.t, "\"Principal 8' (soft): with the choir\"")
                once.add("colla")
            if k == "fifth" and gap > BAR:
                say(h, n.t, "\"Subbass 16', Bourdon 8': the fifth, held\"")
            if k == "B":
                if "B" not in seen:
                    say(h, n.t, "\"16' + 8': with the basses\""); seen.add("B")
                if n.t in lex and "lex" not in seen:
                    say(h, n.t, "\"+ Principal 8' (or a soft reed): the Law held\""); seen.add("lex")
                if n.t not in lex and "lex" in seen and "unlex" not in seen and n.t > max(lex):
                    say(h, n.t, "\"− Principal 8'\""); seen.add("unlex")
            if k == "quake" and gap > BAR:
                say(h, n.t, "\"Subbass 16' (+ 32'): the earth quakes\" \\dynamic p")
            if k.startswith("amen") and n.t in E.amen_full and "full" not in seen:
                if h == "RH":
                    say(h, n.t, "\\bold \"Full organ\"")
                seen.add("full")
            last_at[k] = n.end
    return out

def clefs(notes, total, start="bass", high=61, low=59):
    """{time: '\\clef ...'} for a hand: treble where a bar's notes lie around middle C or
    higher (mean at least `high`), bass where they lie lower (mean at most `low`)."""
    out, now = {}, start
    for b in range(total // BAR):
        ms = [n.midi for n in notes if n.t < (b + 1) * BAR and b * BAR < n.end]
        if not ms:
            continue
        mean = sum(ms) / len(ms)
        want = "treble" if mean >= high else "bass" if mean <= low else now
        if want != now:
            out[b * BAR] = [f"\\clef \"{want}\""]; now = want
    return out

def staff_music(v1, v2, total, place, regs, hand, edges, before=None, roll=lambda n: "", name=None):
    """A staff's two voices as LilyPond, with the hand's markings on the first note at each time."""
    name = name or (lambda n: lyname(n.midi))
    c1, c2, sp1, sp2 = two_voices(v1, v2, total)
    for t, cs in (before or {}).items():
        c1.setdefault(t, [])[:0] = cs
    starts1, starts2 = {n.t for n in v1}, {n.t for n in v2}
    a1, a2 = {}, {}
    for (h, t), texts in regs.items():
        if h != hand:
            continue
        target = a1 if t in starts1 else a2 if t in starts2 else None
        if target is None:
            continue
        target[t] = target.get(t, "") + "".join(
            (f"{place}\\markup \\small \\italic {{ {x} }}" if not x.startswith("\\dynamic") else "") for x in texts)
    one = ly_line(v1, total, name=name, spacer=sp1, edges=edges, before=c1, after=a1, roll=roll)
    two = ly_line(v2, total, name=name, spacer=sp2, edges=edges, before=c2, after=a2, roll=roll)
    return one, two

# ---------------------------------------------------------------- 8. the bells and the percussion
BELL_DYN = {0.39: "mp", 0.33: "p", 0.3: "p"}

def bell_marks(E):
    """The bells' dynamics at each entry, the 8va brackets above C6, and a word over the low E."""
    after, before, last = defaultdict(str), defaultdict(list), -10 * BAR
    high, high_end = False, 0
    for n in E.bell:
        g = round(n.value.get("gain", 0), 2)
        if n.layer == "amen-bells":
            if n.t > last:
                after[n.t] += "\\mf_\\markup \\small \\italic \"the light: let ring\"\\laissezVibrer"
        elif n.t - last > BAR:
            after[n.t] += "\\" + BELL_DYN.get(g, "p")
        if n.midi >= 84 and not high:
            before[n.t].append("\\ottava #1"); high = True
        elif n.midi < 84 and high:
            before[high_end].append("\\ottava #0"); high = False
        if n.midi >= 84:
            high_end = n.end
        if n.midi < 67 and n.layer == "bells":
            after[n.t] += "_\\markup \\tiny \\italic \"(2-oct. set: 8va)\""
        last = max(last, n.end)
    return dict(after), dict(before)

DRUM = {"kick": "bd", "quake": "bd", "hats": "wbh", "hammer": "wbl", "rocks": "wbl",
        "timpani": "tomfl", "veil": "cymr", "whirlwind": "cymc"}
ROLLED = {"quake", "veil", "whirlwind"}
LABEL = {"kick": "B.D.", "hats": "Wood bl.", "hammer": "Temple bl.",
         "rocks": "Temple bl.", "timpani": "Timp.", "veil": "Sus. cym., soft mallets",
         "whirlwind": "Wind mach. (or cym.)", "quake": "B.D. roll"}
PERC_DYN = {"kick": "p", "hats": "p", "hammer": "mp", "rocks": "mf", "whirlwind": "pp"}

def perc_marks(E):
    """The percussion's labels and dynamics at each instrument's entry, one dynamic where
    both hands come in together; the shapes of the crescendo and the rolls."""
    after = {"up": defaultdict(str), "down": defaultdict(str)}
    labels, dyn, last = defaultdict(list), {}, {}
    timp = [n.t for n in E.perc_up if n.layer == "timpani"]
    for voice, notes in (("up", E.perc_up), ("down", E.perc_down)):
        for n in notes:
            k = n.layer
            if n.t - last.get(k, -10 * BAR) > BAR:
                if LABEL[k] not in labels[(voice, n.t)]:
                    labels[(voice, n.t)].append(LABEL[k])
                if k in PERC_DYN and not (timp and timp[0] <= n.t <= timp[-1]):
                    dyn[(voice, n.t)] = PERC_DYN[k]
            last[k] = n.end
    for (voice, t), d in list(dyn.items()):
        if voice == "down" and dyn.get(("up", t)) == d:
            del dyn[(voice, t)]
    for (voice, t), xs in labels.items():
        place = "^" if voice == "up" else "_"
        after[voice][t] += f"{place}\\markup \\small \\italic {ly_text(' + '.join(xs))}"
    for (voice, t), d in dyn.items():
        after[voice][t] += "\\" + d
    for n in E.perc_up:
        if n.layer == "timpani":
            after["up"][n.t] += "\\p\\<" if n.t == timp[0] else "\\f" if n.t == timp[-1] else ""
        if n.layer == "veil":
            after["up"][n.t] += "\\f\\>\\laissezVibrer"
    for n in E.perc_down:
        if n.layer == "quake":
            after["down"][n.t] += "\\f\\>"
    return after

def perc_before(E):
    """A roll's diminuendo ends inside it, three quarters of the way through."""
    return {n.t: ["\\after 2. \\!"] for n in E.perc_up + E.perc_down if n.layer in ("veil", "quake")}

def perc_music(E, edges, texts=None, simile=False):
    """The percussion as LilyPond: the two hands as two voices where they play, one rest
    where both are silent (so a part can compress it). simile: in the part, four or more
    bars alike are written once, with repeat signs (the score and the MIDI write them all)."""
    total, texts = E.N * BAR, texts or {}
    after, before = perc_marks(E), perc_before(E)
    name, roll = (lambda n: DRUM[n.layer]), (lambda n: ":32" if n.layer in ROLLED else "")
    # a stroke is written as one sign from its onset, never tied: wood and skin do not sustain
    hit = lambda ns: [n if n.layer in ROLLED else Note(n.t, sign16(n.t, n.d), n.midi, n.layer, n.value) for n in ns]
    ups, downs = hit(E.perc_up), hit(E.perc_down)
    au, ad = bars_of(E.perc_up), bars_of(E.perc_down)
    segs = []                                       # bars alike in which hands play, together
    for b in sorted(au | ad):
        who = (b in au, b in ad)
        if segs and b == segs[-1][1] and who == segs[-1][2]:
            segs[-1][1] = b + 1
        else:
            segs.append([b, b + 1, who])
    out, at = [], 0
    rest_after = {t: f"^\\markup \\tiny \\italic {ly_text(x)}" for t, x in texts.items()}
    def music(a, z):
        u = [n for n in ups if a * BAR <= n.t < z * BAR]
        d = [n for n in downs if a * BAR <= n.t < z * BAR]
        line = lambda ns, v: ly_line(ns, z * BAR, name=name, start=a * BAR, edges=edges, after=after[v], roll=roll,
                                     before=before)
        return f"<< {{ {line(u, 'up')} }}\n  \\\\ {{ {line(d, 'down')} }} >>" if u and d else line(u or d, "up" if u else "down")
    def alike(b):
        """What a bar plays, its marks, and whether a section or a cue begins on it."""
        ns = [n for n in ups + downs if b * BAR <= n.t < (b + 1) * BAR]
        return (tuple(sorted((n.t - b * BAR, n.d, n.layer, after["up"].get(n.t, "") + after["down"].get(n.t, ""))
                             for n in ns)), any(b * BAR <= t < (b + 1) * BAR for t in set(edges) | set(before)))
    for a, z, _ in segs:
        if a > at:
            out.append(ly_line([], a * BAR, start=at * BAR, edges=edges, after=rest_after))
        whole = [n for n in ups + downs if a * BAR <= n.t < z * BAR]
        if not simile or any(n.end > (n.t // BAR + 1) * BAR for n in whole):
            out.append(music(a, z))
        else:
            b = a
            while b < z:
                k = 1
                while b + k < z and alike(b + k) == alike(b) and not alike(b + k)[1]:
                    k += 1
                if k >= 4:
                    out.append(f"\\repeat percent {k} {{ {music(b, b + 1).rstrip(' |')} }}")
                    b += k
                else:
                    out.append(music(b, b + k)); b += k
        at = z
    if at < E.N:
        out.append(ly_line([], total, start=at * BAR, edges=edges, after=rest_after))
    return "\n  ".join(x.strip() for x in out if x.strip())

# ---------------------------------------------------------------- 9. the form's marks, and the cues
SUBPART = {"dark": "darkness: the clock alone (choir tacet)", "cry": "the cry: the clock stutters",
           "elias": "the crowd, and a wind that does not come", "finished": "“it is finished”: the clock stops",
           "rent": "the veil, top to bottom; the earth quakes; the rocks rend",
           "centurion": "the centurion, alone",
           "silence": "the tomb: three bars of silence, all tacet, organ too"}

SUBPART_SHORT = {"dark": "darkness", "cry": "the cry", "elias": "the crowd", "finished": "“it is finished”",
                 "rent": "the rent", "centurion": "the centurion", "silence": "the tomb: silence"}

def mark_list(E, part=False):
    """[(time, order, LilyPond)]: the sections, their parts, the silences, the spoken line.
    A part (part=True) for the bells has the sections and the spoken line only."""
    out = [(0, 0, "\\tempo 4 = 120")]
    for b0, bars, sec, name, num in E.secs:
        t = b0 * BAR
        if b0:
            out.append((t, 1, "\\section"))
        out.append((t, 2, f"\\mark \\markup \\box \\bold {ly_text(num)}"))
        out.append((t, 3, f"\\sectionLabel \\markup \\line {{ \\bold {ly_text(name)} \\hspace #1 "
                          f"\\italic {ly_text(f'bar {b0 + 1} ({clock(b0)})')} }}"))
    household = {n.t // BAR for n in E.L.get("canticle", []) if n.t >= 9 * BAR}
    for b0, bars, sec, p in E.parts:
        t, text = b0 * BAR, None
        if part == "bells" and not (sec == "secAMEN" and p == "silence"):
            if sec == "secGOLGOTHA" and p == "dark":
                out.append((t, 4, "\\textMark \\markup \\italic \"bells tacet\""))
            continue
        if sec == "secGOLGOTHA":
            text = SUBPART_SHORT[p] if part else SUBPART[p]
        elif sec == "secVERE" and b0 == min(x for x, _, s, _ in E.parts if s == "secVERE"):
            text = "the stone" if part else "the stone: the clock comes back"
        elif sec == "secDUOBUS" and b0 in household:
            text = "the household" if part else "the household hangs on them"
        elif sec == "secAMEN" and p == "silence":
            text = None
            out.append((t, 4, "\\textMark \\markup \\italic \"silence\""))
            out.append((t, 5, "\\textMark \\markup \\column { \\line { \\bold \"Reader (or the priest), optional, spoken:\" } "
                              "\\line { \\italic \"“If ye love me, keep my commandments.”\" \"(John 14:15)\" } }"))
        if text:
            out.append((t, 4, f"\\textMark \\markup \\italic {ly_text(text)}"))
    out.append((E.N * BAR, 9, "\\bar \"|.\""))
    return out

def ly_marks(E, part=False):
    stream, now = [], 0
    for t, _, code in sorted(mark_list(E, part)):
        if t > now:
            n = t - now
            stream.append(f"s1*{n // BAR}" if n % BAR == 0 else f"s16*{n}"); now = t
        stream.append(code)
    return "\n  ".join(stream)

def edges_of(E):
    """Where a run of rests is broken: every section and every part of a section."""
    return {b0 * BAR for b0, *_ in E.secs} | {b0 * BAR for b0, *_ in E.parts}

def entrances(notes, total, rest=4):
    """The times a part comes in after `rest` bars or more of silence (or at its first note)."""
    out, last = [], -rest * BAR
    for n in sorted(notes, key=lambda n: n.t):
        if n.t - last >= rest * BAR and n.t >= 2 * BAR:
            out.append(n.t)
        last = max(last, n.end)
    return out

def heard(E, a, z):
    """What a player hears from a to z, loudest first: [(quote, label, words)]."""
    out = []
    for v in ORDER:
        sung = [(t, syl) for t, m, d, syl in E.choir[v] if 2 * t < z and a < 2 * (t + d)]
        if sung:
            words = " ".join(s[0] + ("-" if s[1] else "") for _, s in sung if s).replace("- ", "")
            out.append((v, {"S": "Sop.", "A": "Alto", "T": "Ten.", "B": "Bass"}[v], words))
    for h, q, label in (("RH", "orgRH", "Org."), ("LH", "orgLH", "Org. L.H.")):
        if any(n.t < z and a < n.end for n in E.voices[h][0]):
            out.append((q, label, ""))
    return out

def cue_rests(E, notes, kind):
    """Cues in a part: two bars of what is heard before each entrance after a long rest.
    The bells read the notes; the percussion reads a word."""
    cues, texts = {}, {}
    for t in entrances(notes, E.N * BAR):
        b = t // BAR
        a = (b - 2) * BAR
        if a < 0 or any(n.t < t and a < n.end for n in notes):
            continue
        h = heard(E, a, t)
        if not h:
            continue
        quote, label, words = h[0]
        if kind == "bells" and quote in ("S", "A", "orgRH", "orgLH"):
            cues[a] = (quote, 2, label)
        else:
            texts[(b - 1) * BAR] = f"cue: {label}" + (f" “{words}”" if words else "")
    return cues, texts

# ---------------------------------------------------------------- 10. the books
def runs_of(bars):
    """[first, last] of each run of consecutive bars (0-based in, 1-based out)."""
    out = []
    for b in sorted(bars):
        if out and b + 1 == out[-1][1] + 1:
            out[-1][1] = b + 1
        else:
            out.append([b + 1, b + 1])
    return out

NUMBER = {6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve"}

def say_bars(r):
    return f"{r[0]}–{r[1]}" if r[1] > r[0] else f"{r[0]}"

def preface(E, form_name):
    """The preface page: forces, the optional parts, registration, the silences, timings."""
    N = E.N
    sec = {s[2]: s for s in E.secs}
    part = lambda p: [x for x in E.parts if x[3] == p][0]
    dark, rent, tomb, fin = part("dark"), part("rent"), part("silence"), part("finished")
    after = [x for x in E.parts if x[2] == "secAMEN" and x[3] == "silence"][0]
    vere = sec["secVERE"]
    cue = runs_of(E.cues)
    hammer = runs_of({b - 1 for b in E.log["hats left to the organ's wheel (the hands have the hammer)"]})
    names = {64: "E4", 67: "G4", 71: "B4", 76: "E5", 79: "G5", 80: "G♯5", 83: "B5", 88: "E6", 91: "G6"}
    bells = " ".join(names.get(m, str(m)) for m in sorted({n.midi for n in E.bell}))
    low = sorted({n.t // BAR + 1 for n in E.bell if n.midi < 67 and n.layer == "bells"})
    pedal = "in Pendet" + (" and Fundamentum" if "secFUNDAMENTUM" in sec else "")
    lex = " In Lex it adds a Principal 8' (or a soft reed) for the Law held." if "secLEX" in sec else ""
    paras = [
        ("The edition",
         "The track at canon-lawyer.ca/music/ is techno: a kick drum, hi-hats and a square-wave arpeggio around a choir. "
         "This is the same piece for a parish, arranged by rule (organ_edition.py) from what the track plays. The choir's "
         "part is the choir score's, note for note and word for word; the organ doubles it, as the track's organ does, "
         "and takes the other layers in their own notes and rhythms. The bar numbers and the times are the track's: a bar "
         f"is two seconds (quarter = 120); {N} bars, {clock(N)}."),
        ("Forces",
         "SATB choir, with a soprano solo in Golgotha (the cry, “Consummatum est”, the centurion) and a few sopranos for "
         "the crowd; organ, two manuals and pedal. Optional: bells and percussion, a player each, and a reader."),
        ("The words",
         "The subjects are sung to the Latin of the Vulgate they are carved from. The free voices have no words yet "
         "(“free voices: text to be set”): they may sing on “ah”, or hum."),
        ("The organ",
         "Manual I doubles the choir (Principal 8', soft), and has Viri Galilaei in long notes. Manual II has the clock's "
         "wheel, staccato (Gedackt 8', Flute 4'), and the canticle of “Brother Electron”, a solo. The pedal doubles the "
         f"basses at 16' and 8' and holds the fifth E–B {pedal}.{lex} In the darkness: Gedackt 8' alone, the box closed. "
         "In the earthquake: low E on 16' (and 32'). The last chord: full organ. Under the wheel the right hand takes the "
         "two upper voices that fit the hand, the subject first; at the end of Duobus it leaves the choir for the canticle."),
        ("The silences, and the spoken line",
         f"In the darkness ({dark[0] + 1}–{dark[0] + dark[1]}) the choir rests. At “it is finished” ({fin[0] + 1}) the "
         f"clock stops. The tomb ({tomb[0] + 1}–{tomb[0] + tomb[1]}) is silence for all, organ too. After the Amen, four "
         f"bars of silence ({after[0] + 1}–{N}): in the first ({clock(after[0])}) a reader or the priest may say plainly "
         "“If ye love me, keep my commandments” (John 14:15); if not, keep the silence."),
        ("Bells (optional)",
         "One part for handbells, handchimes or glockenspiel, at the track's pitch: "
         f"{NUMBER[len(set(n.midi for n in E.bell))]} notes, the triad E–G–B over three octaves "
         f"and the G♯ of the last chord ({bells}). Handbells or handchimes (sounding an octave up): a 3-octave set plays "
         f"it as written; a 2-octave set plays the low E an octave up (bar{'s' if len(low) > 1 else ''} "
         f"{', '.join(map(str, low))}). Glockenspiel (sounding two octaves up): the 8va passages without the 8va. "
         "Tubular bells (C4–F5) reach only the lowest notes."),
        ("Without bells",
         "The bells' line shadows whichever voice has the subject, so the music stands without them. Twice they carry "
         f"what no one else has: their first entrance ({say_bars(cue[0])}), the triad's light over the alto's subject, "
         f"and their return after the tomb ({say_bars(cue[-1])}), high over the centurion's confession. There the organ "
         f"has a cue staff for Manual II (in {say_bars(cue[-1])}, instead of the choir's notes)."),
        ("Percussion (optional, one player)",
         "Bass drum (soft beater; soft mallets for rolls), woodblock or claves, temple block or side stick, suspended "
         "cymbal, one timpano on E, wind machine (or the cymbal). The clock: bass drum on 1 and 3, woodblock in eighths. "
         "The hammer: the Morse of “Is not this the carpenter”, a dot a sixteenth, a dash a dotted eighth. Where the "
         "track needs more than two hands, the part keeps the bass drum and the hammer "
         f"({', '.join(say_bars(r) for r in hammer)}; the wheel has the eighths), the cymbal and then the timpani with "
         f"the temple block in the rent ({rent[0] + 1}, {rent[0] + 2}), and the bass drum roll at the stone "
         f"({vere[0] + 1}). A second player could add the bass drum roll in {rent[0] + 1}–{rent[0] + 2} and the temple "
         f"block in {rent[0] + 1}."),
        ("Without percussion",
         "The music stands, and loses the clock's tick (its eighths stay in the wheel), the hammer, the stutter under "
         "the cry, the wind under the crowd, the veil, rocks and timpani of the rent (the organ's low E stays), and the stone."),
        ("Sections",
         " · ".join(f"{num} {name}, bar {b0 + 1} ({clock(b0)})" for b0, bars, s_, name, num in E.secs) + "."),
    ]
    scm = lambda x: x.replace("\\", "\\\\").replace('"', '\\"')
    body = []
    for head, text in paras:
        body.append(f"\\line {{ \\bold {ly_text(head)} }}")
        body.append(f"\\wordwrap-string #\"{scm(text)}\"")
        body.append("\\vspace #0.2")
    body.append("\\vspace #0.5")
    body.append("\\line { \\italic \"Dedicated to the public domain (CC0 1.0) · Made by Claude + Richard\" }")
    return "\\markup \\fontsize #-1.5 \\column {\n    " + "\n    ".join(body) + "\n  }"

LEGEND = r"""\markup \score {
  \new DrumStaff \with { drumStyleTable = #(alist->hash-table churchPercussion) \remove "Time_signature_engraver"
    \override StaffSymbol.staff-space = #0.9 }
  \drummode { \cadenzaOn
    cymr1_\markup \tiny \center-column { "susp." "cym." } s4 cymc1_\markup \tiny \center-column { "wind" "mach." } s4
    wbh1_\markup \tiny "woodbl." s4 wbl1_\markup \tiny \center-column { "temple" "block" } s4
    tomfl1_\markup \tiny \center-column { "timp." "(E)" } s4 bd1_\markup \tiny \center-column { "bass" "drum" } }
  \layout { indent = 0 ragged-right = ##t }
}"""

def write(E, path, form_name, stem):
    total = E.N * BAR
    edges = edges_of(E)
    # the choir
    events = choir_events(E.choir, E.secs, E.parts, E.N * 8)
    heads = {b0 * 8: f"{num}. {name}" for b0, bars, sec, name, num in E.secs}
    names = dict(zip(ORDER, ("soprano", "alto", "tenor", "bass")))
    music = []
    for v in ORDER:
        music.append(f"{names[v]} = {{{ly_voice(events[v], heads)}\n}}\n"
                     f"{names[v]}Words = \\lyricmode {{\n  {ly_words(events[v])}\n}}")
    # the organ
    regs = registrations(E)
    rh_notes = E.voices["RH"][0] + E.voices["RH"][1]
    rh1, rh2 = staff_music(*E.voices["RH"], total, "^", regs, "RH", edges,
                           before=clefs(rh_notes, total, start="treble", high=58, low=52))
    lh_notes = E.voices["LH"][0] + E.voices["LH"][1]
    lh1, lh2 = staff_music(*E.voices["LH"], total, "_", regs, "LH", edges,
                           before=clefs(lh_notes, total, high=64, low=59))
    ped, _ = staff_music(E.voices["Ped"][0] + E.voices["Ped"][1], [], total, "_", regs, "Ped", edges)
    cue_after = {}
    starts = []
    for n in sorted(E.cue, key=lambda n: n.t):
        if not starts or n.t - starts[-1][1] > BAR:
            starts.append([n.t, n.end])
        starts[-1][1] = max(starts[-1][1], n.end)
    for a, z in starts:
        inst = "if no bells: R.H., II, Flute 8' + 4'" if not any(n.t < z and a < n.end for n in E.voices["RH"][0] + E.voices["RH"][1]) \
            else "if no bells: R.H. plays this on II, Flute 8' + 4', and leaves the choir's notes"
        cue_after[a] = f"^\\markup \\tiny \\italic {ly_text(inst)}"
    cue_before = {}
    high = False
    for n in sorted(E.cue, key=lambda n: n.t):
        if n.midi >= 84 and not high:
            cue_before.setdefault(n.t, []).append("\\ottava #1"); high = True
        elif n.midi < 84 and high:
            cue_before.setdefault(n.t, []).append("\\ottava #0"); high = False
    cue = ly_line(E.cue, total, edges=edges, after=cue_after, before=cue_before)
    # the bells: in the score; and in their part, with cues, a rest to a section
    b_after, b_before = bell_marks(E)
    part_edges = {b0 * BAR for b0, *_ in E.secs} | {b0 * BAR for b0, _, sec, p in E.parts if p == "silence"}
    b_cues, b_texts = cue_rests(E, E.bell, "bells")
    bells_score = ly_line(E.bell, total, edges=edges, after=b_after, before=b_before)
    b_part_after = dict(b_after)
    for t, x in b_texts.items():
        b_part_after[t] = b_part_after.get(t, "") + f"^\\markup \\tiny \\italic {ly_text(x)}"
    bells_part = ly_line(E.bell, total, edges=part_edges | set(b_texts), after=b_part_after, before=b_before,
                         cues=b_cues)
    # the percussion: in the score; and in its part, with cues in words
    _, p_texts = cue_rests(E, E.perc_up + E.perc_down, "perc")
    perc = perc_music(E, edges)
    perc_part = perc_music(E, edges | set(p_texts), texts=p_texts, simile=True)
    long_form = E.long
    sub = "The long form: a double fugue for Matthew 22:34–40" if long_form else "A double fugue for Matthew 22:34–40"
    ly = TEMPLATE.format(
        stem=stem, form=form_name, subtitle=sub, marks=ly_marks(E), music="\n\n".join(music),
        rh1=rh1, rh2=rh2, lh1=lh1, lh2=lh2, ped=ped, cue=cue, bells=bells_score, bellsPart=bells_part,
        perc=perc, percPart=perc_part, preface=preface(E, form_name), legend=LEGEND, marksPart=ly_marks(E, part="bells"), marksPerc=ly_marks(E, part="percussion"),
        quotes="\n".join(f'\\addQuote "{q}" {{ \\{x} }}' for q, x in
                         (("S", "soprano"), ("A", "alto"), ("orgRH", "organRHone"), ("orgLH", "organLHone"))),
        bars=E.N, time=clock(E.N))
    path.write_text(ly, encoding="utf-8")

TEMPLATE = r"""% On These Two Hang{form}: an organ edition, with optional bells and percussion
% SATB choir and organ (two manuals and pedal); bells and percussion ad libitum; a reader.
% Written by organ_edition.py (music-generation/arrange) from the events the track plays
% and from the published choir parts; do not edit by hand.
% Engrave with GNU LilyPond: lilypond {stem}-organ.ly
% It makes {stem}-organ.pdf (the full score, with a preface), {stem}-organ-bells.pdf and
% {stem}-organ-percussion.pdf (the parts), and {stem}-organ.mid (a track to a staff).
% Dedicated to the public domain (CC0 1.0).

\version "2.24.0"

#(ly:set-option 'midi-extension "mid")

\paper {{
  #(set-paper-size "letter")
  top-margin = 14\mm
  bottom-margin = 12\mm
  left-margin = 16\mm
  right-margin = 14\mm
  markup-system-spacing.padding = 2
  score-markup-spacing.padding = 2
  system-system-spacing.padding = 2.5
  print-page-number = ##t
  print-first-page-number = ##f
}}

\header {{
  title = "On These Two Hang"
  subtitle = "{subtitle}"
  subsubtitle = "For SATB choir and organ, with bells and percussion ad libitum"
  poet = "Words: the Vulgate"
  composer = \markup \right-column {{ "Notes made by rule: counterpoint.py" "Arranged by rule from the track: organ_edition.py" }}
  copyright = "Dedicated to the public domain (CC0 1.0)"
  tagline = \markup \small {{ "canon-lawyer.ca/music/ · Dedicated to the public domain (CC0 1.0) · Made by Claude + Richard" }}
}}

#(define churchPercussion '(
  (ridecymbal cross #f 5)
  (crashcymbal xcircle #f 5)
  (hiwoodblock default #f 3)
  (lowoodblock default #f 1)
  (lowfloortom default #f -1)
  (bassdrum default #f -3)))

global = {{ \key e \phrygian \numericTimeSignature \time 4/4 }}

marks = {{
  {marks}
}}

{music}

organRHone = {{{rh1}
}}
organRHtwo = {{{rh2}
}}
organLHone = {{{lh1}
}}
organLHtwo = {{{lh2}
}}
pedal = {{{ped}
}}
bellCue = {{{cue}
}}
bells = {{{bells}
}}
bellsPart = {{{bellsPart}
}}
perc = \drummode {{
  {perc}
}}
percPart = \drummode {{
  {percPart}
}}

marksPart = {{
  {marksPart}
}}

marksPerc = {{
  {marksPerc}
}}

{quotes}

choir = \new ChoirStaff <<
  \new Staff \with {{ instrumentName = "Soprano" shortInstrumentName = "S." }} <<
    \new Voice = "S" {{ \global \clef "treble" \soprano }}
  >>
  \new Lyrics \lyricsto "S" {{ \sopranoWords }}
  \new Staff \with {{ instrumentName = "Alto" shortInstrumentName = "A." }} <<
    \new Voice = "A" {{ \global \clef "treble" \alto }}
  >>
  \new Lyrics \lyricsto "A" {{ \altoWords }}
  \new Staff \with {{ instrumentName = "Tenor" shortInstrumentName = "T." }} <<
    \new Voice = "T" {{ \global \clef "treble_8" \tenor }}
  >>
  \new Lyrics \lyricsto "T" {{ \tenorWords }}
  \new Staff \with {{ instrumentName = "Bass" shortInstrumentName = "B." }} <<
    \new Voice = "B" {{ \global \clef "bass" \bass }}
  >>
  \new Lyrics \lyricsto "B" {{ \bassWords }}
>>

organ = \new PianoStaff \with {{
  instrumentName = "Organ" shortInstrumentName = "Org."
  \consists Keep_alive_together_engraver
}} <<
  \new Staff = "RH" <<
    \global \clef "treble"
    \new Voice = "RH1" {{ \organRHone }}
    \new Voice = "RH2" {{ \organRHtwo }}
  >>
  \new Staff = "LH" <<
    \global \clef "bass"
    \new Voice = "LH1" {{ \organLHone }}
    \new Voice = "LH2" {{ \organLHtwo }}
  >>
  \new Staff = "Ped" \with {{ instrumentName = "Ped." shortInstrumentName = "Ped." }} <<
    \global \clef "bass"
    \new Voice = "Ped" {{ \pedal }}
  >>
>>

bellStaff = \new Staff \with {{
  instrumentName = \markup \center-column {{ "Bells" "(opt.)" }} shortInstrumentName = "Bl."
  midiInstrument = "celesta"
}} \new Voice = "Bells" {{ \global \clef "treble" \bells }}

percStaff = \new DrumStaff \with {{
  instrumentName = \markup \center-column {{ "Perc." "(opt.)" }} shortInstrumentName = "Perc."
  drumStyleTable = #(alist->hash-table churchPercussion)
}} {{ \numericTimeSignature \time 4/4 \perc }}

\book {{
  {preface}
  \pageBreak
  \score {{
    <<
      \new Staff \with {{ \remove "Staff_symbol_engraver" \override VerticalAxisGroup.remove-first = ##t }} {{ \marks }}
      \bellStaff
      \percStaff
      \choir
      \new Staff = "cue" \with {{
        \magnifyStaff #2/3
        instrumentName = \markup \center-column {{ "Org. II" "(no bells)" }} shortInstrumentName = "cue"
        \override VerticalAxisGroup.remove-first = ##t
      }} {{ \global \clef "treble" \bellCue }}
      \organ
    >>
    \layout {{
      #(layout-set-staff-size 15)
      \context {{ \Staff \RemoveEmptyStaves \override VerticalAxisGroup.staff-staff-spacing.minimum-distance = #6 }}
      \context {{ \DrumStaff \RemoveEmptyStaves }}
      \context {{ \Score
        \override BarNumber.break-visibility = ##(#f #t #t)
        barNumberVisibility = #(every-nth-bar-number-visible 1)
        \override BarNumber.font-size = #-2
      }}
      \context {{ \Lyrics
        \override LyricText.font-size = #0.5
        \override LyricHyphen.minimum-distance = #1.2
        \override LyricSpace.minimum-distance = #1.0
      }}
    }}
  }}
  \score {{
    <<
      \new Staff = "Bells" \with {{ midiInstrument = "celesta" }} \new Voice = "Bells" {{ \bells }}
      \new DrumStaff = "Percussion" {{ \perc }}
      \new Staff = "Soprano" \with {{ midiInstrument = "choir aahs" }} \new Voice = "S" {{ \soprano }}
      \new Lyrics \lyricsto "S" {{ \sopranoWords }}
      \new Staff = "Alto" \with {{ midiInstrument = "choir aahs" }} \new Voice = "A" {{ \alto }}
      \new Lyrics \lyricsto "A" {{ \altoWords }}
      \new Staff = "Tenor" \with {{ midiInstrument = "choir aahs" }} \new Voice = "T" {{ \tenor }}
      \new Lyrics \lyricsto "T" {{ \tenorWords }}
      \new Staff = "Bass" \with {{ midiInstrument = "choir aahs" }} \new Voice = "B" {{ \bass }}
      \new Lyrics \lyricsto "B" {{ \bassWords }}
      \new Staff = "Organ right hand" \with {{ midiInstrument = "church organ" }} << \new Voice = "RH1" {{ \organRHone }} \new Voice = "RH2" {{ \organRHtwo }} >>
      \new Staff = "Organ left hand" \with {{ midiInstrument = "church organ" }} << \new Voice = "LH1" {{ \organLHone }} \new Voice = "LH2" {{ \organLHtwo }} >>
      \new Staff = "Organ pedal" \with {{ midiInstrument = "church organ" }} \new Voice = "Ped" {{ \pedal }}
    >>
    \midi {{ \tempo 4 = 120 }}
  }}
}}

\book {{
  \bookOutputSuffix "bells"
  \header {{
    subsubtitle = \markup \bold "Handbells, chimes or glockenspiel (optional)"
    poet = ##f composer = ##f
  }}
  \markup \fontsize #-1 \wordwrap-string #"Written at the track's pitch: handbells and handchimes sound an octave higher, the glockenspiel two. A 3-octave set (C4–C7) plays it as written; a 2-octave set (G4–G6) plays the low E an octave higher, where marked. Glockenspiel: play the 8va passages as printed, without the 8va. Small notes are cues. {bars} bars, {time}; a bar is two seconds."
  \score {{
    <<
      \new Staff \with {{ \remove "Staff_symbol_engraver" \remove "Clef_engraver" \remove "Time_signature_engraver" }} {{ \marksPart }}
      \new Staff \with {{ instrumentName = "Bells" }} {{ \global \clef "treble" \compressMMRests \bellsPart }}
    >>
    \layout {{
      #(layout-set-staff-size 18)
      \context {{ \Staff \RemoveEmptyStaves \override VerticalAxisGroup.remove-first = ##t }}
      \context {{ \Score \override MultiMeasureRest.minimum-length = #30 }}
    }}
  }}
  \paper {{ page-breaking = #ly:optimal-breaking }}
}}

\book {{
  \bookOutputSuffix "percussion"
  \header {{
    subsubtitle = \markup \bold "Percussion (optional, one player)"
    poet = ##f composer = ##f
  }}
  \markup \fontsize #-1 \wordwrap-string #"Bass drum (soft beater; soft mallets for the rolls), woodblock (or claves), temple block (or side stick), suspended cymbal (soft mallets), one timpano tuned to E, wind machine (or the cymbal, rolled). The clock: bass drum on 1 and 3, woodblock in eighths. The hammer: the Morse of “Is not this the carpenter”, a dot a sixteenth, a dash a dotted eighth. Cues are in words. {bars} bars, {time}; a bar is two seconds."
  {legend}
  \score {{
    <<
      \new Staff \with {{ \remove "Staff_symbol_engraver" \remove "Clef_engraver" \remove "Time_signature_engraver" }} {{ \marksPerc }}
      \new DrumStaff \with {{ instrumentName = "Perc." drumStyleTable = #(alist->hash-table churchPercussion) }}
        {{ \numericTimeSignature \time 4/4 \set countPercentRepeats = ##t
           \set repeatCountVisibility = #(every-nth-repeat-count-visible 4) \compressMMRests \percPart }}
    >>
    \layout {{
      #(layout-set-staff-size 19)
      \context {{ \Staff \RemoveEmptyStaves \override VerticalAxisGroup.remove-first = ##t }}
      \context {{ \Score \override MultiMeasureRest.minimum-length = #30 }}
    }}
  }}
  \paper {{ max-systems-per-page = 6 }}
}}
"""

# ---------------------------------------------------------------- 11. main
def main():
    args = sys.argv[1:]
    def arg(flag, default=None):
        if flag in args:
            k = args.index(flag)
            if k + 1 >= len(args):
                sys.exit(f"organ_edition.py: {flag} needs a value")
            return args[k + 1]
        return default
    site = Path(arg("--site") or sys.exit(__doc__))
    long_form = "--long" in args
    music = site / "docs" / "assets" / "music"
    track = music / ("on-these-two-hang.long.strudel.js" if long_form else "on-these-two-hang.strudel.js")
    stem = "on-these-two-hang-long" if long_form else "on-these-two-hang"
    out = Path(arg("--out") or music / "scores")
    src = track.read_text(encoding="utf-8")
    secs, parts, total = form(src)
    L = layers(track_events(track, total))
    choir = published_choir(music / "scores" / stem)
    eng = engine_choir(L)
    for v in ORDER:
        if [(t, m, d) for t, m, d, _ in choir[v]] != eng[v]:
            sys.exit(f"organ_edition.py: the published {VOICE[v].lower()} part is not what the track sings")
    E = Edition(L, choir, secs, parts, total, long_form)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{stem}-organ.ly"
    write(E, path, ", the long form" if long_form else "", stem)
    print(f"organ_edition.py: {total} bars; the choir checked against the track; {path}")
    if "--log" in args:
        for k, v in E.log.items():
            print(f"  {k}: {len(v)}")
    if "--engrave" in args:
        import importlib
        try:
            exe = importlib.import_module("lilypond").executable()
        except ImportError:
            exe = shutil.which("lilypond") or sys.exit("organ_edition.py: --engrave needs LilyPond (pip install lilypond)")
        subprocess.run([str(exe), "-dno-point-and-click", "-o", str(out / f"{stem}-organ"), str(path)], check=True)

if __name__ == "__main__":
    main()
