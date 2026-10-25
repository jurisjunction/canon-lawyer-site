"""ascend.py: at the waters, the voice ascends.

The motet's first five lines are SAM's, a machine chanting (sam.mjs). When
the mantle falls, at "Where is the LORD God of Elijah?", the last four pass
to a small choir: SAM's line lends only the shape of its mouth (its spectral
envelope) to three voices of three singers each, singing the same reciting
tone an octave up in fauxbourdon, the chant on top with a fourth and a sixth
below, as the motet's waters sing it, in a long stone-church tail. The buzz
goes; the words stay, on breath and harmony.

This is a stand-in for people. When a person records the lines, their voice
goes in the middle and the choir stays around it; it is never used to make
anyone's voice say what they did not sing.

    python3 ascend.py [track]      (numpy and scipy; run node sam.mjs [track] first)

reads docs/assets/music/voices/<track>/sam/ and writes the lines that ascend
to docs/assets/music/voices/<track>/ascended/; the track is a-new-song unless
another is named. Each track sings in its own mode (below). Deterministic: the
choir's small detunings come from fixed seeds, so the same input gives the
same bytes.
"""
import sys
import json, wave
from pathlib import Path
import numpy as np
from scipy.signal import stft, istft, resample_poly, fftconvolve

SR_IN, SR = 22050, 44100
MODES = {                                            # final (pitch class) and steps
    "a-new-song": (7, [0, 2, 4, 5, 7, 9, 10]),       # G mixolydian, from G
    "on-these-two-hang": (4, [0, 1, 3, 5, 7, 8, 10]),  # E phrygian, mode III, from E
}
TRACK = sys.argv[1] if len(sys.argv) > 1 else "a-new-song"
FINAL, MIX = MODES[TRACK]
def degree(m):                                       # midi -> scale degree (the final = 0 at octave -1)
    for d in range(-30, 60):
        o, k = divmod(d, 7)
        if FINAL + 12 * o + MIX[k] == m:
            return d
    raise ValueError(m)
def midi_of(d):
    o, k = divmod(d, 7)
    return FINAL + 12 * o + MIX[k]
hz = lambda m: 440 * 2 ** ((m - 69) / 12)

def read(fn):
    w = wave.open(fn)
    return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16) / 32768

def carrier(n, segs, lift):
    """A choir in fauxbourdon over the line's pitches: three voices, three singers each."""
    t = np.arange(n) / SR
    out = np.zeros(n)
    rng = np.random.default_rng(7)                   # the same choir every time
    bounds = [s * 2 for s, _ in segs] + [n]
    for (start, m), end in zip(segs, bounds[1:]):
        a, b = start * 2, end
        for under in (0, -3, -5):
            f0 = hz(midi_of(degree(m + lift) + under))
            for singer in range(3):
                cents = rng.uniform(-9, 9)
                vib = 1 + (2 ** (14 / 1200) - 1) * np.sin(2 * np.pi * (5.2 + rng.uniform(-.4, .4)) * t[a:b] + rng.uniform(0, 6.28))
                f = f0 * 2 ** (cents / 1200) * vib
                ph = 2 * np.pi * np.cumsum(f) / SR + rng.uniform(0, 6.28)
                k = np.arange(1, int(9000 / f0))[:, None]
                saw = (np.sin(k * ph[None, :]) / k).sum(0)
                out[a:b] += saw * (1.0 if under == 0 else 0.7)
    # crossfade the joins a little so the chord moves like breath
    return out / np.abs(out).max() + 0.04 * rng.standard_normal(n)

def envelope(Z, keep=36):
    """Spectral envelope by cepstral liftering."""
    logm = np.log(np.abs(Z) + 1e-7)
    c = np.fft.irfft(logm, axis=0)
    c[keep:-keep] = 0
    return np.exp(np.fft.rfft(c, axis=0).real[: Z.shape[0]])

def ascend(x, segs, lift):
    x = resample_poly(x, 2, 1)
    car = carrier(len(x), segs, lift)
    nper = 2048
    _, _, M = stft(x, SR, nperseg=nper, noverlap=nper * 3 // 4)
    _, _, C = stft(car, SR, nperseg=nper, noverlap=nper * 3 // 4)
    gate = np.clip(np.abs(M).sum(0) / np.abs(M).sum(0).max() * 6, 0, 1)   # silence stays silence
    Y = C * envelope(M) / envelope(C) * gate
    _, y = istft(Y, SR, nperseg=nper, noverlap=nper * 3 // 4)
    y = y[: len(x)]
    # a stone church: a long, dark tail
    rng = np.random.default_rng(1)
    ir_t = np.arange(int(2.8 * SR)) / SR
    ir = rng.standard_normal(len(ir_t)) * np.exp(-ir_t / .55)
    ir = np.convolve(ir, np.ones(6) / 6, mode="same")
    wet = fftconvolve(y, ir)[: len(y) + int(2.0 * SR)]
    dry = np.concatenate([y, np.zeros(len(wet) - len(y))])
    out = dry / np.abs(dry).max() * .75 + wet / np.abs(wet).max() * .45
    fade = int(.6 * SR)
    out[-fade:] *= np.linspace(1, 0, fade)
    return out / np.abs(out).max() * .89

def write(fn, y):
    w = wave.open(fn, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()

VOICES = Path(__file__).parent / "docs" / "assets" / "music" / "voices" / TRACK
ASCENDS = {
    "a-new-song": ["where_is_the_lord_god_of_elijah", "the_spirit_of_elijah_doth_rest_on_elisha",
                   "things_new_and_old", "he_shall_turn_the_heart_of_the_fathers_to_the_children"],
    # the Lord's words, and the centurion's once the others join him
    "on-these-two-hang": ["thou_shalt_love_the_lord_thy_god_with_all_thy_heart", "the_second_is_like_unto_it",
                          "thou_shalt_love_thy_neighbour_as_thyself",
                          "on_these_two_commandments_hang_all_the_law_and_the_prophets",
                          "eli_eli_lama_sabachthani", "it_is_finished", "truly_this_was_the_son_of_god",
                          "if_ye_love_me_keep_my_commandments"],
}
ASCENDED = ASCENDS[TRACK]

if __name__ == "__main__":
    segs = json.load(open(VOICES / "sam" / "segments.json"))
    (VOICES / "ascended").mkdir(exist_ok=True)
    for name in ASCENDED:
        y = ascend(read(str(VOICES / "sam" / f"{name}.wav")), segs[name]["starts"], 12)
        write(str(VOICES / "ascended" / f"{name}.wav"), y)
        print(f"ascend.py: {name} ({segs[name]['voice']}), {len(y) / SR:.2f} s")
