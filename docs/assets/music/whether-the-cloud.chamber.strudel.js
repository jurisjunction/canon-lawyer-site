// WHETHER THE CLOUD MAKES MANY WORLDS
// A musical analogue to the disputation of the same name.
// For Strudel (https://strudel.cc). Paste this in and press play.
// About three minutes and twenty seconds. It gets very loud once, briefly.
//
// Dedicated to the public domain (CC0 1.0). The chant melodies are public
// domain; the pitches are taken from GregoBase transcriptions (CC0).
//
// The form is built from its end. The last thing you hear is the opening of
// the Ascension introit, "Viri Galilaei". The first thing you hear is that
// same phrase backwards, in fog: Machaut's "Ma fin est mon commencement".

setcpm(30) // one cycle = two seconds

// ---------- the sources ----------
// Durations in units: a syllable on one note takes 2, notes of a neume take 1,
// the end of a phrase takes more. "~" is a breath.

// "Viri Galilaei, quid admiramini" (Acts 1:11), introit for the Ascension, mode 7
const VIRI = 'g3@2 g3@2 g3 c4 b3 c4@2 d4 c4 e4 d4 d4@3'
// the same phrase, end first
const IRIV = 'd4@3 d4 e4 c4 d4 c4@2 b3 c4 g3 g3@2 g3@2'
// the answer, a fifth above
const ANSWER = 'd4@2 d4@2 d4 g4 f4 g4@2 a4 g4 b4 a4 a4@3'
// mode 7 recites on D: the tenor holds it while the answer sings
const TENOR = 'd4@12 c4@4'
// two voices above the bass entry
const ALTO = 'd4@2 d4@2 d4 e4 d4 c4@2 f4 g4 g4 a4 a4@3'
const TREBLE = 'b4@2 b4@2 b4 c5 d5 e5@2 d5 e5 g5 f5 f5@3'

// "Rorate caeli desuper, et nubes pluant justum" (Isaiah 45:8), Advent, mode 1
const RORATE = 'f3@2 g3 a3 a3@3 d4@2 c4@2 c4 bb3 a3@2 a3@2 g3@2 ~ ' +
               'a3@2 bb3@2 a3@2 g3 f3 e3@2 f3 e3 d3@3 ~@5'

// "Lumen Christi" / "Deo gratias", the Easter Vigil: do do do la, raised each time
const lumen = (doh, la) => doh + '@2 ' + doh + '@2 ' + doh + '@2 ' + la + '@3 ~'
const gratias = (doh, la) => doh + '@2 ' + doh + '@2 ' + doh + '@2 ' + la + '@2 ' + la + '@3 ~'

// ---------- the medium ----------
// The first message sent by electric telegraph, 24 May 1844 (Numbers 23:23).
// Dot 1 unit, dash 3; 1 between signs, 3 between letters, 7 between words.
const CODE = { W: '.--', H: '....', A: '.-', T: '-', G: '--.', O: '---', D: '-..', R: '.-.', U: '..-' }
const morse = (text) => text.split(' ').map((word) =>
  word.split('').map((ch) =>
    CODE[ch].split('').map((sign) => (sign === '.' ? 'x' : 'x@3')).join(' ~ ')
  ).join(' ~@3 ')
).join(' ~@7 ')
const TALEA = morse('WHAT HATH GOD WROUGHT') // 189 units, 50 strokes
const SPAN = 189 / 16 // one unit = a sixteenth of a cycle

// Isorhythm, the fourteenth century's own device: a rhythm (talea) carries a
// melody (color), one pitch per stroke. The medium given back its word.
const pitches = (phrase) => phrase.split(' ').filter((t) => t && t[0] !== '~').map((t) => t.split('@')[0])
const iso = (talea, color) => { let i = 0; return talea.replace(/x/g, () => color[i++ % color.length]) }
const telegraph = (pitch) => note(mini(iso(TALEA, [pitch]))).slow(SPAN)
const ringing = (phrase, up) => note(mini(iso(TALEA, pitches(phrase)))).transpose(up).slow(SPAN)

// a phrase sung over n cycles
const sing = (phrase, n) => note(mini(phrase)).slow(n)

// ---------- I. The cloud (12 cycles) ----------
// The ending, backwards, through fog. A telegraph somewhere far off.
const cloud = stack(
  arrange([8, sing(IRIV, 8)], [4, silence])
    .s('gm_voice_oohs').lpf(700).room(0.9).gain(0.35),
  s('pink').attack(0.8).release(0.8).lpf(600).gain(0.06),
  arrange([4, silence], [8, telegraph('a5')])
    .s('sine').hpf(1500).delay(0.5).delaytime(0.375).delayfeedback(0.5).room(0.8).gain(0.03),
  arrange([8, silence], [4, note("[g2,d3]")])
    .s('gm_church_organ').attack(2).gain(0.12),
)

// ---------- II. The hall (16 cycles) ----------
// A fugato on the introit: the subject over a drone, the answer over the held
// tenor, then the bass with two voices above it.
const hall = stack(
  arrange([4, note("[g2,d3]")], [12, silence]).s('gm_church_organ').gain(0.15),
  arrange([4, sing(VIRI, 4)], [4, sing(TENOR, 4)], [4, sing(ALTO, 4)], [4, sing('c5 b4', 4)])
    .s('gm_choir_aahs').room(0.6).gain(0.4),
  arrange([4, silence], [4, sing(ANSWER, 4)], [4, sing(TREBLE, 4)], [4, sing('e5 d5', 4)])
    .s('gm_choir_aahs').room(0.6).gain(0.32),
  arrange([8, silence], [4, sing(VIRI, 4).transpose(-12)], [4, sing('c3 g2', 4)])
    .s('gm_church_organ').gain(0.3),
  arrange([8, silence], [4, telegraph('a5').gain(0.05)], [4, telegraph('a5').gain(0.1)])
    .s('sine').room(0.3),
)

// ---------- III. The Voice (4 cycles) ----------
// No name. Fortissimo. Then nothing at all.
const voice = arrange(
  [2, stack(
    s('white').gain(0.6),
    s('crackle').density(0.6).gain(0.45),
    note("[g2,ab2,a2,bb2,b2,c3,db3]").s('sawtooth').distort(2).gain(0.1),
  )],
  [2, silence],
)

// ---------- IV. Horeb (12 cycles) ----------
// "But the LORD was not in the wind ... not in the earthquake ... not in the fire."
const horeb = arrange(
  [3, s('wind').n("<0 4 7>").gain(0.4).room(0.4)],
  [1, silence],
  [3, stack(s('brown').lpf(140).gain(0.4), note('g1').s('sawtooth').lpf(90).gain(0.3))],
  [1, silence],
  [3, s('crackle').density(0.25).hpf(800).gain(0.35)],
  [1, silence],
)

// ---------- V. A still small voice (12 cycles) ----------
// A pure tone, the thinnest medium there is. The people answer, three times,
// each time a step higher.
const still = stack(
  arrange(
    [2, sing(lumen('d4', 'b3'), 2)], [2, silence],
    [2, sing(lumen('e4', 'c#4'), 2)], [2, silence],
    [2, sing(lumen('f4', 'd4'), 2)], [2, silence],
  ).s('sine').attack(0.05).release(0.6).room(0.7).gain(0.22),
  arrange(
    [2, silence], [2, sing(gratias('d4', 'b3'), 2)],
    [2, silence], [2, sing(gratias('e4', 'c#4'), 2)],
    [2, silence], [2, sing(gratias('f4', 'd4'), 2)],
  ).s('gm_voice_oohs').room(0.7).gain(0.22),
)

// ---------- VI. A bright cloud (16 cycles) ----------
// "Drop down, ye heavens, and let the clouds rain down the Just One."
// The telegraph's rhythm now carries the chant.
const bright = stack(
  note("[d2,a2]").s('gm_church_organ').gain(0.14),
  sing(RORATE, 8).s('gm_choir_aahs').room(0.6).gain(0.38),
  arrange([4, silence], [12, ringing(RORATE, 24)])
    .s('gm_celesta').room(0.8).gain(0.18),
  note("[d4,a4]").s('gm_pad_halo').lpf(saw.range(500, 3000).slow(16)).gain(0.1),
)

// ---------- VII. Taken up (12 cycles) ----------
// "There appeared a chariot of fire ... and Elijah went up by a whirlwind."
// The introit rises an octave at each entry; the bells carry it on the telegraph.
const takenUp = stack(
  note("[g1,g2]").s('gm_church_organ').gain(0.18),
  arrange([4, sing(VIRI, 4).transpose(-12)], [8, note('d3')])
    .s('gm_church_organ').gain(0.28),
  arrange([4, silence], [4, sing(VIRI, 4)], [4, note('d4')])
    .s('gm_choir_aahs').room(0.6).gain(0.36),
  arrange([8, silence], [4, sing(VIRI, 4).transpose(12)])
    .s('gm_choir_aahs').room(0.6).gain(0.4),
  ringing(VIRI, 12).s('gm_tubular_bells').room(0.7).gain(0.16),
)

// ---------- VIII. My end is my beginning (16 cycles) ----------
// The opening phrase, forward and clear. Then the open fifth.
const end = stack(
  arrange([8, note("[g2,d3]")], [8, silence]).s('gm_church_organ').gain(0.12),
  arrange([8, sing(VIRI, 8)], [8, silence]).s('gm_voice_oohs').room(0.7).gain(0.38),
  arrange([8, silence], [8, note("[g2,d3,g3,d4]")])
    .s('gm_church_organ').gain("<0.3 0.27 0.24 0.2 0.16 0.12 0.08 0.04>"),
)

arrange(
  [12, cloud],
  [16, hall],
  [4, voice],
  [12, horeb],
  [12, still],
  [16, bright],
  [12, takenUp],
  [16, end],
)
