// ============================================================
// A NEW SONG — a motet for the household
// "O sing unto the LORD a new song" (Psalm 98:1) · mode VII x motet
// 120 BPM · 72 bars · ~2:24, then it loops
// For Strudel (https://strudel.cc): paste, press play (Ctrl+Enter).
// Dedicated to the public domain (CC0 1.0).
//
// The tracks of the essays form a family, and this is the first
// song they sing together. It is built as a medieval motet: a chant
// in long notes at the bottom, the tenor, and newer voices above it,
// each with its own words, sung at once. The tenor is the line every
// track in the family shares, the Ascension introit "Viri Galilaei".
// Above it the children: the Lenin track's hook as the motetus, and
// Francis's canticle from "Brother Electron" as the triplum. Each is
// sung in the household's mode, the chant's own (G mixolydian), and
// each keeps its own family's instrument: the cloud's choir, the
// garage guitar, the recorder and the square waves of the chip.
// Elijah's commission is the household's rule: "he shall turn the
// heart of the fathers to the children, and the heart of the children
// to their fathers" (Malachi 4:6).
//
// It begins as Elisha asked: "bring me a minstrel" (2 Kings 3:15),
// and a harp plays. Elisha had asked Elijah for "a double portion of
// thy spirit" (2 Kings 2:9), and took up the mantle that fell from
// him. So at the end the mantle falls: the tenor's chant goes up to
// the top, doubled, in three voices, and the children's tunes go
// down beneath it. Things new and old (Matthew 13:52): the new song
// is made of the old ones.
//
// The code is a DAG, like the essays. Each part names its PARENTS,
// the parts it is made from, which stand above it; some name what
// they are FOR, a later part they foreshadow.
//
// PARENTS. A track carries its parents in its own material. This one
// has three, so it quotes all three, each line with a short hash of
// the parent's original (sha256 of the quoted text, first 12 hex):
//   whether-the-cloud.strudel.js   VIRI       fd123dbc28e8
//   whether-the-cloud.strudel.js   TELEGRAPH  019cbc25c20f
//   what-is-to-be-done.strudel.js  MOTETUS    ab1eec72525c
//   what-is-to-be-done.strudel.js  CARPENTER  3b8716d43c19
//   brother-electron.strudel.js    TRIPLUM    2b82b56f32b5
//
// TIMELINE (bar / time):
//   MINSTREL   1  0:00  "bring me a minstrel": a harp; then the
//                       hand of the LORD, an open fifth
//   TENOR      9  0:16  Viri Galilaei in long notes; the cloud's
//                       telegraph taps beneath it
//   MANTLE    17  0:32  the motetus: the Lenin hook above the tenor,
//                       and the carpenter's hammer
//   PORTION   33  1:04  the triplum: Francis's canticle, on recorder,
//                       then on the gates; three texts at once
//   WATERS    49  1:36  the mantle falls: the chant on top, doubled,
//                       the children beneath; the waters part
//   AMEN      65  2:08  things new and old; one chord; then
//                       Elijah's commission, in the silence
//
// The words are chanted, not spoken. SAM, the Software Automatic
// Mouth, a speech program of 1982, reads each line as a lector chants
// a reading: recited on D, falling through C to B; the question rises
// back to D, and the last line falls home to G. It is a machine's
// voice and sounds like one. At the waters, when the mantle falls,
// the voice ascends: the last four lines pass to a small choir an
// octave up, in fauxbourdon, which keeps SAM's words and not its
// buzz. Both stand in until people sing it; the score is on the site.
// The lines load from canon-lawyer.ca the first time they play; if
// they are slow, stop and play again.
// ============================================================

setcpm(120/4) // one cycle = one bar, the household's tempo

// the lines, in the order they come: SAM's until the waters, then the
// choir's (sam.mjs and ascend.py on the site make them)
samples({
  bring_me_a_minstrel: 'sam/bring_me_a_minstrel.wav',
  o_sing_unto_the_lord_a_new_song: 'sam/o_sing_unto_the_lord_a_new_song.wav',
  let_a_double_portion_of_thy_spirit_be_upon_me: 'sam/let_a_double_portion_of_thy_spirit_be_upon_me.wav',
  a_new_man_knows_a_new_song: 'sam/a_new_man_knows_a_new_song.wav',
  the_singer_himself_is_the_praise: 'sam/the_singer_himself_is_the_praise.wav',
  where_is_the_lord_god_of_elijah: 'ascended/where_is_the_lord_god_of_elijah.wav',
  the_spirit_of_elijah_doth_rest_on_elisha: 'ascended/the_spirit_of_elijah_doth_rest_on_elisha.wav',
  things_new_and_old: 'ascended/things_new_and_old.wav',
  he_shall_turn_the_heart_of_the_fathers_to_the_children: 'ascended/he_shall_turn_the_heart_of_the_fathers_to_the_children.wav',
}, 'https://www.canon-lawyer.ca/assets/music/voices/a-new-song/')

// ============================================================
// ORBITS: 1 drums and telegraph · 2 guitar and the chip ·
//         3 the chanted lines · 4 organ, harp and bells · 5 the waters ·
//         6 choir · 7 recorder
// ============================================================

// ---------------- ROOTS

// ROOT 1. THE MODE: the household's, the chant's own. G mixolydian.
// parents: none (it is the tenor's, and a motet keeps the tenor's mode)
const MODE = 'mixolydian'
const STEPS = { major: [0, 2, 4, 5, 7, 9, 11], mixolydian: [0, 2, 4, 5, 7, 9, 10] }

// ---------------- PARENTS
// from whether-the-cloud.strudel.js: "Viri Galilaei", quoted as
// written (sha256 fd123dbc28e8), and its telegraph (019cbc25c20f)
const VIRI = 'g3@2 g3@2 g3 c4 b3 c4@2 d4 c4 e4 d4 d4@3'
const TELEGRAPH = 'WHAT HATH GOD WROUGHT'
// from what-is-to-be-done.strudel.js: its hook (ab1eec72525c), in D
// major, and its hammer (3b8716d43c19)
const MOTETUS = 'a4@2 a4 b4 a4@2 f#4@2 ~@2 d4 e4 f#4@2 e4@2 d5@2 c#5 b4 a4@2 b4@2 a4@6 ~@2'
const CARPENTER = 'IS NOT THIS THE CARPENTER'
// from brother-electron.strudel.js: Francis's canticle (2b82b56f32b5),
// in A mixolydian
const TRIPLUM = 'a4 a4 b4 c#5@2 b4 a4@2 g4 a4 b4@2 a4@4 e5 d5 c#5 b4 c#5@2 b4 a4 g4@2 e4@2 a4@4'

// ---------------- SUNG IN THE HOUSEHOLD'S MODE
// Each line is read as steps of its own scale, from its own final,
// and sung on the same steps of the household's. The chant and the
// canticle are in this mode already, so they are only moved; the
// Lenin hook, in major, gives up its leading note for the chant's
// flat seventh.
// parents: THE MODE, PARENTS
const PC = { c: 0, d: 2, e: 4, f: 5, g: 7, a: 9, b: 11 }
const midiOf = (t) => {
  const m = t.match(/^([a-g])(#|b)?(\d)$/)
  return 12 * (+m[3] + 1) + PC[m[1]] + (m[2] === '#' ? 1 : m[2] === 'b' ? -1 : 0)
}
const stepOf = (note, final, mode) => {
  for (let d = -21; d <= 28; d++) {
    const o = Math.floor(d / 7), k = ((d % 7) + 7) % 7
    if (midiOf(final) + 12 * o + STEPS[mode][k] === midiOf(note)) return d
  }
  throw new Error(note + ' is not in ' + final + ' ' + mode)
}
const inMode = (phrase, final, mode) => phrase.split(' ').map((t) => {
  const [p, d] = t.split('@')
  return (p === '~' ? '~' : stepOf(p, final, mode)) + (d ? '@' + d : '')
}).join(' ')
const sing = (phrase, final, mode, home, bars) => n(mini(inMode(phrase, final, mode))).scale(home).slow(bars)

// ---------------- THE TENOR: the chant every track shares, in long
// notes, four times slower than the cloud sang it: eight bars a statement.
// parents: PARENTS (VIRI), SUNG IN THE HOUSEHOLD'S MODE
// for: WATERS (where it goes up to the top)
const tenor = (g = .3) => stack(
  sing(VIRI, 'g3', 'mixolydian', 'G2:' + MODE, 8).s('gm_choir_aahs')
    .attack(.3).release(1.2).gain(g * 3).room(.6).roomsize(6).orbit(6),
  sing(VIRI, 'g3', 'mixolydian', 'G2:' + MODE, 8).s('gm_church_organ')
    .attack(.2).release(1).gain(.05 * 3).room(.5).orbit(4),
)

// ---------------- THE MOTETUS: the Lenin hook, on the garage's clean guitar
// parents: PARENTS (MOTETUS), SUNG IN THE HOUSEHOLD'S MODE
const motetus = (home = 'G3:' + MODE, g = .26) => sing(MOTETUS, 'd4', 'major', home, 4)
  .s('gm_electric_guitar_clean').release(.5).gain(g * 3).delay(".25:.25:.3").room(.4).pan(.35).orbit(2)

// ---------------- THE TRIPLUM: Francis's canticle, on the recorder and on the gates
// parents: PARENTS (TRIPLUM), SUNG IN THE HOUSEHOLD'S MODE
const triplum = (home = 'G4:' + MODE, g = .26) => sing(TRIPLUM, 'a3', 'mixolydian', home, 4)
  .s('gm_recorder').release(.3).gain(g * 3).delay(".25:.25:.3").room(.4).pan(.62).orbit(7)
const gates = (home = 'G4:' + MODE) => sing(TRIPLUM, 'a3', 'mixolydian', home, 4)
  .s('square').attack(.005).decay(.12).sustain(.35).release(.1).lpf(3000).gain(.1).pan(.62).orbit(2)

// ---------------- THE TELEGRAPH AND THE HAMMER: Morse, as in the parents
// dot 1 sixteenth, dash 3; 1 between signs, 3 between letters, 7 between words
// parents: PARENTS (the two Morse lines)
const CODE = { A: '.-', C: '-.-.', D: '-..', E: '.', G: '--.', H: '....', I: '..', N: '-.', O: '---',
               P: '.--.', R: '.-.', S: '...', T: '-', U: '..-', W: '.--' }
const morse = (text) => text.split(' ').map((word) =>
  word.split('').map((ch) =>
    CODE[ch].split('').map((sign) => (sign === '.' ? 'x' : 'x@3')).join(' ~ ')
  ).join(' ~@3 ')
).join(' ~@7 ') + ' ~@7'
const units = (talea) => talea.split(' ').reduce((k, t) => k + (t.includes('@') ? +t.split('@')[1] : 1), 0)
const tap = (text, sound) => {
  const talea = morse(text)
  return s(sound).struct(mini(talea)).slow(units(talea) / 16).bank('RolandTR909')
}

// ---------------- THE MINSTREL: "and it came to pass, when the minstrel
// played, that the hand of the LORD came upon him."
// parents: THE MODE
// for: AMEN (its first chord is the last)
const harp = n("0 2 4 7 9 7 4 2").scale('G3:' + MODE).s('gm_orchestral_harp')
  .release(1.5).gain(.3 * 3).room(.5).roomsize(4).pan(sine.slow(4).range(.35, .65)).orbit(4)
const fifth = note("[g2,d3]").s('gm_church_organ').attack(2).release(2).gain(.06 * 3).room(.6).orbit(4)

// ---------------- THE CLOCK: the chip's, lightly
const clock = stack(
  s("bd ~ ~ ~ bd ~ bd ~").bank('RolandTR909').gain(.6).orbit(1),
  s("~ ~ sd ~ ~ ~ sd ~").bank('RolandTR909').gain(.35).room(.2).orbit(1),
  s("hh*8").bank('RolandTR909').gain(".18 .1 .15 .1").hpf(6000).orbit(1),
)

// ---------------- THE WATERS: "he smote the waters ... and they parted
// hither and thither" (2 Kings 2:14)
const waters = stack(
  s('white').lpf(saw.slow(2).range(5000, 400)).gain(saw.slow(2).range(.1, 0)).pan(saw.slow(2).range(.5, 0)).orbit(5),
  s('white').lpf(saw.slow(2).range(5000, 400)).gain(saw.slow(2).range(.1, 0)).pan(saw.slow(2).range(.5, 1)).orbit(5),
)

// ---------------- VOICES: SAM, chanting; then the choir
const vox = (p, g = 1) => s(p).hpf(80).lpf(8000).gain(g)
  .delay(".12:.25:.25").room(.25).orbit(3)

// ============================================================
// SECTIONS
// ============================================================

// I. MINSTREL. "But now bring me a minstrel."
// parents: THE MINSTREL
const secMINSTREL = stack(
  harp,
  fifth.mask("<0 0 0 0 1 1 1 1>"),
  vox("<~ bring_me_a_minstrel ~ ~ ~ ~ ~ ~>"),
)

// II. TENOR. "O sing unto the LORD a new song." The chant alone, in
// long notes, with the cloud's telegraph beneath it.
// parents: THE TENOR, THE TELEGRAPH
const secTENOR = stack(
  tenor(), fifth,
  tap(TELEGRAPH, 'rim').gain(.28).hpf(1200).pan(.6).orbit(1),
  vox("<o_sing_unto_the_lord_a_new_song ~ ~ ~ ~ ~ ~ ~>"),
)

// III. MANTLE. "Let a double portion of thy spirit be upon me." The
// first child sings above the tenor; the hammer taps.
// parents: THE TENOR, THE MOTETUS, THE TELEGRAPH AND THE HAMMER
const secMANTLE = stack(
  tenor(), fifth,
  motetus(),
  tap(CARPENTER, 'rim').gain(.32).pan(.35).orbit(1).mask("<0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0>"),
  vox("<let_a_double_portion_of_thy_spirit_be_upon_me ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~>"),
)

// IV. PORTION. "A new man knows a new song" (Augustine, Sermon 34).
// The second child above the first: the canticle on the recorder,
// then on the gates; three texts at once.
// parents: THE TENOR, THE MOTETUS, THE TRIPLUM, THE CLOCK
const secPORTION = stack(
  tenor(.28), motetus(),
  triplum().mask("<1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0>"),
  gates().mask("<0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1>"),
  clock.mask("<0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1>"),
  vox("<a_new_man_knows_a_new_song ~ ~ ~ ~ ~ ~ ~ the_singer_himself_is_the_praise ~ ~ ~ ~ ~ ~ ~>"),
)

// V. WATERS. "Where is the LORD God of Elijah?" The mantle falls: the
// tenor's chant goes up and is sung on top, doubled, in three voices
// (fauxbourdon, as in "Brother Electron"); the children's tunes go
// down beneath it.
// parents: THE TENOR, THE MOTETUS, THE TRIPLUM, THE WATERS
const MANTLE_UP = (lift) => stack(...[0, -3, -5].map((under) =>
  n(mini(inMode(VIRI, 'g3', 'mixolydian')).add(under + lift)).scale('G4:' + MODE)))
const secWATERS = stack(
  MANTLE_UP(0).slow(4).s('gm_choir_aahs').attack(.1).release(.8).gain(.3 * 3).room(.6).roomsize(6).orbit(6),
  MANTLE_UP(7).slow(4).s('gm_celesta').release(.8).gain(.14 * 3).room(.6).orbit(4).mask("<0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1>"),
  motetus('G2:' + MODE, .22),
  triplum('G2:' + MODE, .2),
  waters.mask("<1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0>"),
  clock,
  vox("<where_is_the_lord_god_of_elijah ~ ~ ~ ~ ~ ~ ~ the_spirit_of_elijah_doth_rest_on_elisha ~ ~ ~ ~ ~ ~ ~>"),
)

// VI. AMEN. "Things new and old." The minstrel's first chord, held;
// then, in the silence, the last word of the old prophets, which is
// about Elijah: "he shall turn the heart of the fathers to the
// children" (Malachi 4:6).
// parents: THE MINSTREL, THE TENOR
const CHORD = "[g2,d3,g3,b3,d4,g4]"
const secAMEN = stack(arrange(
  [4, stack(
    note(CHORD).s('gm_church_organ').attack(.05).release(4).gain(.1 * 3).room(.7).roomsize(6),
    note(CHORD).s('gm_choir_aahs').attack(.1).release(4).gain(.24 * 3).room(.7).roomsize(6),
    note(CHORD).s('gm_orchestral_harp').release(3).gain(.25 * 3).room(.6),
  ).slow(4).orbit(4)],
  [4, silence],
), vox("<things_new_and_old ~ ~ ~ he_shall_turn_the_heart_of_the_fathers_to_the_children ~ ~ ~>"))

// ============================================================
// THE ARRANGEMENT
// ============================================================
arrange(
  [8,  secMINSTREL],
  [8,  secTENOR],
  [16, secMANTLE],
  [16, secPORTION],
  [16, secWATERS],
  [8,  secAMEN],
)
