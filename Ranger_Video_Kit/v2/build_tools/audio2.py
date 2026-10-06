"""Synthesised score (120 BPM, bars on the 2 s edit grid) and UI sound effects."""
import os
import wave
import numpy as np

W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.environ.get("AUDIO_OUT", os.path.join(W, "build/assets"))
SR = 44100
rng = np.random.default_rng(3)


def save(name, x):
    x = np.asarray(x, np.float64)
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    peak = np.max(np.abs(x)) or 1
    x = x / peak * 0.89
    with wave.open(f"{A}/{name}", "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())


def t_axis(sec):
    return np.arange(int(sec * SR)) / SR


def onepole(x, cutoff):
    a = np.exp(-2 * np.pi * np.asarray(cutoff) / SR)
    y = np.empty_like(x)
    acc = 0.0
    if np.ndim(a) == 0:
        b = 1 - a
        # vectorised via lfilter-like recursion in chunks
        for i in range(len(x)):
            acc = b * x[i] + a * acc
            y[i] = acc
    else:
        for i in range(len(x)):
            acc = (1 - a[i]) * x[i] + a[i] * acc
            y[i] = acc
    return y


def lowpass(x, cutoff):
    """Cheap FFT brick-ish lowpass with a soft knee."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (f / cutoff) ** 4)
    return np.fft.irfft(X, len(x))


def highpass(x, cutoff):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 - 1 / (1 + (f / cutoff) ** 4)
    return np.fft.irfft(X, len(x))


def reverb(x, secs=2.2, mix=0.3):
    n = int(secs * SR)
    ir = rng.normal(0, 1, n) * np.exp(-np.arange(n) / SR * 3.2)
    ir = lowpass(ir, 5000)
    ir /= np.sqrt(np.sum(ir ** 2))
    L = len(x) + n
    nfft = 1 << (L - 1).bit_length()
    y = np.fft.irfft(np.fft.rfft(x, nfft) * np.fft.rfft(ir, nfft), nfft)[:len(x)]
    return x * (1 - mix) + y * mix * 1.5


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def saw(freq, t, detune=(0.0,)):
    out = np.zeros_like(t)
    for d in detune:
        ph = (freq * (1 + d) * t) % 1.0
        out += 2 * ph - 1
    return out / len(detune)


def env_adsr(n, a, r):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    if na:
        e[:na] = np.linspace(0, 1, na)
    if nr:
        e[-nr:] *= np.linspace(1, 0, nr)
    return e


def kick():
    t = t_axis(0.45)
    f = 45 + 95 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 7.5) + 0.15 * rng.normal(0, 1, len(t)) * np.exp(-t * 180)


def hat():
    t = t_axis(0.08)
    return highpass(rng.normal(0, 1, len(t)), 7000) * np.exp(-t * 60)


def pluck(freq, dur=0.32):
    t = t_axis(dur)
    x = saw(freq, t, (0, 0.004)) * np.exp(-t * 11)
    return lowpass(x, 3200)


def score(total=190.0, HOOK=18.0, IMPACT=22.5, GROOVE=32.0, END=179.0, LIGHT=(-1, -1)):
    n = int(total * SR)
    mix = {k: np.zeros(n) for k in ("pad", "bass", "drums", "arp", "fx")}

    def add(track, x, at, gain=1.0):
        i = int(at * SR)
        j = min(n, i + len(x))
        if j > i:
            mix[track][i:j] += x[: j - i] * gain

    # progression Am F C G, one chord per 2 s bar (MIDI roots)
    prog = [(57, [57, 60, 64]), (53, [53, 57, 60]), (48, [55, 60, 64]), (55, [55, 59, 62])]
    beat = 0.5

    # -- hook 0-10: drone + sparse sub
    t = t_axis(HOOK + 0.5)
    drone = (saw(midi(33), t, (0, 0.003, -0.004)) * 0.6 + np.sin(2 * np.pi * midi(45) * t) * 0.3)
    drone = lowpass(drone, 260) * env_adsr(len(t), 2.5, 1.5)
    add("pad", drone, 0, 0.9)
    add("fx", lowpass(rng.normal(0, 1, len(t)), 900) * env_adsr(len(t), 3, 2), 0, 0.12)
    for s in np.arange(2.0, HOOK, 4.0):
        add("drums", kick(), float(s), 0.45)

    # -- build 10-15.5: pulse + riser
    BL = IMPACT - HOOK
    for k in range(int(BL / beat)):
        s = HOOK + k * beat
        add("drums", kick(), s, 0.35 + 0.4 * k / 11)
    t = t_axis(BL)
    riser_f = 300 * (1 + 12 * (t / BL) ** 2)
    rs = np.sin(2 * np.pi * np.cumsum(riser_f) / SR) * 0.25 + highpass(rng.normal(0, 1, len(t)), 2000) * 0.5
    add("fx", rs * (t / BL) ** 2, HOOK, 0.5)
    for b in range(int(BL // 2)):
        root, ch = prog[b % 4]
        tt = t_axis(2.0)
        x = sum(saw(midi(nn), tt, (0, 0.006, -0.005)) for nn in ch)
        add("pad", lowpass(x, 900 + 600 * b) * env_adsr(len(tt), 0.3, 0.3), HOOK + 2 * b, 0.25)

    # -- reveal impact at 15.5, sparse until 20
    tt = t_axis(3.0)
    boom = np.sin(2 * np.pi * np.cumsum(38 + 60 * np.exp(-tt * 6)) / SR) * np.exp(-tt * 1.6)
    add("fx", boom + lowpass(rng.normal(0, 1, len(tt)), 400) * np.exp(-tt * 4) * 0.6, IMPACT, 1.0)
    tt = t_axis(GROOVE - IMPACT + 0.1)
    x = sum(saw(midi(nn), tt, (0, 0.006, -0.005)) for nn in (57, 60, 64, 69))
    add("pad", lowpass(x, 1400) * env_adsr(len(tt), 1.0, 1.2), IMPACT + 0.1, 0.22)

    # -- groove 20-120
    def bar_at(s):
        return prog[int((s - GROOVE) // 2) % 4]

    s = GROOVE
    while s < END - 1e-6:
        root, ch = bar_at(s)
        light = LIGHT[0] <= s < LIGHT[1]
        tt = t_axis(2.0)
        x = sum(saw(midi(nn), tt, (0, 0.006, -0.005)) for nn in ch)
        add("pad", lowpass(x, 1600) * env_adsr(len(tt), 0.05, 0.05), s, 0.18)
        for k in range(4):
            bs = s + k * beat
            if not light or k % 2 == 0:
                add("drums", kick(), bs, 0.9)
            add("drums", hat(), bs + beat / 2, 0.35)
            bt = t_axis(beat * 0.9)
            bx = lowpass(saw(midi(root - 12), bt, (0, 0.003)), 380) * env_adsr(len(bt), 0.005, 0.08)
            add("bass", bx, bs, 0.75)
        if s >= GROOVE + 12:
            for k in range(8):
                nn = ch[[0, 1, 2, 1, 0, 2, 1, 2][k]] + 12
                add("arp", pluck(midi(nn)), s + k * beat / 2, 0.30 if not light else 0.22)
        s += 2.0

    # -- warm ending 120-130: C major, swell then fade
    tt = t_axis(total - END)
    x = sum(saw(midi(nn), tt, (0, 0.006, -0.005)) for nn in (48, 55, 60, 64, 67))
    end = lowpass(x, 1800) * env_adsr(len(tt), 0.4, 6.0)
    add("pad", end, END, 0.28)
    for k in range(10):
        add("arp", pluck(midi([72, 76, 79, 84, 79, 76, 72, 67, 72, 76][k]), 0.6), END + k * 0.5, 0.25 * (1 - k / 12))
    tt = t_axis(2.5)
    add("bass", lowpass(saw(midi(36), tt, (0, 0.003)), 300) * env_adsr(len(tt), 0.01, 2.0), END, 0.7)

    pad = reverb(mix["pad"], 2.6, 0.35)
    arp = reverb(mix["arp"], 1.8, 0.3)
    fx = reverb(mix["fx"], 2.0, 0.25)
    L = pad * 1.0 + mix["bass"] + mix["drums"] + arp * 0.9 + fx
    R = pad * 1.0 + mix["bass"] + mix["drums"] + np.roll(arp, int(0.012 * SR)) * 0.9 + fx
    # final fade
    fade = np.ones(n)
    fn = int(3.0 * SR)
    fade[-fn:] = np.linspace(1, 0, fn) ** 1.5
    out = np.stack([L * fade, R * fade], 1)
    out = np.tanh(out / (np.max(np.abs(out)) * 0.8))
    save("music.wav", out)


def sfx():
    t = t_axis(0.12)
    blip = (np.sin(2 * np.pi * 1760 * t) + 0.4 * np.sin(2 * np.pi * 2640 * t)) * np.exp(-t * 45)
    blip[: int(0.002 * SR)] *= np.linspace(0, 1, int(0.002 * SR))
    save("sfx_blip.wav", blip)
    t = t_axis(0.7)
    f = 900 + 1700 * np.clip(t / 0.18, 0, 1)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-np.clip(t - 0.12, 0, None) * 25) * (t < 0.3)
    noise = highpass(lowpass(rng.normal(0, 1, len(t)), 4000), 600) * np.sin(np.pi * np.clip(t / 0.7, 0, 1)) ** 2
    save("sfx_chirp.wav", tone * 0.5 + noise * 0.35)
    t = t_axis(0.25)
    pop = np.sin(2 * np.pi * np.cumsum(500 + 700 * np.exp(-t * 30)) / SR) * np.exp(-t * 22)
    save("sfx_pop.wav", pop)
    t = t_axis(0.6)
    sw = highpass(lowpass(rng.normal(0, 1, len(t)), 3000), 300) * np.sin(np.pi * t / 0.6) ** 3
    save("sfx_whoosh.wav", sw)


if __name__ == "__main__":
    if os.environ.get("V2"):
        score()
    else:
        sfx()
        score(130.0, 10.0, 15.5, 20.0, 120.0, (80, 104))
