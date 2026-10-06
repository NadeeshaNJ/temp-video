"""Narration for Ranger v3 (expo cut): short, energetic lines, Kokoro am_michael at 1.15x."""
import json
import os
import sys

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(W, "build/v3/vo")
os.makedirs(OUT, exist_ok=True)
SPEED = 1.15

LINES = {
    "h1": "No signal.",
    "h2": "No network.",
    "h3": "No way to call for help.",
    "reveal": "Meet Ranger! A pocket radio that keeps you connected. No towers, no sim card, no internet!",
    "how": "Rangers talk directly to each other over long range LoRa radio. Up to eight kilometers!",
    "mesh": "And every Ranger relays for the others, so the mesh keeps on growing. Fully encrypted!",
    "f_text": "Send texts!",
    "f_talk": "Push to talk!",
    "f_track": "Track your team!",
    "f_loc": "Share your location!",
    "f_sos": "Hit SOS to alert everyone!",
    "f_phone": "Even join from your phone. No app needed!",
    "u1": "Rescue teams!",
    "u2": "Remote patrols!",
    "u3": "Lost hikers!",
    "u4": "Anyone, anywhere the network can't reach!",
    "built": "Designed from scratch, on a custom PCB. With an ESP32, a LoRa radio, GPS, and a battery that lasts for days on standby.",
    "cost": "All for around three thousand rupees!",
    "end": "Ranger. Stay connected, anywhere. Scan the code to learn more!",
}


def trim(x, sr, thr=0.008):
    idx = np.where(np.abs(x) > thr)[0]
    if not len(idx):
        return x
    return x[max(0, idx[0] - int(0.02 * sr)):min(len(x), idx[-1] + int(0.08 * sr))]


if __name__ == "__main__":
    k = Kokoro(sys.argv[1] + "/kokoro-v1.0.onnx", sys.argv[1] + "/voices-v1.0.bin")
    man = {}
    for key, text in LINES.items():
        s, sr = k.create(text, voice="am_michael", speed=SPEED, lang="en-us")
        s = trim(np.asarray(s, np.float32), sr)
        s = s / (np.max(np.abs(s)) + 1e-9) * 0.7
        path = os.path.join(OUT, f"v3_{key}.wav")
        sf.write(path, s, sr, subtype="PCM_16")
        man[key] = {"file": path, "dur": round(len(s) / sr, 3), "text": text}
        print(f"{key:10s} {len(s) / sr:6.2f}s")
    json.dump(man, open(os.path.join(OUT, "manifest.json"), "w"), indent=1)
