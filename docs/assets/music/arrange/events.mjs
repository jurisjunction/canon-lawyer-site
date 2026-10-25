// events.mjs: every event a track plays, as JSON, from Strudel's own engine, offline.
//
//   node arrange/events.mjs <track.strudel.js> <bars> > events.json
//
// One object per event with an onset: its start and end in bars, as exact fractions
// ("37/2"), and every control value it carries (s, note, n, gain, pan, lpf, ...).
// A note name is also given as a MIDI number (midi). Nothing is interpreted here:
// what layer an event belongs to is decided by organ_edition.py, from these values.
//
// It evaluates the track as checkers/strudel_play.mjs does (pinned @strudel/core
// 1.1.0, the ducking controls stubbed), and loads the modules from checkers/
// (cd checkers && npm install), or from the folder in $STRUDEL_MODULES.
import fs from 'node:fs'
import path from 'node:path'
import { createRequire } from 'node:module'
import { fileURLToPath } from 'node:url'

const here = path.dirname(fileURLToPath(import.meta.url))
const from = process.env.STRUDEL_MODULES || path.join(here, '..', 'checkers') + path.sep
const require = createRequire(from.endsWith(path.sep) ? from : from + path.sep)
const say = console.log
console.log = (...a) => console.error(...a)   // the engine greets on load; keep stdout for the JSON
const core = await import(require.resolve('@strudel/core'))
const mini = await import(require.resolve('@strudel/mini'))
const tonal = await import(require.resolve('@strudel/tonal'))
Object.assign(globalThis, core, mini, tonal)
mini.miniAllStrings()
globalThis.samples = () => {}
globalThis.setcpm = () => {}
for (const k of ['duckorbit', 'duckattack', 'duckdepth']) {
  if (!core.Pattern.prototype[k]) core.Pattern.prototype[k] = function () { return this }
}

const [file, bars] = [process.argv[2], +process.argv[3]]
if (!file || !(bars > 0)) {
  console.error('usage: node events.mjs <track.strudel.js> <bars>')
  process.exit(2)
}
let src = fs.readFileSync(file, 'utf8')
src = src.replace(/\narrange\(\n(\s*\[\d+,\s*sec)/, '\nreturn arrange(\n$1')
const pat = new Function(src)()

const frac = (f) => `${f.s * f.n}/${f.d}`
const out = []
for (let b = 0; b < bars; b++) {           // a bar at a time, so the order is the engine's
  for (const e of pat.queryArc(b, b + 1)) {
    if (!e.hasOnset()) continue
    const v = { ...e.value }
    if (v.note !== undefined) v.midi = typeof v.note === 'number' ? v.note : core.noteToMidi(v.note)
    out.push({ begin: frac(e.whole.begin), end: frac(e.whole.end), value: v })
  }
}
// a stable order: by onset, then sound, then pitch, then the rest of the values
const key = (x) => JSON.stringify([x.value.s ?? '', x.value.midi ?? -1, x.value])
const num = (s) => { const [n, d] = s.split('/').map(Number); return n / d }
out.sort((a, b) => num(a.begin) - num(b.begin) || (key(a) < key(b) ? -1 : key(a) > key(b) ? 1 : 0))
const sorted = (o) => Object.fromEntries(Object.keys(o).sort().map((k) => [k, o[k]]))
process.stdout.write('[\n' + out.map((x) => JSON.stringify({ begin: x.begin, end: x.end, value: sorted(x.value) })).join(',\n') + '\n]\n')
