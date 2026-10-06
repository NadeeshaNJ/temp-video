"""Ranger v3, the expo cut (1920x1080, 30 fps, 76 s): fast hook, reveal, how it works,
rapid features, use cases, how it's built, cost flash, QR end card. Reuses build.py helpers."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as b  # noqa: E402
from build import WHITE, MIST, MINT, RED, style  # noqa: E402

W = b.W
A1 = os.path.join(W, "build/assets")
V2 = os.path.join(W, "build/v2")
V3 = os.path.join(W, "build/v3")
END = 76.0

T1, T2, T3, T4, G1, G2, V1, G3, G4, G5, G6, VB, BG, SFX1, SFX2, VOICE, VO, MUSIC = range(18)
LANES = ["text"] * 4 + ["shape", "shape", "video", "shape", "shape", "shape", "shape", "video", "shape",
                        "audio", "audio", "audio", "audio", "audio"]
VOM = json.load(open(os.path.join(V3, "vo/manifest.json")))
PILL = "#D90E1210"
placed = []


def call(n, a):
    return b.call(n, a)


def apply(ops):
    return b.apply(ops)


def setup():
    call("new_project", {})
    call("set_project_setup", {"width": 1920, "height": 1080, "fps": 30})
    call("set_overlap", {"enabled": True})
    for ty in reversed(LANES):
        call("add_track", {"type": ty})
    tracks = call("inspect", {})["tracks"]
    for t in reversed(tracks[len(LANES):]):
        call("remove_track", {"track": t["i"]})
    got = [t["type"] for t in call("inspect", {})["tracks"]]
    assert got == LANES, got
    want = ["bg.png", "hero_front.png", "card_proto.png", "card_pcb.png", "qr_end.png", "oled_01.png",
            "oled_07.png", "oled_15.png", "oled_18.png", "oled_20.png", "oled_22.png", "oled_25.png",
            "phone_03.png", "foot_2.webm", "foot_3.webm", "foot_4.webm", "foot_6.webm", "foot_7.webm",
            "sfx_blip.wav", "sfx_pop.wav", "sfx_whoosh.wav", "sfx_chirp.wav"]
    files = [os.path.join(A1, f) for f in want]
    files += sorted(os.path.join(V2, "parts", f) for f in os.listdir(os.path.join(V2, "parts")) if f.startswith("part_"))
    for sub in ("clips", "vo", "audio"):
        d = os.path.join(V3, sub)
        files += sorted(os.path.join(d, f) for f in os.listdir(d) if f.endswith((".mp4", ".wav")))
    names = [os.path.basename(f) for f in files]
    assert len(names) == len(set(names)), "duplicate asset names"
    r = call("import_media", {"paths": files})
    assert not r.get("missing"), r.get("missing")
    print("imported", len(r["assets"]))


def vo(key, at):
    placed.append((at, key))
    cid = call("place_clip", {"asset": f"v3_{key}.wav", "at": at, "track": VO})["id"]
    apply([{"tool": "set_volume", "args": {"clip": cid, "value": 1.7}}])
    return at + VOM[key]["dur"]


def full(asset, t0, dur, push=1.06, fade=(0.0, 0.0)):
    box = (0, 0, 1920, 1080)
    c = b.place(asset, VB, t0, dur, box, fade=fade)
    apply(b.push(c, t0, t0 + dur, box, push))
    return c


def kicker(t0, t1, txt, lane=T4, box=(120, 64, 900, 46), red=False):
    b.text(lane, t0, t1, txt, box, style(26, 800, "#FFE8857D" if red else MINT, spacing=4, shadow=False, box_color=PILL),
           anim_in="fade", srt=False)


def headline(t0, t1, txt, box=(120, 130, 1200, 110), size=62, lane=T1, red=False):
    b.text(lane, t0, t1, txt, box, style(size, 900, box_color=RED if red else PILL), anim_in="pop")


# ---------------------------------------------------------------- scenes
def bg_music():
    b.place("bg.png", BG, 0, END)
    m = call("place_clip", {"asset": "music_v3.wav", "at": 0, "track": MUSIC})["id"]
    keys = [(0.0, 0.42), (4.4, 0.42), (4.5, 0.55), (5.8, 0.55), (6.0, 0.21), (70.6, 0.21), (71.0, 0.55)]
    apply([{"tool": "set_volume", "args": {"clip": m, "at": t, "value": v}} for t, v in keys])


def s_hook():
    for t0, clip, word, key in ((0.0, "c3_trail.mp4", "No signal.", "h1"), (1.5, "c3_collapse.mp4", "No network.", "h2"),
                                (3.0, "c3_rain.mp4", "No help?", "h3")):
        full(clip, t0, 1.5, 1.05)
        b.text(T1, t0 + 0.12, t0 + 1.5, word, (120, 110, 1100, 170), style(130, 900), anim_in="pop", anim_out=None)
        vo(key, t0 + 0.18)
        b.sfx("sfx_whoosh.wav", t0 + 1.25, lane=SFX2, vol=0.35)


def s_reveal():
    lb = (260, 70, 1400, 810.5)
    lg = b.place("oled_01.png", G3, 4.5, 1.5, lb, fade=(0.08, 0.15))
    apply(b.pop(lg, 4.5, lb, 0.9, 0.25) + b.push(lg, 4.75, 6.0, lb, 1.04))
    hb = (250, 30, 699.5, 1020)
    h = b.place("hero_front.png", G3, 6.0, 6.0, hb, fade=(0.15, 0.2))
    apply(b.pop(h, 6.0, hb, 0.92, 0.35) + b.push(h, 6.35, 12.0, hb, 1.05))
    vo("reveal", 6.05)
    b.text(T1, 6.15, 11.85, "Meet Ranger.", (1040, 320, 800, 150), style(118, 900), anim_in="pop")
    b.text(T2, 8.1, 11.85, "No towers · No SIM · No internet", (1046, 480, 800, 70), style(40, 700, MINT, spacing=0),
           anim_in="fade-up-char")


def s_how():
    full("c3_range.mp4", 12.0, 6.0, 1.04)
    kicker(12.15, 23.85, "HOW IT WORKS")
    headline(12.3, 15.0, "Device to device")
    headline(15.15, 17.9, "Up to 8 km", size=96, box=(120, 124, 1000, 140))
    vo("how", 12.2)
    for t in (12.4, 13.4, 14.4):
        b.sfx("sfx_chirp.wav", t, lane=SFX1, vol=0.3)
    full("c3_mesh.mp4", 18.0, 6.0, 1.04)
    headline(18.35, 21.0, "Every Ranger is a relay")
    headline(21.15, 23.85, "Fully encrypted")
    vo("mesh", 18.4)
    for t in (18.2, 18.55, 18.9, 19.25, 19.6, 19.95, 20.3):
        b.sfx("sfx_blip.wav", t, lane=SFX2, vol=0.25)


FEATS = [("foot_2.webm", "18", "Send texts", "f_text"), ("foot_3.webm", "22", "Push to talk", "f_talk"),
         ("foot_4.webm", "07", "Track your team", "f_track"), ("foot_6.webm", "15", "Share your location", "f_loc"),
         ("foot_7.webm", "20", "SOS to everyone", "f_sos"), ("phone_03.png", "25", "Join from your phone", "f_phone")]


def s_features(T0=24.0, step=3.0):
    fb = (150, 165, 600, 750)
    pb = (300, 70, 485.5, 920)
    ob = (830, 140, 960, 555.8)
    b.text(T2, T0 + 0.1, T0 + step * len(FEATS) - 0.1, "FEATURES", (884, 720, 900, 46),
           style(28, 800, MINT, spacing=4, shadow=False), anim_in="fade", srt=False)
    for i, (left, scr, cap, key) in enumerate(FEATS):
        t0 = T0 + step * i
        fin, fout = (0.12 if i == 0 else 0.0), (0.15 if i == len(FEATS) - 1 else 0.0)
        if left.endswith(".webm"):
            f = b.place(left, V1, t0, step, fb, fade=(fin, fout))
            apply(b.box_keys(f, t0, t0 + 0.3, (fb[0] - 40, fb[1], fb[2], fb[3]), fb, "settle"))
        else:
            f = b.place(left, G4, t0, step, pb, fade=(fin, fout))
            apply(b.pop(f, t0, pb, 0.92, 0.3))
        o = b.place(f"oled_{scr}.png", G3, t0, step, ob, fade=(fin, fout))
        apply(b.pop(o, t0, ob, 0.94, 0.2))
        b.sfx("sfx_blip.wav", t0, lane=SFX1, vol=0.45)
        sos = key == "f_sos"
        b.text(T1, t0 + 0.2, t0 + step - 0.05, cap, (884 if not sos else 902, 780, 920, 110),
               style(76, 900, box_color=RED) if sos else style(76, 900), anim_in="pop")
        vo(key, t0 + 0.25)


USES = [("c3_rubble.mp4", "Rescue teams", "u1", 2.5), ("c3_desert.mp4", "Remote patrols", "u2", 2.5),
        ("c3_jungle.mp4", "Lost hikers", "u3", 2.5), ("c3_trail_day.mp4", "Anyone, anywhere", "u4", 3.5)]


def s_uses(T0=42.0):
    kicker(T0 + 0.1, T0 + 10.9, "BUILT FOR")
    t = T0
    for clip, cap, key, d in USES:
        full(clip, t, d, 1.05)
        headline(t + 0.1, t + d - 0.05, cap, size=72, box=(120, 124, 1100, 120))
        vo(key, t + 0.15)
        b.sfx("sfx_whoosh.wav", t + d - 0.25, lane=SFX2, vol=0.3)
        t += d


def s_built(T0=53.0):
    pb1 = (442, 150, 1036, 638.6)
    c = b.place("card_proto.png", G3, T0, 2.12, pb1, fade=(0.12, 0.12))
    apply(b.pop(c, T0, pb1, 0.94, 0.25) + b.push(c, T0 + 0.25, T0 + 2.0, pb1, 1.04))
    pb2 = (560, 140, 800, 666)
    c = b.place("card_pcb.png", G4, T0 + 2.0, 2.0, pb2, fade=(0.0, 0.12))
    apply(b.pop(c, T0 + 2.0, pb2, 0.94, 0.25) + b.push(c, T0 + 2.25, T0 + 4.0, pb2, 1.04))
    b.text(T1, T0 + 0.15, T0 + 3.95, "Designed from scratch", (96, 850, 1728, 110), style(76, 900, align="center"),
           anim_in="pop")
    vo("built", T0 + 0.2)
    keys = ["esp32", "lora", "oled", "mic", "battery", "gps"]
    lanes = [G1, G2, G3, G4, G5, G6]
    cw, ch = 539.4, 434.8
    xs, ys = (95, 690, 1285), (110, 560)
    G0 = T0 + 4.0
    b.text(T4, G0 + 0.1, G0 + 6.1, "WHAT'S INSIDE", (96, 40, 1728, 46),
           style(28, 800, MINT, align="center", spacing=4, shadow=False), anim_in="fade", srt=False)
    for k, key in enumerate(keys):
        t0 = round(G0 + 0.1 + 0.3 * k, 3)
        box = (xs[k % 3], ys[k // 3], cw, ch)
        c = b.place(f"part_{key}.png", lanes[k], t0, round(G0 + 6.2 - t0, 3), box, fade=(0.12, 0.2))
        apply(b.pop(c, t0, box, 0.9, 0.25))
        b.sfx("sfx_pop.wav", t0, lane=SFX1 if k % 2 == 0 else SFX2, vol=0.3)


def s_cost(T0=63.2):
    hb = (150, 60, 658.4, 960)
    h = b.place("hero_front.png", G3, T0, 2.8, hb, fade=(0.12, 0.2))
    apply(b.pop(h, T0, hb, 0.94, 0.3) + b.push(h, T0 + 0.3, T0 + 2.8, hb, 1.04))
    b.text(T4, T0 + 0.15, T0 + 2.75, "MASS PRODUCED", (960, 300, 860, 46), style(28, 800, MINT, spacing=4, shadow=False),
           anim_in="fade", srt=False)
    b.text(T1, T0 + 0.2, T0 + 2.75, "≈ Rs. 3,000", (956, 350, 900, 190), style(150, 900), anim_in="pop")
    b.text(T2, T0 + 0.5, T0 + 2.75, "per unit (estimate)", (962, 545, 860, 60), style(42, 600, MIST, spacing=0),
           anim_in="fade")
    vo("cost", T0 + 0.2)
    b.sfx("sfx_pop.wav", T0 + 0.2, lane=SFX2, vol=0.5)


def s_end(T0=66.0):
    hb = (110, 20, 548.4, 800)
    h = b.place("hero_front.png", G3, T0, END - T0, hb, fade=(0.3, 0.6))
    apply(b.push(h, T0, END, hb, 1.04))
    lb = (680, 250, 560, 324.2)
    lg = b.place("oled_01.png", G4, T0 + 0.2, END - T0 - 0.2, lb, fade=(0.1, 0.6))
    apply(b.pop(lg, T0 + 0.2, lb, 0.94, 0.2))
    qb = (1290, 150, 546.8, 620)
    q = b.place("qr_end.png", G2, T0 + 0.4, END - T0 - 0.4, qb, fade=(0.2, 0.6))
    apply(b.pop(q, T0 + 0.4, qb, 0.9, 0.267))
    b.sfx("sfx_pop.wav", T0 + 0.4, lane=SFX1, vol=0.6)
    b.text(T1, T0 + 0.8, END, "Stay connected, anywhere.", (150, 830, 1100, 100), style(64, 900, valign="top"),
           anim_in="pop", anim_out=None)
    b.text(T2, T0 + 1.4, END, "nadeeshanj.dev/ranger   ·   hackster.io/nadeeshanj/ranger-421e83",
           (150, 950, 1200, 50), style(30, 600, MIST, spacing=0), anim_in="fade", anim_out=None)
    vo("end", T0 + 0.8)
    for t in call("inspect", {"clips": True})["tracks"]:
        for c in t.get("items", []):
            if t["i"] in (T1, T2) and abs(c["start"] + c["duration"] - END) < 0.05:
                apply([{"tool": "set_fade", "args": {"clip": c["id"], "out": 0.6}}])


def write_srt(path):
    def ts(s):
        ms = int(round(s * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    with open(path, "w") as fh:
        for i, (a, key) in enumerate(sorted(placed), 1):
            text = VOM[key]["text"].replace("sim card", "SIM card")
            fh.write(f"{i}\n{ts(a)} --> {ts(a + VOM[key]['dur'])}\n{text}\n\n")


if __name__ == "__main__":
    setup()
    for fn in (bg_music, s_hook, s_reveal, s_how, s_features, s_uses, s_built, s_cost, s_end):
        fn()
        print("built", fn.__name__, flush=True)
    write_srt(os.path.join(V3, "ranger_v3.srt"))
    print(call("save_project", {"path": os.path.join(V3, "ranger_v3.json")}))
    print(json.dumps({k: v for k, v in call("inspect", {}).items() if k in ("dur", "clips", "w", "h", "fps")}))
