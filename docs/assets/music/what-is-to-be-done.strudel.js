// ============================================================
// WHAT IS TO BE DONE? — the garage mix
// In the register of V. I. Lenin · D major x garage power pop
// 132 BPM · 102 bars · ~3:05, then it loops
// For Strudel (https://strudel.cc): paste, press play (Ctrl+Enter).
// Dedicated to the public domain (CC0 1.0).
//
// Lenin's worst word for the small circle was kustarnichestvo:
// cottage craft, the work of amateurs with their own tools. So
// this is a garage band. A clean guitar asks the question of Acts
// 2:37, "what shall we do?", and leaves it open on the dominant.
// The band answers together; a great chord from outside swamps it;
// it rebuilds itself by hand while a hammer taps, in Morse, IS NOT
// THIS THE CARPENTER (Mark 6:3). Then the hook is passed round as
// a round, voice after voice. At the end the snare taps BREAK THE
// BREAD PASS IT ROUND, and the last chord rings while a voice says
// the essay's last line.
//
// The code is a little DAG. Every part below is made from parts
// above it and names them as its parents, the way each entry in
// the record names the entries it came from. One part has no
// parents: the cloud, which is brought from without.
//
// PARENTS. The tracks, like the essays, form a DAG, and a track
// carries its parents in its own material. This essay cites
// "Whether the Cloud Makes Many Worlds" in its first section, so
// in HANDS the band comes in under that track's hook, Viri
// Galilaei, moved from G to D on the same choir, and its telegraph,
// WHAT HATH GOD WROUGHT; then this track's own hook takes over.
// Each quoted line keeps a short hash of the parent's original
// (sha256 of the quoted text, first 12 hex), so it can be checked:
//   whether-the-cloud.strudel.js  VIRI   fd123dbc28e8
//   whether-the-cloud.strudel.js  TALEA  019cbc25c20f
//
// TIMELINE (bar / time):
//   PREFACE    1  0:00  the question: a clean guitar, left open on A
//   HANDS      9  0:15  the band comes in together, holding hands,
//                       under the parent: Viri Galilaei, in D;
//                       at bar 17 the hook: "what is to be done?"
//   WITHOUT   25  0:44  a great chord from outside swells; the band
//                       is filtered away beneath it; one bar of nothing
//   SHOP      33  0:58  kustarnichestvo: a hammer taps the carpenter
//                       in Morse; the band rebuilt by hand, four bars
//                       at a time
//   ROUND     49  1:27  the little DAG: the hook passed round, each
//                       voice a bar behind the last
//   LAMP      65  1:56  a lamp for the house, a lantern for the road
//                       (Psalm 119:105); a drum roll back in
//   TABLE     73  2:11  the common table: everyone; the snare taps
//                       BREAK THE BREAD PASS IT ROUND
//   END       97  2:55  three hits, the chord rings, the last line
//   tail     101  3:02  silence for the reverb
//
// The spoken lines come from Shabda's text-to-speech and load the
// first time they play. If they are slow, stop and play again.
// ============================================================

setcpm(132/4) // one cycle = one bar

// ---- the spoken lines
samples('shabda/speech/en-GB/f:what_is_to_be_done,thy_word_is_a_lamp_unto_my_feet,break_the_bread,pass_it_round,write_down_who_was_there')
samples('shabda/speech/en-GB/m:men_and_brethren_what_shall_we_do,brought_to_them_from_without,is_not_this_the_carpenter,give_us_a_table')

// ============================================================
// ORBITS: 1 drums · 2 guitars and bass · 3 spoken word ·
//         4 keys and bells · 5 the cloud · 6 choir
// Strudel plays soundfonts at 0.3 of their gain, so the
// instruments are lifted (gain x 3) to sit with the drums.
// ============================================================

// ---------------- ROOTS: the two things everything is made of

// ROOT 1. THE QUESTION: four chords, I vi IV V, D Bm G A.
// parents: none (it is asked)
const QUESTION = "<[d3,a3,d4] [b2,f#3,b3] [g2,d3,g3] [a2,e3,a3]>"
const ARPEGGIO = "<[d3 a3 d4 f#4 a4 f#4 d4 a3] [b2 f#3 b3 d4 f#4 d4 b3 f#3] [g2 d3 g3 b3 d4 b3 g3 d3] [a2 e3 a3 c#4 e4 c#4 a3 e3]>"
const ROOTS = "<d2 b1 g1 a1>"

// ROOT 2. THE HOOK: four bars on the eighth-note grid.
// "What is to be done? ... Break the bread, pass it round."
// parents: none (it is the answer)
const HOOK = 'a4@2 a4 b4 a4@2 f#4@2 ~@2 d4 e4 f#4@2 e4@2 d5@2 c#5 b4 a4@2 b4@2 a4@6 ~@2'
const hook = () => note(mini(HOOK)).slow(4)

// ---------------- PARENTS: from whether-the-cloud.strudel.js
// the Ascension introit, "Viri Galilaei", two bars, quoted as written
// in G (sha256 fd123dbc28e8) and sung a fifth higher, in D
const VIRI = 'g3@2 g3@2 g3 c4 b3 c4@2 d4 c4 e4 d4 d4@3'
const viri = () => note(mini(VIRI)).slow(2).transpose(7)
// the first telegraph message, quoted as written (sha256 019cbc25c20f)
const PARENT_TALEA = 'WHAT HATH GOD WROUGHT'

// the verse turns the question round: I V vi IV
// parents: QUESTION
const VERSE = "<[d3,a3,d4] [a2,e3,a3] [b2,f#3,b3] [g2,d3,g3]>"
const VERSE_ROOTS = "<d2 a1 b1 g1>"

// ---------------- THE TELEGRAPH: Morse, as in the cloud's track
// dot 1 sixteenth, dash 3; 1 between signs, 3 between letters, 7 between words
const CODE = { A: '.-', B: '-...', C: '-.-.', D: '-..', E: '.', G: '--.', H: '....', I: '..', K: '-.-',
               N: '-.', O: '---', P: '.--.', R: '.-.', S: '...', T: '-', U: '..-', W: '.--' }
const morse = (text) => text.split(' ').map((word) =>
  word.split('').map((ch) =>
    CODE[ch].split('').map((sign) => (sign === '.' ? 'x' : 'x@3')).join(' ~ ')
  ).join(' ~@3 ')
).join(' ~@7 ') + ' ~@7'
const units = (talea) => talea.split(' ').reduce((n, t) => n + (t.includes('@') ? +t.split('@')[1] : 1), 0)
const telegraph = (text, sound) => {
  const talea = morse(text)
  return s(sound).struct(mini(talea)).slow(units(talea) / 16).bank('RolandTR909')
}

// ---------------- THE GROUP: holding each other by the hand
// parents: QUESTION (through VERSE)
const kick = s("bd ~ ~ bd bd ~ ~ ~").bank('RolandTR909').gain(.9).orbit(1)
const snare = s("~ ~ sd ~ ~ ~ sd ~").bank('RolandTR909').gain(.7).room(.15).orbit(1)
const hats = s("hh*8").bank('RolandTR909').gain(".3 .18 .26 .18").hpf(5000).orbit(1)
const crash = s("<cr ~ ~ ~>").bank('RolandTR909').gain(.35).orbit(1)
const fill = s("<~ ~ ~ [~ ~ ~ ~ lt mt ht ht]>").bank('RolandTR909').gain(.6).orbit(1)
const drums = stack(kick, snare, hats, crash, fill)
const bass = (roots) => note(roots).struct("x*8").s('gm_electric_bass_pick')
  .clip(.85).release(.05).lpf(1800).gain(.32 * 3).orbit(2)
const chug = (chords, g = .2) => note(chords).struct("x*8").s('gm_overdriven_guitar')
  .clip(.7).release(.08).lpf(3200).gain(g * 3).pan(.4).orbit(2)
const organ = (chords) => note(chords).s('gm_drawbar_organ')
  .attack(.02).release(.4).gain(.07 * 3).pan(.62).room(.3).orbit(4)
const group = (chords, roots) => stack(drums, bass(roots), chug(chords), organ(chords))

// ---------------- THE LEAD: the hook on a dirty guitar
// parents: HOOK
const lead = (g = .22) => hook().s('gm_distortion_guitar')
  .release(.3).lpf(4200).gain(g * 3).delay(".15:.25:.3").room(.25).pan(.55).orbit(2)

// ---------------- THE CLOUD: consciousness brought from without
// parents: none. It comes from outside and answers to nothing above it.
const cloud = (bars) => note("[d2,a2,d3,a3,d4,f#4,a4,d5]").s('sawtooth')
  .attack(2).release(2)
  .lpf(saw.slow(bars).range(400, 7000)).gain(saw.slow(bars).range(.02, .22))
  .room(.9).roomsize(8).orbit(5)

// ---------------- THE SHOP: kustarnichestvo
// parents: THE GROUP (rebuilt by hand)
const hammer = telegraph('IS NOT THIS THE CARPENTER', 'rim').gain(.5).room(.2).orbit(1)
const claps = s("~ cp ~ cp").bank('RolandTR909').gain(.45).room(.3).orbit(1)

// ---------------- THE ROUND: the little DAG
// parents: HOOK, THE SHOP. Each voice is the voice before it, a bar later.
const voice1 = () => lead(.22)
const voice2 = () => hook().late(1).transpose(-12).s('gm_drawbar_organ')
  .release(.3).gain(.12 * 3).pan(.3).room(.3).orbit(4)
const voice3 = () => hook().late(2).transpose(12).s('gm_celesta')
  .release(.6).gain(.14 * 3).pan(.7).room(.5).orbit(4)
const voice4 = () => hook().late(3).s('gm_choir_aahs')
  .attack(.05).release(.5).gain(.22 * 3).room(.6).roomsize(5).orbit(6)

// ---------------- THE LAMP AND THE LANTERN
// parents: QUESTION (the lamp holds its first chord), HOOK (the lantern walks it)
const lamp = note("[d4,a4,d5]").s('gm_drawbar_organ')
  .attack(1).release(2).gain(.06 * 3).room(.7).orbit(4)
const lantern = note(mini(HOOK)).slow(8).transpose(12).s('gm_celesta')
  .release(1).gain(.16 * 3).pan(sine.slow(8).range(.2, .8))
  .delay(".25:.375:.4").room(.7).roomsize(5).orbit(4)

// ---------------- VOICES
const vox = (p, g = 1.4) => s(p).hpf(150).lpf(8000).gain(g)
  .delay(".12:.25:.25").room(.2).orbit(3)

// ============================================================
// SECTIONS
// ============================================================

// PREFACE. "Men and brethren, what shall we do?" (Acts 2:37)
// parents: QUESTION
const secPREFACE = stack(
  arrange(
    [7, note(ARPEGGIO).s('gm_electric_guitar_clean')
      .release(.4).gain(.3 * 3).delay(".25:.25:.35").room(.4).orbit(2)],
    [1, note("[a2,e3,a3,c#4,e4]").s('gm_electric_guitar_clean')
      .release(1.6).gain(.3 * 3).room(.5).orbit(2)],
  ),
  vox("<what_is_to_be_done ~ ~ ~ men_and_brethren_what_shall_we_do ~ ~ ~>"),
)

// HANDS. "We are marching in a compact group ... firmly holding
// each other by the hand." The band comes in together, under the
// parent track: Viri Galilaei on the choir and WHAT HATH GOD WROUGHT
// on the rim, where the essay cites "Whether the Cloud Makes Many
// Worlds". Then the child's own hook.
// parents: THE GROUP, THE LEAD, PARENTS
const secHANDS = stack(
  group(VERSE, VERSE_ROOTS),
  viri().s('gm_choir_aahs').attack(.05).release(.6)
    .room(.6).roomsize(5).gain(.3 * 3).orbit(6).mask("<1!8 0!8>"),
  telegraph(PARENT_TALEA, 'rim').gain(.3).hpf(1500).pan(.65).orbit(1).mask("<1!8 0!8>"),
  lead().mask("<0!8 1!8>"),
)

// WITHOUT. "It would have to be brought to them from without."
// The cloud swells; the band is filtered away beneath it.
// parents: THE GROUP, THE CLOUD
const secWITHOUT = arrange(
  [7, stack(
    group(VERSE, VERSE_ROOTS)
      .lpf(saw.slow(7).range(3000, 180)).postgain(saw.slow(7).range(1, .15)),
    cloud(7),
    vox("<~ ~ brought_to_them_from_without ~ ~ ~ ~>"),
  )],
  [1, silence],
)

// SHOP. "Is not this the carpenter?" (Mark 6:3)
// The band rebuilt by hand, four bars at a time.
// parents: THE SHOP, THE GROUP
const secSHOP = stack(
  hammer,
  claps,
  bass(ROOTS).mask("<0!4 1!12>"),
  chug(QUESTION).mask("<0!8 1!8>"),
  stack(kick, snare, hats, fill).mask("<0!12 1!4>"),
  organ(QUESTION).mask("<0!12 1!4>"),
  vox("<is_not_this_the_carpenter ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~>"),
)

// ROUND. The little DAG: pass it round.
// parents: THE ROUND, THE GROUP (half-time)
const secROUND = stack(
  s("bd ~ ~ ~ ~ ~ ~ ~").bank('RolandTR909').gain(.85).orbit(1),
  s("~ ~ ~ ~ sd ~ ~ ~").bank('RolandTR909').gain(.6).room(.3).orbit(1),
  s("hh*4").bank('RolandTR909').gain(.18).hpf(6000).orbit(1),
  crash,
  bass(ROOTS).struct("x ~ ~ ~ x ~ ~ ~"),
  chug(QUESTION, .12).struct("x ~ ~ ~ ~ ~ ~ ~").clip(2),
  voice1(),
  voice2().mask("<0!4 1!12>"),
  voice3().mask("<0!8 1!8>"),
  voice4().mask("<0!12 1!4>"),
  vox("<pass_it_round ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~>"),
)

// LAMP. "Thy word is a lamp unto my feet, and a light unto my path."
// parents: THE LAMP AND THE LANTERN; a drum roll from THE GROUP
const secLAMP = stack(
  lamp,
  lantern,
  note("<d2 b1 g1 a1>").s('gm_electric_bass_pick').release(1).gain(.22 * 3).orbit(2),
  vox("<thy_word_is_a_lamp_unto_my_feet ~ ~ ~ ~ ~ ~ ~>", 1.2),
  s("<~ ~ ~ ~ ~ ~ sd*4 [sd*8, ~ ~ ~ ~ lt mt ht ht]>").bank('RolandTR909')
    .gain(saw.slow(2).range(.25, .6)).orbit(1),
)

// TABLE. "Breaking bread from house to house" (Acts 2:46).
// Everyone, and the snare taps the answer.
// parents: everything above but the cloud
const secTABLE = stack(
  group(QUESTION, ROOTS),
  lead(.24),
  telegraph('BREAK THE BREAD PASS IT ROUND', 'rim').gain(.4).hpf(800).pan(.35).orbit(1),
  voice4().mask("<0!8 1!16>"),
  voice3().mask("<0!16 1!8>"),
  vox("<break_the_bread ~ ~ ~ ~ ~ ~ ~ pass_it_round ~ ~ ~ ~ ~ ~ ~ give_us_a_table ~ ~ ~ ~ ~ ~ ~>"),
)

// END. Three hits, the chord rings, and the last line.
const STAB = "[d2,d3,a3,d4,f#4]"
const secEND = arrange(
  [1, stack(
    note(STAB).struct("x ~ ~ x ~ ~ x ~").s('gm_overdriven_guitar').clip(.9).gain(.25 * 3).orbit(2),
    note("d1").struct("x ~ ~ x ~ ~ x ~").s('gm_electric_bass_pick').gain(.3 * 3).orbit(2),
    s("[bd, cr] ~ ~ [bd, sd] ~ ~ [bd, sd] ~").bank('RolandTR909').gain(.8).orbit(1),
  )],
  [3, stack(
    stack(
      note(STAB).s('gm_overdriven_guitar').release(4).gain(.22 * 3).room(.6).roomsize(6).orbit(2),
      note("d2").s('gm_electric_bass_pick').release(3).gain(.25 * 3).orbit(2),
      s("cr").bank('RolandTR909').gain(.4).room(.5).orbit(1),
    ).slow(3),
    vox("<write_down_who_was_there ~ ~>", 1.5),
  )],
  [2, silence],
)

// ============================================================
// THE ARRANGEMENT
// ============================================================
arrange(
  [8,  secPREFACE],
  [16, secHANDS],
  [8,  secWITHOUT],
  [16, secSHOP],
  [16, secROUND],
  [8,  secLAMP],
  [24, secTABLE],
  [6,  secEND],
)
