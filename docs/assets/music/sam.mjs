// sam.mjs: SAM chants the motet's lines, until people sing them.
//
// SAM, the Software Automatic Mouth (Don't Ask Software, 1982), in the
// JavaScript port sam-js. Its code is abandoned commercial software whose
// rights holder could not be reached (see the port's README); nothing of it
// is kept here, only the recordings it makes.
//
// Each line is a reading chanted on a reciting tone in the motet's mode,
// G mixolydian: recited in one breath on D, then the cadence a syllable at a
// time, falling through C to B; the question rises back to D, and the last
// line falls home to G. The women's lines are an octave up. The words are
// written in SAM's own phonetic alphabet, because its text reader mangles
// the prophets' names (it says EHLIHJAE).
//
//   npm i --no-save sam-js@0.3.1 && node sam.mjs [track]
//
// writes voices/<track>/sam/<line>.wav beside this file, and segments.json,
// where each line's pitches begin, for ascend.py. The track is a-new-song
// unless another is named; each track keeps its own lines and mode below.
import SamJs from 'sam-js'
import fs from 'node:fs'
import { fileURLToPath } from 'node:url'
const SR = 22050, K = 6805
const HZ = (m) => 440 * 2 ** ((m - 69) / 12)
const N = { E2: 40, F2: 41, G2: 43, A2: 45, B2: 47, C3: 48, D3: 50, E3: 52, F3: 53, G3: 55, A3: 57, B3: 59, C4: 60, D4: 62, E4: 64 }
const VOICE = {
  m: { mouth: 128, throat: 128, oct: 0 },   // SAM himself
  f: { mouth: 150, throat: 140, oct: 12 },  // brighter, an octave up
}
const NEW_SONG = {
  // name: [voice, recitation, [[syllable, note, speed], ...]]
  o_sing_unto_the_lord_a_new_song: ['f', 'OW SIHNX AHNTUW DHAX LAORD AX', [['NUW', 'C3', 96], ['SAOAONX', 'B2', 130]]],
  the_singer_himself_is_the_praise: ['f', 'DHAX SIHNXER /HIHMSEHLF IHZ', [['DHAX', 'C3', 90], ['PREYEYZ', 'B2', 130]]],
  the_spirit_of_elijah_doth_rest_on_elisha: ['f', 'DHAX SPIHRIHT AHV IHLAYJAH DAHTH REHST AAN IH', [['LAY', 'C3', 96], ['SHAXAXAX', 'B2', 140]]],
  things_new_and_old: ['f', 'THIHNXZ NUW', [['AEND', 'C3', 96], ['OWOWLD', 'B2', 140]]],
  bring_me_a_minstrel: ['m', 'BRIHNX MIY AX', [['MIHN', 'C3', 96], ['STREHEHL', 'B2', 130]]],
  let_a_double_portion_of_thy_spirit_be_upon_me: ['m', 'LEHT AX DAHBUL PAORSHUN AHV DHAY SPIHRIHT BIY AX', [['PAAN', 'C3', 96], ['MIYIY', 'B2', 130]]],
  a_new_man_knows_a_new_song: ['m', 'AX NUW MAEN NOWZ AX', [['NUW', 'C3', 96], ['SAOAONX', 'B2', 130]]],
  where_is_the_lord_god_of_elijah: ['m', 'WHEHR IHZ DHAX LAORD GAAD AHV IH', [['LAY', 'C3', 96], ['JAHAHAH', 'D3', 140]]],
  he_shall_turn_the_heart_of_the_fathers_to_the_children: ['m', '/HIY SHAEL TERN DHAX /HAART AHV DHAX FAADHERZ TUW DHAX', [['CHIHL', 'B2', 100], ['DREHEHN', 'G2', 150]]],
}
const SPEED = 82

// On These Two Hang: mode III, E phrygian. The reciting tone is C, the
// mode's own tenor; a statement falls through B to A, the Lord's words come
// home to E, the mode's final, and the questions rise.
const TWO_HANG = {
  master_which_is_the_great_commandment_in_the_law: ['m', 'MAESTER WIHCH IHZ DHAX GREYT KAXMAEND', [['MEHNT', 'B2', 96], ['IHN DHAX', 'B2', 110], ['LAOAO', 'D3', 140]]],
  thou_shalt_love_the_lord_thy_god_with_all_thy_heart: ['m', 'DHAW SHAELT LAHV DHAX LAORD DHAY GAAD WIHDH AOL DHAY', [['/HAA', 'F2', 100], ['AART', 'E2', 150]]],
  the_second_is_like_unto_it: ['m', 'AEND DHAX SEHKAHND IHZ LAYK AHN', [['TUW', 'B2', 96], ['IHIHT', 'A2', 140]]],
  thou_shalt_love_thy_neighbour_as_thyself: ['m', 'DHAW SHAELT LAHV DHAY NEYBER AEZ', [['DHAY', 'F2', 100], ['SEHEHLF', 'E2', 150]]],
  on_these_two_commandments_hang_all_the_law_and_the_prophets: ['m', 'AAN DHIYZ TUW KAXMAENDMEHNTS /HAENX AOL DHAX LAO AEND DHAX', [['PRAA', 'B2', 96], ['FEHEHTS', 'A2', 140]]],
  eli_eli_lama_sabachthani: ['m', 'IYLAY IYLAY LAAMAA SAABAAK', [['TAA', 'F2', 110], ['NIYIY', 'E2', 160]]],
  this_man_calleth_for_elias: ['f', 'DHIHS MAEN KAOLEHTH FAOR IH', [['LAY', 'D3', 96], ['AXAXS', 'E3', 140]]],
  it_is_finished: ['m', 'IHT IHZ', [['FIHN', 'F2', 110], ['IHSHT', 'E2', 150]]],
  truly_this_was_the_son_of_god: ['m', 'TRUWLIY DHIHS WAAZ DHAX SAHN AHV', [['GAAAAD', 'E2', 160]]],
  truly_this_was_the_son_of_god_f: ['f', 'TRUWLIY DHIHS WAAZ DHAX SAHN AHV', [['GAAAAD', 'E2', 160]]],
  if_ye_love_me_keep_my_commandments: ['m', 'IHF YIY LAHV MIY KIYP MAY', [['KAXMAEND', 'F2', 100], ['MEHNTS', 'E2', 150]]],
}

const TRACKS = {
  'a-new-song': { lines: NEW_SONG, recite: 'D3' },
  'on-these-two-hang': { lines: TWO_HANG, recite: 'C3' },
}
const TRACK = process.argv[2] || 'a-new-song'
const { lines: LINES, recite: RECITE } = TRACKS[TRACK]

const render = (ph, midi, speed, v) => {
  const f = HZ(midi), p = Math.max(8, Math.round(K / f))
  const x = new SamJs({ pitch: p, speed, mouth: v.mouth, throat: v.throat, singmode: true }).buf32(ph, true)
  const r = f / (K / p)                       // the last few cents
  const y = new Float32Array(Math.floor(x.length / r))
  for (let i = 0; i < y.length; i++) { const t = i * r, j = Math.floor(t), a = t - j; y[i] = (x[j] ?? 0) * (1 - a) + (x[j + 1] ?? 0) * a }
  return trim(y)
}
const trim = (y) => {
  const c = y.reduce((s, v) => s + v, 0) / y.length, z = y.map((v) => v - c)
  const th = 0.02 * Math.max(...z.map(Math.abs))
  let a = 0, b = z.length - 1
  while (a < b && Math.abs(z[a]) < th) a++
  while (b > a && Math.abs(z[b]) < th) b--
  return z.subarray(Math.max(0, a - 80), Math.min(z.length, b + 80))
}
const join = (parts, fade = 176) => {   // 8 ms crossfades
  const len = parts.reduce((s, p) => s + p.length, 0) - fade * (parts.length - 1)
  const out = new Float32Array(len); let at = 0
  parts.forEach((p, k) => {
    for (let i = 0; i < p.length; i++) {
      let g = 1
      if (k > 0 && i < fade) g = i / fade
      if (k < parts.length - 1 && i >= p.length - fade) g = (p.length - i) / fade
      out[at + i] += p[i] * g
    }
    at += p.length - fade
  })
  const peak = Math.max(...out.map(Math.abs))
  return out.map((v) => v / peak * 0.89)
}
const wav = (x) => {
  const b = Buffer.alloc(44 + x.length * 2)
  b.write('RIFF', 0); b.writeUInt32LE(36 + x.length * 2, 4); b.write('WAVEfmt ', 8); b.writeUInt32LE(16, 16)
  b.writeUInt16LE(1, 20); b.writeUInt16LE(1, 22); b.writeUInt32LE(SR, 24); b.writeUInt32LE(SR * 2, 28); b.writeUInt16LE(2, 32); b.writeUInt16LE(16, 34)
  b.write('data', 36); b.writeUInt32LE(x.length * 2, 40)
  x.forEach((v, i) => b.writeInt16LE(Math.round(Math.max(-1, Math.min(1, v)) * 32767), 44 + i * 2))
  return b
}
const outDir = process.argv[3] || fileURLToPath(new URL(`./voices/${TRACK}/sam`, import.meta.url)); fs.mkdirSync(outDir, { recursive: true })
const segments = {}
const report = {}
for (const [name, [vk, rec, cad]] of Object.entries(LINES)) {
  const v = VOICE[vk]
  const parts = [render(rec, N[RECITE] + v.oct, SPEED, v), ...cad.map(([syl, note, sp]) => render(syl, N[note] + v.oct, sp, v))]
  const x = join(parts)
  { let at = 0; segments[name] = { voice: vk, starts: parts.map((p, k) => { const s = [at, [N[RECITE], ...cad.map((c) => N[c[1]])][k] + v.oct]; at += p.length - 176; return s }) } }
  fs.writeFileSync(`${outDir}/${name}.wav`, wav(x))
  report[name] = { voice: vk, seconds: +(x.length / SR).toFixed(2), notes: [RECITE, ...cad.map((c) => c[1])].map((n) => n.replace(/\d/, (d) => String(+d + v.oct / 12))) }
}
fs.writeFileSync(`${outDir}/segments.json`, JSON.stringify(segments, null, 1) + '\n')
console.log(JSON.stringify(report, null, 1))
