"""Ranger v2 (1920x1080, 30 fps, 190 s): illustrated stories, range + mesh, features, phones,
use cases, components, cost, narration. Reuses the v1 helpers in build.py."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as b  # noqa: E402
from build import WHITE, MIST, MINT, RED, style, scaled  # noqa: E402

W = b.W
A1 = os.path.join(W, "build/assets")
V2 = os.path.join(W, "build/v2")
KIT = b.KIT
END = 190.0

T1, T2, T3, T4, G1, G2, V1, G3, G4, G5, G6, VB, BG, SFX1, SFX2, VOICE, VO, MUSIC = range(18)
LANES = ["text"] * 4 + ["shape", "shape", "video", "shape", "shape", "shape", "shape", "video", "shape",
                        "audio", "audio", "audio", "audio", "audio"]
VOM = json.load(open(os.path.join(V2, "vo/manifest.json")))
PILL = "#D90E1210"


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
    files = sorted(os.path.join(A1, f) for f in os.listdir(A1)
                   if f.endswith((".png", ".mp4", ".webm", ".wav")) and not f.startswith("mask") and f != "music.wav")
    for sub in ("scenes", "parts", "vo", "audio"):
        d = os.path.join(V2, sub)
        files += sorted(os.path.join(d, f) for f in os.listdir(d) if f.endswith((".png", ".mp4", ".wav"))
                        and not f.startswith("preview"))
    files.append(f"{KIT}/audio/ranger_startup_voice_8khz.wav")
    names = [os.path.basename(f) for f in files]
    assert len(names) == len(set(names)), "duplicate asset names"
    r = call("import_media", {"paths": files})
    assert not r.get("missing"), r.get("missing")
    print("imported", len(r["assets"]))


def vo(key, at):
    cid = call("place_clip", {"asset": f"vo_{key}.wav", "at": at, "track": VO})["id"]
    apply([{"tool": "set_volume", "args": {"clip": cid, "value": 1.6}}])
    return at + VOM[key]["dur"]


def story_caption(t0, t1, kicker, line, red=False):
    b.text(T4, t0, t1, kicker, (120, 64, 900, 46), style(26, 700, "#FFE8857D" if red else MINT, spacing=4, shadow=False,
                                                        box_color=PILL), anim_in="fade", srt=False)
    b.text(T1, t0 + 0.15, t1, line, (120, 130, 1100, 100), style(58, 800, box_color=PILL), anim_in="fade-scale")


# ---------------------------------------------------------------- scenes
def bg_music():
    b.place("bg.png", BG, 0, END)
    m = call("place_clip", {"asset": "music_v2.wav", "at": 0, "track": MUSIC})["id"]
    keys = [(0.0, 0.35), (17.5, 0.35), (18.2, 0.5), (23.6, 0.5), (24.2, 0.14), (172.6, 0.14), (173.3, 0.42),
            (180.2, 0.42), (180.6, 0.2), (186.6, 0.2), (187.3, 0.45)]
    apply([{"tool": "set_volume", "args": {"clip": m, "at": t, "value": v}} for t, v in keys])


def s_hook():
    b.place("sc_trail.mp4", VB, 0.0, 9.0, fade=(0.6, 0.0))
    vo("hook_trail", 1.2)
    b.text(T1, 5.0, 8.7, "No signal.", (120, 120, 900, 160), style(120, 800), anim_in="blur-in")
    b.place("sc_collapse.mp4", VB, 9.0, 9.0, fade=(0.25, 0.4))
    vo("hook_collapse", 9.8)
    b.text(T1, 14.3, 17.7, "No help?", (120, 120, 900, 160), style(120, 800), anim_in="blur-in")
    b.sfx("sfx_whoosh.wav", 17.6, lane=SFX1, vol=0.6)


def s_reveal():
    hb = (250, 30, 699.5, 1020)
    h = b.place("hero_front.png", G3, 18.0, 4.5, hb, fade=(0.8, 0.25))
    apply(b.push(h, 18.0, 22.5, hb, 1.06))
    lb = (260, 70, 1400, 810.5)
    lg = b.place("oled_01.png", G3, 22.5, 4.0, lb, fade=(0.2, 0.3))
    apply(b.pop(lg, 22.5, lb, 0.98, 0.2) + b.push(lg, 22.7, 26.5, lb, 1.03))
    call("place_clip", {"asset": "ranger_startup_voice_8khz.wav", "at": 22.5, "track": VOICE})
    vo("reveal", 24.0)
    hb2 = (250, 30, 699.5, 1020)
    h2 = b.place("hero_front.png", G4, 26.3, 5.7, hb2, fade=(0.3, 0.4))
    apply(b.push(h2, 26.3, 32.0, hb2, 1.04))
    b.text(T1, 26.6, 31.6, "Meet Ranger.", (1060, 330, 760, 140), style(104, 800))
    b.text(T2, 27.3, 31.6, "No towers · No SIM · No internet", (1064, 480, 780, 80), style(40, 500, MIST, spacing=0),
           anim_in="fade-up-char")


def s_range():
    b.place("sc_range.mp4", VB, 32.0, 13.0, fade=(0.4, 0.3))
    vo("range", 32.5)
    b.text(T1, 33.4, 38.8, "Up to 8 km", (120, 100, 1000, 130), style(110, 800))
    b.text(T2, 33.8, 38.8, "Open line of sight (maker rating)", (124, 240, 1000, 60), style(36, 500, MIST, spacing=0),
           anim_in="fade")
    b.text(T1, 39.0, 44.8, "Up to 202 kbps", (120, 100, 1100, 130), style(110, 800))
    b.text(T2, 39.4, 44.8, "LoRa data rate (SX1280) at shorter range", (124, 240, 1100, 60),
           style(36, 500, MIST, spacing=0), anim_in="fade")
    for t in (33.2, 35.0, 36.8):
        b.sfx("sfx_chirp.wav", t, lane=SFX1, vol=0.35)


def s_mesh():
    b.place("sc_mesh.mp4", VB, 45.0, 16.0, fade=(0.3, 0.3))
    vo("mesh", 45.5)
    b.text(T4, 45.6, 60.7, "MESH NETWORK", (120, 60, 700, 46), style(28, 700, MINT, spacing=4, shadow=False,
                                                                       box_color=PILL), anim_in="fade", srt=False)
    for t0, t1, s in ((46.4, 51.8, "Every Ranger is a relay"), (52.0, 56.4, "Each hop: up to 8 km"),
                      (56.6, 60.7, "Encrypted end to end")):
        b.text(T1, t0, t1, s, (120, 124, 1000, 100), style(60, 800, box_color=PILL), anim_in="fade-scale")
    for t in (46.0, 46.75, 47.5, 48.25, 49.0, 49.75, 50.5):
        b.sfx("sfx_blip.wav", t, lane=SFX2, vol=0.3)


FEATS = [(1, ["04"], "FIND YOUR PEOPLE", "See who's nearby", "f_people"),
         (2, ["17", "18"], "TEXT MESSAGING", "Text without towers", "f_text"),
         (3, ["21", "22"], "PUSH-TO-TALK VOICE", "Hold to talk", "f_talk"),
         (4, ["07"], "TRACK & NAVIGATE", "Arrow points to them", "f_track"),
         (5, ["08"], "NO GPS? RADIO RANGING", "Distance by radio", "f_ranging"),
         (6, ["10", "15"], "YOUR LOCATION", "Share your position", "f_location"),
         (7, ["19", "20"], "SOS", "SOS to everyone", "f_sos"),
         (8, ["26"], "LOW-POWER SLEEP", "Sleeps, still listening", "f_sleep")]


def s_features(T0=61.0):
    fb = (150, 165, 600, 750)
    ob = (830, 140, 960, 555.8)
    for i, (foot, screens, kick, cap, key) in enumerate(FEATS):
        bt = T0 + 6 * i
        f = b.place(f"foot_{foot}.webm", V1, bt, 6.0, fb, fade=(0.3, 0.25))
        apply(b.box_keys(f, bt, bt + 0.5, (fb[0], fb[1] + 24, fb[2], fb[3]), fb, "settle"))
        last = i == len(FEATS) - 1
        if len(screens) == 1:
            o = b.place(f"oled_{screens[0]}.png", G3, bt + 0.5, 5.5, ob, fade=(0.2, 0.6 if last else 0.25))
            apply(b.pop(o, bt + 0.5, ob, 0.98, 0.2))
            b.sfx("sfx_blip.wav", bt + 0.5, lane=SFX1, vol=0.5)
        else:
            o = b.place(f"oled_{screens[0]}.png", G3, bt + 0.5, 2.9, ob, fade=(0.2, 0.0))
            apply(b.pop(o, bt + 0.5, ob, 0.98, 0.2))
            o2 = b.place(f"oled_{screens[1]}.png", G4, bt + 3.3, 2.7, ob, fade=(0.0, 0.25))
            apply(b.pop(o2, bt + 3.3, ob, 0.98, 0.2))
            b.sfx("sfx_blip.wav", bt + 0.5, lane=SFX1, vol=0.5)
            b.sfx("sfx_blip.wav", bt + 3.3, lane=SFX2, vol=0.5)
        sos = kick == "SOS"
        b.text(T2, bt + 0.6, bt + 5.75, kick, (884, 720, 900, 46),
               style(28, 700, "#FFE8857D" if sos else MINT, spacing=4, shadow=False), anim_in="fade", srt=False)
        cst = style(72, 800, box_color=RED) if sos else style(72, 800)
        b.text(T1, bt + 0.75, bt + 5.75, cap, (884 if not sos else 902, 780, 900, 110), cst)
        vo(key, bt + 0.6)
    b.place("qr_corner.png", G1, T0 + 0.5, 63.0, (1748, 870, 132, 152.2), fade=(0.5, 0.5), opacity=0.8)


def s_phones(T0=109.0, dur=16.0):
    pb = (300, 70, 485.5, 920)
    n = 6
    step = dur / n
    for k in range(n):
        t0 = T0 + step * k
        lane = G3 if k % 2 == 0 else G4
        c = b.place(f"phone_0{k + 1}.png", lane, round(t0, 3), round(min(step + 0.4, T0 + dur - t0), 3), pb,
                    fade=(0.4, 0.4))
        if k == 0:
            apply(b.pop(c, t0, pb, 0.94, 0.5))
        else:
            b.sfx("sfx_blip.wav", round(t0, 3), lane=SFX2, vol=0.3)
    ob = (1060, 250, 760, 440)
    for t0, t1, scr in ((T0 + 0.6, T0 + 7.0, "25"), (T0 + 7.0, T0 + 15.6, "11")):
        o = b.place(f"oled_{scr}.png", G2, t0, t1 - t0, ob, fade=(0.2, 0.3))
        apply(b.pop(o, t0, ob, 0.98, 0.2))
        b.sfx("sfx_blip.wav", t0, lane=SFX1, vol=0.5)
    b.place("wifi_link.webm", V1, T0 + 0.8, dur - 1.2, (770, 400, 300, 115.4), fade=(0.4, 0.4))
    b.text(T2, T0 + 0.8, T0 + dur - 0.6, "PHONES JOIN IN", (1064, 700, 760, 46),
           style(28, 700, MINT, spacing=4, shadow=False), anim_in="fade", srt=False)
    for t0, t1, s in ((T0 + 1.0, T0 + 6.8, "No app. Just Wi-Fi."), (T0 + 7.2, T0 + dur - 0.6, "Lend your phone's GPS & clock")):
        b.text(T1, t0, t1, s, (1064, 760, 780, 150), style(60, 800, valign="top"))
    vo("phones", T0 + 0.6)


def s_uses():
    b.place("sc_desert.mp4", VB, 125.0, 9.0, fade=(0.3, 0.0))
    vo("uc_desert", 125.6)
    story_caption(126.4, 133.6, "REMOTE PATROLS", "No infrastructure needed")
    b.sfx("sfx_chirp.wav", 126.2, lane=SFX1, vol=0.35)
    b.place("sc_rubble.mp4", VB, 134.0, 8.0, fade=(0.25, 0.0))
    vo("uc_rubble", 134.5)
    story_caption(134.8, 141.6, "SEARCH & RESCUE", "A voice through the rubble")
    b.place("sc_jungle.mp4", VB, 142.0, 8.0, fade=(0.25, 0.0))
    vo("uc_jungle", 142.5)
    story_caption(142.8, 149.6, "LOST IN THE JUNGLE", "SOS hops across the mesh", red=True)
    for t in (143.6, 144.2, 144.8, 145.4):
        b.sfx("sfx_blip.wav", t, lane=SFX2, vol=0.3)
    b.place("sc_trail_day.mp4", VB, 150.0, 5.0, fade=(0.25, 0.35))
    vo("uc_trail", 150.4)
    story_caption(150.6, 154.6, "HIKERS & CAMPERS", "Always know where your team is")


def s_parts(T0=155.0):
    keys = ["esp32", "lora", "oled", "mic", "amp", "gps"]
    lanes = [G1, G2, G3, G4, G5, G6]
    cw, ch = 539.4, 434.8  # 620 x 500 card at 0.87
    xs, ys = (95, 690, 1285), (110, 560)
    b.text(T4, T0 + 0.2, T0 + 9.8, "WHAT'S INSIDE", (96, 40, 1728, 46),
           style(28, 700, MINT, align="center", spacing=4, shadow=False), anim_in="fade", srt=False)
    b.text(T3, T0 + 0.6, T0 + 9.8, "Parts shown as illustrations", (96, 1020, 1728, 40),
           style(22, 500, MIST, align="center", spacing=0, shadow=False), anim_in="fade", srt=False)
    for k, key in enumerate(keys):
        t0 = round(T0 + 0.3 + 0.55 * k, 3)
        box = (xs[k % 3], ys[k // 3], cw, ch)
        c = b.place(f"part_{key}.png", lanes[k], t0, round(T0 + 10.0 - t0, 3), box, fade=(0.25, 0.3))
        apply(b.pop(c, t0, box, 0.94, 0.35))
        b.sfx("sfx_pop.wav", t0, lane=SFX1 if k % 2 == 0 else SFX2, vol=0.3)
    vo("parts", T0 + 0.4)


def s_cost(T0=165.0):
    hb = (150, 60, 658.4, 960)
    h = b.place("hero_front.png", G3, T0, 8.0, hb, fade=(0.4, 0.35))
    apply(b.push(h, T0, T0 + 8.0, hb, 1.04))
    b.text(T4, T0 + 0.4, T0 + 7.7, "MASS PRODUCTION", (960, 300, 860, 46), style(28, 700, MINT, spacing=4, shadow=False),
           anim_in="fade", srt=False)
    b.text(T1, T0 + 0.6, T0 + 7.7, "≈ Rs. 3,000", (956, 350, 900, 190), style(150, 800))
    b.text(T2, T0 + 1.2, T0 + 7.7, "per unit, estimated", (962, 545, 860, 60), style(42, 500, MIST, spacing=0),
           anim_in="fade")
    b.text(T3, T0 + 2.0, T0 + 7.7, "No SIM · No plan · Free to use", (962, 630, 860, 60), style(40, 700),
           anim_in="fade")
    vo("cost", T0 + 0.6)


def s_built(T0=173.0):
    b.text(T2, T0 + 0.2, T0 + 5.8, "OPEN-SOURCE HARDWARE & FIRMWARE", (96, 70, 1728, 46),
           style(28, 700, MINT, align="center", spacing=4, shadow=False), anim_in="fade", srt=False)
    c = b.place("card_proto.png", G3, T0, 2.1, (442, 150, 1036, 638.6), fade=(0.3, 0.0))
    apply(b.push(c, T0, T0 + 2.1, (442, 150, 1036, 638.6), 1.04))
    c = b.place("card_pcb.png", G4, T0 + 2.0, 2.1, (560, 140, 800, 666), fade=(0.15, 0.0))
    apply(b.push(c, T0 + 2.0, T0 + 4.1, (560, 140, 800, 666), 1.04))
    c = b.place("render_top.png", G3, T0 + 4.0, 2.0, (420, 110, 540.8, 720), fade=(0.2, 0.3))
    apply(b.pop(c, T0 + 4.0, (420, 110, 540.8, 720), 0.95, 0.4))
    c = b.place("render_bottom.png", G4, T0 + 4.15, 1.85, (980, 110, 524.2, 720), fade=(0.2, 0.3))
    apply(b.pop(c, T0 + 4.15, (980, 110, 524.2, 720), 0.95, 0.4))
    for t0, t1, s in ((T0 + 0.2, T0 + 1.95, "From breadboard"), (T0 + 2.15, T0 + 3.95, "to custom PCB"),
                      (T0 + 4.15, T0 + 5.8, "to Ranger")):
        b.text(T1, t0, t1, s, (96, 850, 1728, 110), style(72, 800, align="center"))
    b.sfx("sfx_whoosh.wav", T0 - 0.2, lane=SFX2, vol=0.5)


def s_end(T0=179.0):
    hb = (110, 20, 548.4, 800)
    h = b.place("hero_front.png", G3, T0, END - T0, hb, fade=(0.6, 0.6))
    apply(b.push(h, T0, END, hb, 1.04))
    lb = (680, 250, 560, 324.2)
    lg = b.place("oled_01.png", G4, T0 + 0.3, END - T0 - 0.3, lb, fade=(0.2, 0.6))
    apply(b.pop(lg, T0 + 0.3, lb, 0.98, 0.2))
    call("place_clip", {"asset": "ranger_startup_voice_8khz.wav", "at": T0 + 0.3, "track": VOICE})
    qb = (1290, 150, 546.8, 620)
    q = b.place("qr_end.png", G2, T0 + 0.7, END - T0 - 0.7, qb, fade=(0.27, 0.6))
    apply(b.pop(q, T0 + 0.7, qb, 0.9, 0.267))
    b.sfx("sfx_pop.wav", T0 + 0.7, lane=SFX1, vol=0.6)
    b.text(T1, T0 + 1.2, END, "When the network goes down,\nRanger keeps you connected.", (150, 820, 1100, 140),
           style(54, 800, valign="top"), anim_out=None)
    b.text(T2, T0 + 2.0, END, "nadeeshanj.dev/ranger   ·   hackster.io/nadeeshanj/ranger-421e83",
           (150, 965, 1200, 50), style(30, 500, MIST, spacing=0), anim_in="fade", anim_out=None)
    vo("end", T0 + 1.6)
    ids = call("inspect", {"clips": True})
    for t in ids["tracks"]:
        for c in t.get("items", []):
            if t["i"] in (T1, T2) and abs(c["start"] + c["duration"] - END) < 0.05:
                apply([{"tool": "set_fade", "args": {"clip": c["id"], "out": 0.6}}])


def write_vo_srt(path, placements):
    def ts(s):
        ms = int(round(s * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    with open(path, "w") as fh:
        for i, (a, key) in enumerate(sorted(placements), 1):
            fh.write(f"{i}\n{ts(a)} --> {ts(a + VOM[key]['dur'])}\n{VOM[key]['text']}\n\n")


if __name__ == "__main__":
    placed = []
    _vo = vo

    def vo(key, at):  # noqa: F811 - record placements for the narration .srt
        placed.append((at, key))
        return _vo(key, at)

    globals()["vo"] = vo
    setup()
    for fn in (bg_music, s_hook, s_reveal, s_range, s_mesh, s_features, s_phones, s_uses, s_parts, s_cost,
               s_built, s_end):
        fn()
        print("built", fn.__name__, flush=True)
    write_vo_srt(os.path.join(V2, "ranger_v2.srt"), placed)
    print(call("save_project", {"path": os.path.join(V2, "ranger_v2.json")}))
    print(json.dumps({k: v for k, v in call("inspect", {}).items() if k in ("dur", "clips", "w", "h", "fps")}))
