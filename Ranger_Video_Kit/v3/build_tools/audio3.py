"""Energetic score for the Ranger v3 expo cut (120 BPM, bars on the 2 s grid)."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("AUDIO_OUT", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "build/v3/audio"))
import audio2 as au  # noqa: E402
from audio2 import SR, t_axis, saw, lowpass, highpass, reverb, env_adsr, midi, kick, hat, pluck  # noqa: E402

rng = np.random.default_rng(9)


def clap():
    t = t_axis(0.22)
    n = rng.normal(0, 1, len(t))
    env = np.exp(-t * 28)
    for d in (0.0, 0.011, 0.022):
        env = np.maximum(env, (t >= d) * np.exp(-np.clip(t - d, 0, None) * 120))
    return highpass(lowpass(n, 5000), 900) * env


def score(total, BUILD, GROOVE, FULL, OUT_T):
    n = int(total * SR)
    mix = {k: np.zeros(n) for k in ("pad", "bass", "drums", "arp", "fx")}

    def add(track, x, at, gain=1.0):
        i = int(at * SR)
        j = min(n, i + len(x))
        if j > i:
            mix[track][i:j] += x[: j - i] * gain

    beat = 0.5
    prog = [(57, [57, 60, 64]), (53, [53, 57, 60]), (48, [55, 60, 64]), (55, [55, 59, 62])]
    # build: accelerating kicks + riser + filtered pad
    k = 0
    s = 0.0
    while s < BUILD - 0.01:
        add("drums", kick(), s, 0.4 + 0.5 * s / BUILD)
        s += beat if s < BUILD - 2 else beat / 2
        k += 1
    t = t_axis(BUILD)
    rf = 300 * (1 + 14 * (t / BUILD) ** 2)
    rs = np.sin(2 * np.pi * np.cumsum(rf) / SR) * 0.3 + highpass(rng.normal(0, 1, len(t)), 2500) * 0.6
    add("fx", rs * (t / BUILD) ** 2, 0, 0.55)
    x = sum(saw(midi(nn), t, (0, 0.006, -0.005)) for nn in (45, 57, 60, 64))
    add("pad", lowpass(x, 700) * env_adsr(len(t), 0.5, 0.05), 0, 0.2)
    # impact
    tt = t_axis(2.5)
    boom = np.sin(2 * np.pi * np.cumsum(40 + 70 * np.exp(-tt * 7)) / SR) * np.exp(-tt * 2.0)
    add("fx", boom + lowpass(rng.normal(0, 1, len(tt)), 600) * np.exp(-tt * 5) * 0.7, BUILD, 1.0)
    # groove
    s = GROOVE
    while s < OUT_T - 1e-6:
        root, ch = prog[int((s - GROOVE) // 2) % 4]
        full = s >= FULL
        tt = t_axis(2.0)
        x = sum(saw(midi(nn), tt, (0, 0.006, -0.005)) for nn in ch)
        pump = np.ones(len(tt))
        for q in range(4):
            i0 = int(q * beat * SR)
            seg = np.linspace(0.35, 1.0, int(0.22 * SR))
            pump[i0:i0 + len(seg)] = np.minimum(pump[i0:i0 + len(seg)], seg)
        add("pad", lowpass(x, 2200 if full else 1300) * pump, s, 0.2)
        for q in range(4):
            bs = s + q * beat
            add("drums", kick(), bs, 1.0)
            if full and q in (1, 3):
                add("drums", clap(), bs, 0.55)
            for h in range(4 if full else 2):
                add("drums", hat(), bs + (h + 0.5) * beat / (4 if full else 2) - (beat / 8 if full else 0), 0.22 if h % 2 else 0.32)
            for e in range(2):
                bt = t_axis(beat * 0.45)
                bx = lowpass(saw(midi(root - 12), bt, (0, 0.003)), 450) * env_adsr(len(bt), 0.004, 0.05)
                add("bass", bx, bs + e * beat / 2, 0.8)
        if full:
            for q in range(16):
                nn = ch[[0, 1, 2, 1][q % 4]] + (24 if q % 8 >= 4 else 12)
                add("arp", pluck(midi(nn), 0.2), s + q * beat / 4, 0.2)
        s += 2.0
    # whoosh-up into the end hit
    tt = t_axis(1.0)
    add("fx", highpass(rng.normal(0, 1, len(tt)), 3000) * (tt / 1.0) ** 2, OUT_T - 1.0, 0.4)
    tt = t_axis(2.5)
    boom = np.sin(2 * np.pi * np.cumsum(40 + 70 * np.exp(-tt * 7)) / SR) * np.exp(-tt * 2.0)
    add("fx", boom, OUT_T, 0.8)
    # outro chord
    tt = t_axis(total - OUT_T)
    x = sum(saw(midi(nn), tt, (0, 0.006, -0.005)) for nn in (48, 55, 60, 64, 67, 72))
    add("pad", lowpass(x, 2400) * env_adsr(len(tt), 0.02, max(0.5, total - OUT_T - 1.0)), OUT_T, 0.3)
    for q in range(8):
        add("arp", pluck(midi([72, 76, 79, 84, 79, 76, 84, 88][q]), 0.5), OUT_T + q * 0.25, 0.25 * (1 - q / 10))
    pad = reverb(mix["pad"], 2.0, 0.3)
    arp = reverb(mix["arp"], 1.4, 0.28)
    fx = reverb(mix["fx"], 1.8, 0.2)
    L = pad + mix["bass"] + mix["drums"] + arp + fx
    R = pad + mix["bass"] + mix["drums"] + np.roll(arp, int(0.011 * SR)) + fx
    fade = np.ones(n)
    fn = int(2.0 * SR)
    fade[-fn:] = np.linspace(1, 0, fn) ** 1.5
    out = np.stack([L * fade, R * fade], 1)
    out = np.tanh(out / (np.max(np.abs(out)) * 0.75))
    au.save("music_v3.wav", out)


if __name__ == "__main__":
    os.makedirs(au.A, exist_ok=True)
    score(total=float(sys.argv[1]), BUILD=4.5, GROOVE=4.5, FULL=12.0, OUT_T=float(sys.argv[2]))
