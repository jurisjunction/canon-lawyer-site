"""
The workshop: Nand to Tetris, Part I, as a strand of the Benedict Year.

Noam Nisan and Shimon Schocken's course builds a working computer from one kind of logic gate. Part I is
the hardware, in seven projects (0 to 6). Here each project is placed beside the units of the year whose
kind of answer it shows, week by week, with the course's own lecture videos and the online IDE. Everything
here is data, and the pages are made from it:

    VIDEOS    the 49 lectures of Part I, in the playlist's order (_src/workshop/videos.txt: id|length|number|title)
    PROJECTS  one entry per project page: the units it walks beside, what is built, the weeks
              (each with its videos and its work), the paper puzzle, and notes for the parent

The build makes one page per project under /curriculum/workshop/, fills {{workshop_plan}} on the strand's
own page and {{workshop}} on each unit page, and refuses a lecture used twice or not at all, a week outside
the units a project walks beside, or weeks out of order.

The course's materials are the authors' under CC BY-NC-SA 3.0. These pages link to them and copy none of
them, and they give no solutions: the authors ask that none be posted.
"""
import html
import pathlib

esc = html.escape
INDEX = "/curriculum/workshop/"
SETUP = INDEX + "setup/"
VIDEO_FILE = pathlib.Path(__file__).parent / "_src" / "workshop" / "videos.txt"
PLAYLIST = "PLNMIACtpT9BfztU0P92qlw8Gd4vxvvfT1"
PLAYLIST_URL = f"https://www.youtube.com/playlist?list={PLAYLIST}"
IDE = "https://nand2tetris.github.io/web-ide/"
COURSE = "https://www.nand2tetris.org/course"

TOOLS = {
    "hw": ("Hardware Simulator", IDE + "chip/"),
    "cpu": ("CPU Emulator", IDE + "cpu/"),
    "asm": ("Assembler", IDE + "asm/"),
}


def _videos():
    out = {}
    for line in VIDEO_FILE.read_text(encoding="utf-8").splitlines():
        if line.strip():
            vid, length, num, title = line.split("|", 3)
            out[num] = {"id": vid, "length": length, "title": title}
    return out


VIDEOS = _videos()

# ---------------------------------------------------------------------------------------------------
# The projects. `fields` are the units of the year the project walks beside, in order; `weeks` are the
# year's week numbers, each with the lectures watched that week and what is done.

PROJECTS = [
    {
        "n": 0, "slug": "project-0", "title": "The workbench",
        "course": "Introduction",
        "fields": ["reading"],
        "lead": "Before anything is built, the whole climb is read once from the top: from one gate to a game of Tetris. Then the bench is set up.",
        "kind": "Read. The course is entered as a book is, whole and from the start, before any part of it is taken apart. You will not understand every step yet, and you are not meant to.",
        "tool": None,
        "build": [],
        "paper": "Ask everyone at the table what is inside a computer, and write down every answer without correcting any. Keep the page. You will read it again in June.",
        "weeks": [
            (1, ["0.0", "0.1"], "Watch the first two lectures together. Then draw, from memory, the ladder of the course: what is built on what."),
            (2, ["0.2", "0.3"], "Watch the next two. Mark on your ladder where this year stops (the computer and its assembler) and where a second year would go on (the software, up to Tetris)."),
            (3, ["0.4"], f"Set up the bench with the <a href=\"{SETUP}\">setup guide</a>, open the Hardware Simulator, and look around without building anything yet."),
        ],
        "parent": "Project 0 in the course is about how to hand work in on the university’s site. There is nothing to hand in here, so the last lecture is only a look at the tools. The setup guide is written to the child; read it with them the first time.",
        "unit_note": {
            "reading": "The five introductory lectures, watched as the course is read whole before it is taken apart, and the bench set up.",
        },
    },
    {
        "n": 1, "slug": "project-1", "title": "The gates",
        "course": "Boolean Logic",
        "fields": ["number", "nature"],
        "lead": "From one chip, NAND, you build every other kind of gate: fifteen chips in all. Every chip the computer will ever have is made of this one.",
        "kind": "Computed. A gate is arithmetic on true and false, and its truth table is worked out, not guessed. Morse already counts in twos. When you run a chip’s test, the comparison is found, as in Unit 3: it is a fact you look at, and it does not care what you hoped.",
        "tool": "hw",
        "build": ["Not", "And", "Or", "Xor", "Mux", "DMux", "Not16", "And16", "Or16", "Mux16", "Or8Way", "Mux4Way16", "Mux8Way16", "DMux4Way", "DMux8Way"],
        "paper": "NAND’s truth table: two inputs, four rows, and the output is 0 only when both inputs are 1. Then, still on paper, find how to make Not with one NAND, and And with two.",
        "weeks": [
            (4, ["1.1", "1.2"], "The truth tables of Not, And and Or, on paper. Then the trick from lecture 1.2: any truth table can be written as an Or of Ands."),
            (5, ["1.3", "1.4"], "How a chip is described in HDL. Write Not, And and Or in HDL on paper, before you touch the computer."),
            (6, ["1.5"], "The Hardware Simulator. Type in Not, And and Or, and run each one’s test until it passes. Then Xor."),
            (7, ["1.6", "1.7"], "Mux and DMux, on paper first: a Mux is a switch that chooses which input to pass on. Mux is the first real wall; take the week."),
            (8, [], "Buses, sixteen wires at once: Not16, And16, Or16 and Mux16. Then Or8Way."),
            (9, ["1.8"], "Mux4Way16, Mux8Way16, DMux4Way and DMux8Way: chips built out of the chips you just made. Then the gates are finished, every one passing its test."),
        ],
        "parent": "HDL describes wiring; it is not a list of steps, so the order of its lines does not matter, and every wire between parts must have a name. Bit 0 of a bus is the rightmost bit, which trips everyone once. When a chip will not pass, go back to its truth table on paper before touching the code. Project 1 is the longest project in Part I, so it walks beside two units.",
        "unit_note": {
            "number": "It begins with NAND’s truth table on paper, then Not, And and Or built from NAND alone. Every chip the computer will ever have is made of this one.",
            "nature": "It goes on: the sixteen-wire chips and the multi-way chips. Each test is a finding: a fact you look at, which does not care what you hoped.",
        },
    },
    {
        "n": 2, "slug": "project-2", "title": "The adders",
        "course": "Boolean Arithmetic",
        "fields": ["making"],
        "lead": "Out of the gates you built, a chip that adds, and then the arithmetic logic unit, the part of the computer that calculates.",
        "kind": "Made. Every chip is NAND gates given a shape. The maker arranges them, and the gates are still gates: the adder has nothing in it that the gates did not have, except the order you gave them. That is the unit’s rule in silicon.",
        "tool": "hw",
        "build": ["HalfAdder", "FullAdder", "Add16", "Inc16", "ALU"],
        "paper": "Count from 0 to 15 in binary on the fingers of one hand, a raised finger for 1. Then add two binary numbers on paper the long way, carrying as you do with ordinary numbers.",
        "weeks": [
            (10, ["2.1", "2.2"], "Binary numbers and binary addition, on paper. Then the HalfAdder and the FullAdder."),
            (11, ["2.3", "2.4"], "Negative numbers in binary, then Add16 and Inc16."),
            (12, ["2.5", "2.6"], "The ALU. Fill in its table of six control bits on paper before you build it."),
        ],
        "parent": "HDL has no “if”. When the ALU must do one thing or another, a Mux chooses, so the ALU is mostly Muxes and the chips from last term. Drawing it large on graph paper, one box per part, helps more than staring at the editor.",
        "unit_note": {
            "making": "Every chip is NAND gates given a shape: the child makes something real and adds nothing to the gates, which is the unit’s rule in silicon. Then ask what the Whisperer’s maker could give it, and what he could not.",
        },
    },
    {
        "n": 3, "slug": "project-3", "title": "Memory",
        "course": "Memory",
        "fields": ["memory"],
        "lead": "A chip that remembers. With a clock, the machine gets a before and an after, and from one remembered bit you build registers, memory and a counter.",
        "kind": "Dated. A flip-flop gives out now what it was given one tick ago. It is the first part of the machine with a past, and the clock is what dates it. The unit’s rule holds here too: first the order of the ticks, then the values.",
        "tool": "hw",
        "build": ["Bit", "Register", "RAM8", "RAM64", "RAM512", "RAM4K", "RAM16K", "PC"],
        "paper": "Draw a clock as a row of ticks along the bottom of a page. Above it, write what a one-bit memory holds at each tick if you tell it to “load 1” at tick 3 and “load 0” at tick 7.",
        "weeks": [
            (13, ["3.1", "3.2"], "Ticks and the flip-flop. Build Bit, then Register out of Bits."),
            (14, ["3.3"], "RAM8, then RAM64 out of RAM8s: the same pattern again, one size up."),
            (15, ["3.4", "3.5", "3.6"], "RAM512, RAM4K and RAM16K, then the program counter, PC."),
        ],
        "parent": "The flip-flop (DFF) is the one chip the course gives rather than has you build. It is taken on trust, as a given. A wire may loop back on itself only through a DFF; that is how the clock gives the machine a past.",
        "unit_note": {
            "memory": "The flip-flop, registers and memory. A flip-flop gives out now what it was given one tick ago. It is the first part of the machine with a before and an after, and the clock is what dates it. The unit’s rule holds here too: first the order of the ticks, then the values.",
        },
    },
    {
        "n": 4, "slug": "project-4", "title": "The machine’s language",
        "course": "Machine Language",
        "fields": ["person", "being", "god"],
        "lead": "Before building the processor, you learn to speak to it: programs written in the machine’s own language, run on an emulator of the computer you are about to build.",
        "kind": "Understood, and said by analogy. A program means something to the one who wrote it and nothing to the machine. The machine “reads” and “remembers” only by analogy, as the units on the person and on being explain. Taught: the instructions come to it from outside, with their rank and order fixed.",
        "tool": "cpu",
        "build": ["Mult.asm", "Fill.asm", "a program of your own"],
        "paper": "The computer’s screen is a grid of pixels stored in memory, sixteen pixels to a word. On graph paper, colour in the first word of the top row: which sixteen pixels is it?",
        "weeks": [
            (16, ["4.1", "4.2"], "What a machine language is. Write a two-line program on paper and read it out loud."),
            (17, ["4.3", "4.4"], "The Hack computer and its two kinds of instruction. Load a program in the CPU Emulator and step through it one instruction at a time."),
            (18, ["4.5"], "The screen and the keyboard are memory too. Draw the screen’s memory map on graph paper."),
            (19, ["4.6"], "Hack programming, part 1: registers, memory, and stopping a program properly."),
            (20, ["4.7"], "Hack programming, part 2: branches, variables and loops."),
            (21, ["4.8"], "Hack programming, part 3: pointers, and drawing on the screen."),
            (22, ["4.9"], "Mult.asm: multiply two numbers with a machine that cannot multiply."),
            (23, [], "Fill.asm: black the screen while a key is held down, white it when the key is let go."),
            (24, ["4.10"], "A program of your own: draw your initial on the screen. Keep it; you will run it again on the computer you build."),
        ],
        "parent": "This is the hardest jump in Part I, because it is the first real programming. Mult is done by adding over and over in a loop. If your child is stuck on Fill, have them write it in plain words first (“wait for a key; if pressed, paint every word black…”), then turn each line into instructions.",
        "unit_note": {
            "person": "It begins: the machine’s own language, programs written by hand and stepped through one instruction at a time. The program means something to its writer and nothing to the machine.",
            "being": "It goes on: branches, loops and pointers. Say carefully in what sense the machine “reads” or “remembers”: by analogy, and only by analogy.",
            "god": "It ends with Mult, Fill, and a program of the child’s own that draws on the screen, kept to run again later on the computer they build.",
        },
    },
    {
        "n": 5, "slug": "project-5", "title": "The computer",
        "course": "Computer Architecture",
        "fields": ["act", "city"],
        "lead": "Everything comes together: memory, the processor that runs the instructions, and the whole computer, which runs any program in the language you learned.",
        "kind": "Judged, and supplied. At each tick the processor decodes one instruction and acts on it, and what it does is settled by that instruction alone. The computer is a small city of parts, each given what the whole needs from it and nothing more.",
        "tool": "hw",
        "build": ["Memory", "CPU", "Computer"],
        "paper": "Write one instruction, for example D=M+1, as its sixteen bits. Underline the bits that choose what the ALU computes, and circle the ones that say where the answer goes.",
        "weeks": [
            (25, ["5.1", "5.2"], "The idea of a stored-program computer, and the fetch-execute cycle: fetch an instruction, carry it out, fetch the next."),
            (26, ["5.3"], "The CPU, explained. Copy the course’s CPU diagram large onto graph paper."),
            (27, ["5.4"], "The whole Hack computer: memory, CPU and the program’s memory together."),
            (28, ["5.5"], "Build Memory: the RAM, the screen and the keyboard joined into one address space."),
            (29, [], "Build the CPU, one part of the diagram at a time. Label every control wire with the instruction bit that drives it."),
            (30, ["5.6"], "Build the Computer, and run its tests: your computer runs the course’s programs."),
        ],
        "parent": "The CPU is the hardest chip in Part I. Let it take two weeks if it needs them, and spend the extra time on the diagram, not on the editor. Every wire in the drawing is a line of HDL.",
        "unit_note": {
            "act": "It begins: the fetch-execute cycle and the processor. At each tick the CPU decodes one instruction and acts on it, settled by that instruction alone.",
            "city": "It ends: memory, the CPU and the whole Computer, a small city of parts, each given what the whole needs from it.",
        },
    },
    {
        "n": 6, "slug": "project-6", "title": "The assembler",
        "course": "Assembler",
        "fields": ["law"],
        "lead": "The translator from the language people write to the ones and zeros the machine runs. Done by hand, it is a code to break, like the Morse of Unit 2.",
        "kind": "Enacted. The instruction set is a law the machine keeps from without, never from within. The assembler applies the code exactly as it is written, line by line, as a rule is applied.",
        "tool": "asm",
        "build": ["Add.asm, translated by hand", "Max.asm, translated by hand", "Rect.asm, translated by hand"],
        "paper": "Turn @17 into sixteen bits. Then turn D=M+1 into sixteen bits with the course’s tables. Check both with the Assembler.",
        "weeks": [
            (31, ["6.1", "6.2", "6.3"], "What an assembler is, and how each kind of instruction is translated. Translate Add.asm by hand and check it against the Assembler in the IDE."),
            (32, ["6.4", "6.6B"], "Symbols: labels and variables. Translate Max.asm by hand, finding the labels first and then everything else, as the lecture does."),
            (33, ["6.5", "6.6", "6.7"], "Rect.asm by hand. Lectures 6.5 and 6.6 show how to write an assembler as a program; that is for a second year, so watch them as a look ahead."),
        ],
        "parent": "The course lets the assembler be written as a program or done by hand, and lecture 6.6B covers the by-hand way. A child who knows Scratch can build a small assembler there, with lists for the course’s tables, but it is not needed. Writing it in a real programming language is for a second year.",
        "unit_note": {
            "law": "By hand: turning <code>@17</code> or <code>D=M+1</code> into sixteen ones and zeros with the course’s tables is a code to break, like Unit 2’s Morse. The instruction set is a law the machine keeps from without, never from within.",
        },
    },
    {
        "n": 7, "slug": "the-machine-runs", "title": "The machine runs",
        "course": None,
        "fields": ["worship"],
        "lead": "Nothing new is built. The program you wrote in Project 4 runs on the computer you built in Project 5, and the family comes to watch.",
        "kind": "Witnessed. A thing shown, not proved. The machine does what it is for, and none of its parts knows it. What it is for is in the one who made it and in the ones it serves.",
        "tool": "hw",
        "build": [],
        "paper": "Read again the page from Project 0, where everyone at the table said what is inside a computer. Write next to each answer what you now know.",
        "weeks": [
            (34, [], "Translate your own program from week 24 by hand into ones and zeros, as in Project 6."),
            (35, [], "Load it into the computer you built and run it. The course’s Computer tests load a program before they run; load yours the same way."),
            (36, [], "Show it to the family. Then watch lecture 0.3 again, From Hack to Tetris: the climb that a second year would take."),
        ],
        "parent": "Nothing here is graded. The child explains the computer to someone, from the gate to the screen. Let them run the show.",
        "unit_note": {
            "worship": "The child’s own program, assembled by hand, on the computer they built from NAND, shown to the family. Nothing new is built and nothing is graded.",
        },
    },
]

BY_FIELD = {f: p for p in PROJECTS for f in p["fields"]}


def path(p):
    return f"{INDEX}{p['slug']}/"


def label(p):
    return f"Project {p['n']}" if p["course"] else "The last weeks"


def video_url(num):
    return f"https://www.youtube.com/watch?v={VIDEOS[num]['id']}&list={PLAYLIST}"


def _seconds(length):
    parts = [int(x) for x in length.split(":")]
    s = 0
    for x in parts:
        s = s * 60 + x
    return s


def minutes(nums):
    return round(sum(_seconds(VIDEOS[n]["length"]) for n in nums) / 60)


def _span(u):
    a, b = u["weeks"].split("–")
    return range(int(a), int(b) + 1)


def check(units):
    """Refuse a lecture used twice or not at all, a week outside a project's units, and weeks out of order."""
    by_field = {u["field"]: u for u in units}
    used = []
    last = 0
    for p in PROJECTS:
        allowed = set()
        for f in p["fields"]:
            if f not in by_field:
                raise SystemExit(f"workshop: {p['slug']} walks beside unknown unit {f!r}")
            allowed.update(_span(by_field[f]))
        for w, nums, _ in p["weeks"]:
            if w not in allowed:
                raise SystemExit(f"workshop: {p['slug']} week {w} is outside its units")
            if w <= last:
                raise SystemExit(f"workshop: week {w} is out of order")
            last = w
            for n in nums:
                if n not in VIDEOS:
                    raise SystemExit(f"workshop: {p['slug']} names unknown lecture {n}")
                used.append(n)
    dup = {n for n in used if used.count(n) > 1}
    if dup:
        raise SystemExit(f"workshop: lectures used twice: {sorted(dup)}")
    missing = set(VIDEOS) - set(used)
    if missing:
        raise SystemExit(f"workshop: lectures not used: {sorted(missing)}")


def _units_of(p, units):
    by_field = {u["field"]: u for u in units}
    return [by_field[f] for f in p["fields"]]


def _unit_link(u):
    import essay_map
    return f'<a href="{u["path"]}">Unit {u["unit"]} · {esc(essay_map.BY_SLUG[u["field"]]["name"])}</a>'


def _weeks_txt(p):
    ws = [w for w, _, _ in p["weeks"]]
    return f"week {ws[0]}" if len(ws) == 1 else f"weeks {ws[0]}–{ws[-1]}"


def _lectures(p):
    return [n for _, nums, _ in p["weeks"] for n in nums]


def _video_list(nums):
    if not nums:
        return ""
    items = "".join(
        f'<li><a href="{video_url(n)}" rel="noopener">{n} {esc(VIDEOS[n]["title"])}</a> <span class="reg-inline">{VIDEOS[n]["length"]}</span></li>'
        for n in nums)
    return f'<ul class="workshop-videos">{items}</ul>'


def _crumbs():
    return f'<p class="crumbs"><a href="/curriculum/">The Benedict Year</a> › <a href="{INDEX}">The workshop</a></p>'


def _nav(prev_html, next_html, extra=""):
    return f"""
<section class="section map-nav-band">
  <div class="wrap narrow">
    <nav class="map-nav" aria-label="In the workshop">
      <p class="eyebrow">In the workshop</p>
      {prev_html}
      {next_html}
      {extra}
      <p class="more"><a href="{INDEX}">The whole strand →</a> · <a href="{SETUP}">Setting up →</a></p>
    </nav>
  </div>
</section>
"""


def project_page(i, units):
    p = PROJECTS[i]
    us = _units_of(p, units)
    lectures = _lectures(p)
    def watch(nums):
        return "; ".join(f'<a href="{video_url(n)}" rel="noopener">{n}</a>' for n in nums) or "—"
    rows = "".join(
        f'<tr><td data-label="Week">Week {w}</td><td data-label="Watch">{watch(nums)}</td><td data-label="Do">{do}</td></tr>'
        for w, nums, do in p["weeks"])
    if p["tool"]:
        tname, turl = TOOLS[p["tool"]]
        where = (f'In the <a href="{turl}" rel="noopener">{tname}</a>'
                 + (f', choose <strong>Project {p["n"]}</strong> from the list at the top, then each chip in turn.' if p["tool"] == "hw" and p["course"] else
                    f'. The files for Project {p["n"]} are in the IDE’s own projects folder, so there is nothing to download.' if p["course"] else "."))
    else:
        where = ""
    build = ""
    if p["build"]:
        chips = "".join(f"<li>{esc(c)}</li>" if " " in c else f"<li><code>{esc(c)}</code></li>" for c in p["build"])
        build = f"""<h2>What you build</h2>
      <p>{where}</p>
      <ul class="workshop-chips">{chips}</ul>
      <p>Each one is done when its test passes in the IDE. A pass cannot be argued with, and neither can a fail.</p>"""
    elif where:
        build = f"<h2>Where</h2><p>{where}</p>"
    lect_html = ""
    if lectures:
        lect_html = f"""<h2>The lectures</h2>
      <p>{len(lectures)} lecture{"s" if len(lectures) != 1 else ""}, about {minutes(lectures)} minutes in all, by Nisan and Schocken. Watch with your parent, one or two at a sitting.</p>
      {_video_list(lectures)}"""
    course_line = (f'<p class="essay-meta">In the course: Project {p["n"]}, {esc(p["course"])} · '
                   f'<a href="{COURSE}" rel="noopener">slides and project notes at nand2tetris.org</a></p>') if p["course"] else ""
    units_line = " and ".join(_unit_link(u) for u in us)
    body = f"""<section class="page-head">
  <div class="wrap narrow">
    {_crumbs()}
    <p class="eyebrow">{esc(label(p))} · {_weeks_txt(p).capitalize()}</p>
    <h1>{esc(p['title'])}</h1>
    <p class="lead">{p['lead']}</p>
    <p class="essay-meta">Beside {units_line}</p>
    {course_line}
  </div>
</section>

<section class="section">
  <div class="wrap narrow">
    <div class="prose">
      <h2>The kind of answer</h2>
      <p>{p['kind']}</p>
      <h2>On paper first</h2>
      <p>{p['paper']}</p>
      {build}
      <h2>Week by week</h2>
      <p>About an afternoon a week. If a week runs long, let it: the strand keeps its own order, not the calendar’s.</p>
      <table class="deadlines curriculum-table">
        <thead><tr><th>Week</th><th>Watch</th><th>Do</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
      {lect_html}
      <h2>For the parent</h2>
      <p class="note">{p['parent']}</p>
    </div>
  </div>
</section>
"""
    prev_p = PROJECTS[i - 1] if i > 0 else None
    next_p = PROJECTS[i + 1] if i + 1 < len(PROJECTS) else None
    prev_html = f'<p><span class="map-nav-label">Before it</span> <a href="{path(prev_p)}">{esc(label(prev_p))} · {esc(prev_p["title"])}</a></p>' if prev_p else ""
    next_html = f'<p><span class="map-nav-label">After it</span> <a href="{path(next_p)}">{esc(label(next_p))} · {esc(next_p["title"])}</a></p>' if next_p else ""
    extra = "".join(f'<p><span class="map-nav-label">In the year</span> {_unit_link(u)}</p>' for u in us)
    body += _nav(prev_html, next_html, extra)
    plain = html.unescape(p["lead"])
    meta = {"title": f"{label(p)}: {p['title']} · The workshop",
            "crumb": p["title"],
            "description": f"{label(p)} of the workshop, the Benedict Year’s strand of Nand to Tetris for ages 10 to 13: {plain}",
            "path": path(p), "nav": "essays", "kind": "workshop-project", "summary": plain}
    return meta, body


def plan_section(units):
    """The strand at a glance, for {{workshop_plan}}: each project, the units it walks beside, and its lectures."""
    rows = []
    for p in PROJECTS:
        us = _units_of(p, units)
        lectures = _lectures(p)
        watch = f"{len(lectures)} lectures, about {minutes(lectures)} min" if lectures else "—"
        rows.append(
            f'<tr><td data-label="Project"><a href="{path(p)}">{esc(label(p))} · {esc(p["title"])}</a></td>'
            f'<td data-label="Beside">{", ".join(_unit_link(u) for u in us)} · {_weeks_txt(p)}</td>'
            f'<td data-label="Watch">{watch}</td></tr>')
    total = minutes(list(VIDEOS))
    return f"""<table class="deadlines curriculum-table">
        <thead><tr><th>Project</th><th>Beside</th><th>Watch</th></tr></thead>
        <tbody>{"".join(rows)}</tbody>
      </table>
      <p class="field-also">All {len(VIDEOS)} lectures of Part I come to about {total // 60} hours {total % 60} minutes, or about twenty minutes a week.</p>"""


def unit_section(field):
    """The workshop's line on a unit page, for {{workshop}}."""
    p = BY_FIELD.get(field)
    if not p:
        return ""
    return (f'<h2>The workshop · suggested</h2>\n      <p>For a child taking the <a href="{INDEX}">workshop strand</a>, '
            f'<a href="{path(p)}">{esc(_low(label(p)) if not p["course"] else label(p))}, {esc(_low(p["title"]))}</a>. {p["unit_note"][field]}</p>')


def _low(s):
    return s[0].lower() + s[1:]


def pages(units):
    check(units)
    return [project_page(i, units) for i in range(len(PROJECTS))]
