"""Narration for Ranger v2: one WAV per line (Kokoro am_michael), plus a manifest of durations."""
import json
import os
import sys

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(W, "build/v2/vo")
os.makedirs(OUT, exist_ok=True)

LINES = {
    "hook_trail": "Far from any tower, a phone shows just one thing. No signal.",
    "hook_collapse": "When a building collapses, the person who needs help most can't call for it.",
    "reveal": "Meet Ranger. A pocket radio messenger that works with no towers, no sim card, and no internet.",
    "range": "Its long range LoRa radio reaches up to eight kilometers in open line of sight. "
             "At shorter range, it moves data at up to two hundred and two kilobits per second.",
    "mesh": "And every Ranger is also a relay. Messages hop from device to device, forming a mesh. "
            "Add more Rangers, and the network stretches far beyond the reach of any single radio. "
            "Every message is encrypted.",
    "f_people": "See everyone in range, at a glance.",
    "f_text": "Send texts to one person, or to everyone, with delivery confirmation.",
    "f_talk": "Hold VOICE to talk, like a walkie-talkie, but private.",
    "f_track": "Track a teammate. The arrow points the way, and shows the distance.",
    "f_ranging": "No GPS? Ranger measures distance using the radio signal itself.",
    "f_location": "Check your position, and share it in one press.",
    "f_sos": "In an emergency, one press sends an SOS with your location to every Ranger.",
    "f_sleep": "It sleeps to save power, and wakes the moment a message arrives.",
    "phones": "No Ranger? Join one with your phone over Wi-Fi. No app, and no mobile data. "
              "Your phone can even lend Ranger its GPS and clock.",
    "uc_desert": "In a remote desert, a patrol stays in contact across open ground, with nothing to rely on but each other.",
    "uc_rubble": "Under the rubble, a survivor's Ranger carries their voice to the rescue team above.",
    "uc_jungle": "Lost in the jungle, a hiker's message hops across the mesh until it reaches the search team.",
    "uc_trail": "And on the trail, friends always know where each other are.",
    "parts": "Inside: an ESP32, a LoRa radio, an OLED screen, a mic and speaker, GPS and a compass, and a three point seven volt, thousand milliamp hour lie-poh battery that can stay on standby for days.",
    "cost": "Built to scale, Ranger is expected to cost around three thousand rupees per unit in mass production.",
    "end": "Ranger. When the network goes down, you stay connected. Scan the code to see how it's built.",
}


def trim(x, sr, thr=0.008):
    idx = np.where(np.abs(x) > thr)[0]
    if not len(idx):
        return x
    a = max(0, idx[0] - int(0.03 * sr))
    b = min(len(x), idx[-1] + int(0.12 * sr))
    return x[a:b]


if __name__ == "__main__":
    k = Kokoro(sys.argv[1] + "/kokoro-v1.0.onnx", sys.argv[1] + "/voices-v1.0.bin")
    man = {}
    for key, text in LINES.items():
        s, sr = k.create(text, voice="am_michael", speed=1.15 if key == "parts" else 1.0, lang="en-us")
        s = trim(np.asarray(s, np.float32), sr)
        s = s / (np.max(np.abs(s)) + 1e-9) * 0.7
        path = os.path.join(OUT, f"vo_{key}.wav")
        sf.write(path, s, sr, subtype="PCM_16")
        man[key] = {"file": path, "dur": round(len(s) / sr, 3), "text": text}
        print(f"{key:14s} {len(s) / sr:6.2f}s")
    json.dump(man, open(os.path.join(OUT, "manifest.json"), "w"), indent=1)
