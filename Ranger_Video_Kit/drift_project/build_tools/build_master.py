"""Builds the Ranger main film (1920x1080, 30 fps, 130 s) in a running Drift
over drift_cli.rpc. One writer, lanes fixed in setup, exact times (overlap on)."""
import json
import os
import sys

SKILL = "/home/user/cutwire-studios/drift-skill/cutwire-drift/scripts"
sys.path.insert(0, SKILL)
import drift_cli as dc  # noqa: E402
import keyframes as kf  # noqa: E402

W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(W, "build/assets")
KIT = "/home/user/temp-video/Ranger_Video_Kit"
END = 130.0

# ---------------------------------------------------------------- palette / type
WHITE = "#FFF2F4F1"
MIST = "#FFB4C0B9"
MINT = "#FF7CC4A0"
RED = "#FFB3261E"

# lanes, top to bottom
T1, T2, T3, T4, G1, G2, V1, G3, G4, V2, BG, SFX1, SFX2, VOICE, MUSIC = range(15)
LANE_TYPES = ["text"] * 4 + ["shape", "shape", "video", "shape", "shape", "video", "shape",
                             "audio", "audio", "audio", "audio"]

LOG = []
captions = []  # (start, end, text) for the .srt


def call(name, args):
    r = dc.text_of(dc.rpc(name, args))
    if isinstance(r, dict) and r.get("ok") is False:
        raise RuntimeError(f"{name} {json.dumps(args)[:300]} -> {json.dumps(r)[:600]}")
    return r


def apply(ops):
    if not ops:
        return []
    out = []
    for i in range(0, len(ops), 150):
        r = call("apply", {"ops": ops[i:i + 150]})
        out += r.get("done", [])
    return out


# ---------------------------------------------------------------- helpers
def place(asset, lane, at, dur, box=None, fade=(0.0, 0.0), opacity=None):
    r = call("place_clip", {"asset": asset, "at": at, "track": lane})
    cid = r["id"]
    if abs(r.get("placed", at) - at) > 0.02 or r.get("track", lane) != lane:
        raise RuntimeError(f"placement drift {asset}: {r}")
    ops = [{"tool": "set_duration", "args": {"clip": cid, "duration": dur}}]
    if box:
        x, y, w, h = box
        ops.append({"tool": "set_transform", "args": {"clip": cid, "x": x, "y": y, "w": w, "h": h}})
    if opacity is not None:
        ops.append({"tool": "set_transform", "args": {"clip": cid, "opacity": opacity}})
    if fade != (0.0, 0.0):
        ops.append({"tool": "set_fade", "args": {"clip": cid, "in": fade[0], "out": fade[1]}})
    apply(ops)
    return cid


def scaled(box, s):
    x, y, w, h = box
    nw, nh = w * s, h * s
    return (x + (w - nw) / 2, y + (h - nh) / 2, nw, nh)


def box_keys(clip, t0, t1, b0, b1, ease):
    props = []
    for prop, i in (("x", 0), ("y", 1), ("width", 2), ("height", 3)):
        if abs(b0[i] - b1[i]) > 0.01:
            props.append({"prop": prop, "ease": ease, "keys": [[t0, round(b0[i], 2)], [t1, round(b1[i], 2)]]})
    return kf.ops_for_clip({"clip": clip, "props": props}) if props else []


def pop(clip, t0, box, s0=0.94, d=0.5):
    """Materialise: scale from s0 with settle (opacity comes from set_fade)."""
    return box_keys(clip, t0, t0 + d, scaled(box, s0), box, "settle")


def push(clip, t0, t1, box, s1=1.05):
    return box_keys(clip, t0, t1, box, scaled(box, s1), "linear")


def style(size, weight=700, color=WHITE, align="left", valign="center", spacing=None, shadow=True,
          box_color=None):
    st = {"fontFamily": "Inter", "fontWeight": weight, "pixelSize": size, "color": color,
          "align": align, "valign": valign, "lineHeight": 1.08, "wordWrap": True,
          "accent": {"rule": "none"}, "boxEnabled": False,
          "letterSpacing": spacing if spacing is not None else round(-size * 0.02, 1)}
    layers = []
    if shadow:
        layers.append({"kind": "shadow", "paint": {"kind": "solid", "color": "#FF0A0D0C"},
                       "opacity": 0.5, "blur": 26, "offsetY": 3})
    layers.append({"kind": "fill", "paint": {"kind": "solid", "color": color}})
    st["layers"] = layers
    if box_color:
        st.update({"boxEnabled": True, "boxColor": box_color, "boxPadding": 18, "boxRadius": 16})
    return st


_park = [400.0]


def text(lane, t0, t1, txt, box, st, anim_in="rise-by-word", anim_out="fade", srt=True):
    _park[0] += 6
    r = call("add_text", {"text": txt, "at": _park[0]})
    cid = r["id"]
    ops = [
        {"tool": "move_to_track", "args": {"clip": cid, "to_track": lane, "at": t0}},
        {"tool": "set_duration", "args": {"clip": cid, "duration": round(t1 - t0, 3)}},
        {"tool": "set_text", "args": {"clip": cid, "style": st}},
        {"tool": "set_transform", "args": {"clip": cid, "x": box[0], "y": box[1], "w": box[2], "h": box[3]}},
    ]
    if anim_in:
        ops.append({"tool": "set_text_animation", "args": {"clip": cid, "which": "in", "preset": anim_in,
                                                          "ease": "easeOut"}})
    if anim_out:
        ops.append({"tool": "set_text_animation", "args": {"clip": cid, "which": "out", "preset": anim_out,
                                                          "ease": "easeIn", "durationOverride": 0.3}})
    done = apply(ops)
    mv = done[0]["result"]
    if mv.get("track", lane) != lane or abs(mv.get("start", t0) - t0) > 0.02:
        raise RuntimeError(f"text landed wrong: {txt} {mv}")
    if srt:
        captions.append((t0, t1, txt.replace("\n", " ")))
    return cid


def sfx(name, at, lane=SFX1, vol=1.0):
    cid = call("place_clip", {"asset": name, "at": at, "track": lane})["id"]
    if vol != 1.0:
        call("set_volume", {"clip": cid, "value": vol})
    return cid


# ---------------------------------------------------------------- setup
def setup():
    call("new_project", {})
    call("set_project_setup", {"width": 1920, "height": 1080, "fps": 30})
    call("set_overlap", {"enabled": True})
    for ty in reversed(LANE_TYPES):
        call("add_track", {"type": ty})
    info = call("inspect", {})
    tracks = info["tracks"]
    for t in reversed(tracks[len(LANE_TYPES):]):
        call("remove_track", {"track": t["i"]})
    info = call("inspect", {})
    got = [t["type"] for t in info["tracks"]]
    assert got == LANE_TYPES, got
    files = sorted(os.path.join(A, f) for f in os.listdir(A)
                   if f.endswith((".png", ".mp4", ".mkv", ".wav")) and not f.startswith("mask"))
    files.append(f"{KIT}/audio/ranger_startup_voice_8khz.wav")
    r = call("import_media", {"paths": files})
    assert not r.get("missing"), r.get("missing")
    print("imported", len(r["assets"]))


# ---------------------------------------------------------------- scenes
def scene_bg_music():
    place("bg.png", BG, 0, END)
    m = call("place_clip", {"asset": "music.wav", "at": 0, "track": MUSIC})["id"]
    apply([{"tool": "set_volume", "args": {"clip": m, "value": 0.8}}])
    # dip under the device voice at the reveal
    apply([{"tool": "set_volume", "args": {"clip": m, "at": t, "value": v}}
           for t, v in ((15.2, 0.8), (15.5, 0.35), (16.9, 0.35), (17.6, 0.8),
                        (120.0, 0.8), (120.25, 0.45), (121.6, 0.45), (122.3, 0.8))])


def scene_hook():
    place("hook.mp4", V2, 0, 10.0, fade=(0, 0.35))
    big = style(128, 800, valign="center")
    for t0, t1, s in ((0.6, 3.3, "No signal."), (3.6, 6.3, "No internet."), (6.6, 9.5, "No help?")):
        text(T1, t0, t1, s, (140, 390, 940, 300), big, anim_in="blur-in")
    sfx("sfx_whoosh.wav", 9.4, vol=0.6)


def scene_reveal():
    hb = (250, 30, 699.5, 1020)
    h = place("hero_front.png", G3, 10.0, 5.6, hb, fade=(0.8, 0.3))
    apply(push(h, 10.0, 15.6, hb, 1.06))
    text(T1, 11.0, 15.3, "Meet Ranger.", (1060, 330, 760, 140), style(104, 800))
    text(T2, 11.9, 15.3, "No towers · No SIM · No internet", (1064, 480, 780, 80),
         style(40, 500, MIST, spacing=0), anim_in="fade-up-char")
    lb = (260, 70, 1400, 810.5)
    lg = place("oled_01.png", G3, 15.6, 4.4, lb, fade=(0.2, 0.35))
    apply(pop(lg, 15.6, lb, 0.98, 0.2) + push(lg, 15.8, 20.0, lb, 1.03))
    call("place_clip", {"asset": "ranger_startup_voice_8khz.wav", "at": 15.6, "track": VOICE})
    text(T1, 17.0, 19.8, "No towers. No SIM. No silence.", (96, 880, 1728, 110),
         style(64, 700, align="center"))


def scene_network():
    place("network.mp4", V2, 20.0, 12.0, fade=(0.4, 0.4))
    text(T4, 20.4, 31.6, "HOW IT WORKS", (140, 300, 700, 50), style(30, 700, MINT, spacing=4, shadow=False),
         anim_in="fade", srt=False)
    items = [(21.6, "Device to device"), (23.8, "Relays for each other"), (26.0, "Encrypted end to end")]
    for (t0, s), lane, y in zip(items, (T1, T2, T3), (370, 460, 550)):
        text(lane, t0, 31.6, s, (140, y, 760, 80), style(54, 700), anim_in="rise-by-word")
    for t in (21.6, 23.7, 26.6, 28.7):
        sfx("sfx_chirp.wav", t, vol=0.55)


FEATURES = [
    # (footage, [oled screens], kicker, caption)
    (1, ["04"], "FIND YOUR PEOPLE", "See who's nearby"),
    (2, ["17", "18"], "TEXT MESSAGING", "Text without towers"),
    (3, ["21", "22"], "PUSH-TO-TALK VOICE", "Hold to talk"),
    (4, ["07"], "TRACK & NAVIGATE", "Arrow points to them"),
    (5, ["08"], "NO GPS? RADIO RANGING", "Distance by radio"),
    (6, ["10", "15"], "YOUR LOCATION", "Share your position"),
    (7, ["19", "20"], "SOS", "SOS to everyone"),
    (8, ["26"], "LOW-POWER SLEEP", "Sleeps, still listening"),
]


def scene_features():
    fb = (150, 165, 600, 750)
    ob = (830, 140, 960, 555.8)
    for i, (foot, screens, kick, cap) in enumerate(FEATURES):
        b = 32.0 + 6 * i
        f = place(f"foot_{foot}.mkv", V1, b, 6.0, fb, fade=(0.3, 0.25))
        apply(box_keys(f, b, b + 0.5, (fb[0], fb[1] + 24, fb[2], fb[3]), fb, "settle"))
        last = i == len(FEATURES) - 1
        if len(screens) == 1:
            o = place(f"oled_{screens[0]}.png", G3, b + 0.5, 5.5, ob, fade=(0.2, 0.6 if last else 0.25))
            apply(pop(o, b + 0.5, ob, 0.98, 0.2))
            sfx("sfx_blip.wav", b + 0.5, vol=0.7)
        else:
            o = place(f"oled_{screens[0]}.png", G3, b + 0.5, 2.9, ob, fade=(0.2, 0.0))
            apply(pop(o, b + 0.5, ob, 0.98, 0.2))
            o2 = place(f"oled_{screens[1]}.png", G4, b + 3.3, 2.7, ob, fade=(0.0, 0.25))
            apply(pop(o2, b + 3.3, ob, 0.98, 0.2))
            # G3 sits above G4: the first screen ends exactly where the second starts
            sfx("sfx_blip.wav", b + 0.5, vol=0.7)
            sfx("sfx_blip.wav", b + 3.3, lane=SFX2, vol=0.7)
        sos = kick == "SOS"
        text(T2, b + 0.6, b + 5.75, kick, (884, 720, 900, 46),
             style(28, 700, "#FFE8857D" if sos else MINT, spacing=4, shadow=False), anim_in="fade", srt=False)
        cst = style(72, 800, box_color=RED) if sos else style(72, 800)
        text(T1, b + 0.75, b + 5.75, cap, (884 if not sos else 902, 780, 900, 110), cst)
    # corner QR during features and phones
    place("qr_corner.png", G1, 32.5, 71.0, (1748, 870, 132, 152.2), fade=(0.5, 0.5), opacity=0.8)


PHONES = ["01", "02", "03", "04", "05", "06"]


def scene_phones():
    pb = (300, 70, 485.5, 920)
    for k, ph in enumerate(PHONES):
        t0 = 80.0 + 4 * k
        lane = G3 if k % 2 == 0 else G4
        dur = 4.0 if k == len(PHONES) - 1 else 4.4
        c = place(f"phone_{ph}.png", lane, t0, min(dur, 104.0 - t0), pb,
                  fade=(0.4, 0.4))
        if k == 0:
            apply(pop(c, t0, pb, 0.94, 0.5))
        else:
            sfx("sfx_blip.wav", t0, lane=SFX2, vol=0.35)
    # The later phone must draw on top while it fades in: odd phones sit on G4 (lower), so
    # give odd phones the fade and keep even ones solid underneath; even phones after the
    # first start on G3 above the previous odd one and fade in over it.
    ob = (1060, 250, 760, 440)
    for t0, t1, scr in ((80.6, 88.0, "25"), (88.0, 96.0, "05"), (96.0, 103.6, "11")):
        o = place(f"oled_{scr}.png", G2, t0, t1 - t0, ob, fade=(0.2, 0.3))
        apply(pop(o, t0, ob, 0.98, 0.2))
        sfx("sfx_blip.wav", t0, vol=0.7)
    place("wifi_link.mkv", V1, 80.8, 22.8, (770, 400, 300, 115.4), fade=(0.4, 0.4))
    sfx("sfx_chirp.wav", 81.0, lane=SFX2, vol=0.5)
    text(T2, 80.8, 103.4, "PHONES JOIN IN", (1064, 700, 760, 46), style(28, 700, MINT, spacing=4, shadow=False),
         anim_in="fade", srt=False)
    for t0, t1, s in ((81.0, 87.8, "No app. Just Wi-Fi."), (88.2, 95.8, "Your phone joins the network"),
                      (96.2, 103.4, "Lend your phone's GPS & clock")):
        text(T1, t0, t1, s, (1064, 760, 780, 150), style(60, 800, valign="top"))


USES = [("Rescue teams"), ("Families"), ("Hikers & campers"), ("Field crews"), ("Events & security"),
        ("Volunteers & NGOs")]


def scene_uses():
    ib = (700, 120, 520, 520)
    d = 10.0 / len(USES)
    text(T2, 104.2, 113.8, "BUILT FOR", (96, 690, 1728, 46), style(28, 700, MINT, align="center", spacing=4,
                                                                    shadow=False), anim_in="fade", srt=False)
    for k, s in enumerate(USES):
        t0 = 104.0 + d * k
        ic = place(f"icon_{k + 1}.png", G3 if k % 2 == 0 else G4, round(t0, 3), round(d, 3), ib)
        apply(pop(ic, round(t0, 3), ib, 0.9, 0.35))
        text(T1, round(t0 + 0.05, 3), round(t0 + d - 0.02, 3), s, (96, 740, 1728, 120),
             style(88, 800, align="center"), anim_in="fade-scale", anim_out=None)
        sfx("sfx_pop.wav", t0, lane=SFX1 if k % 2 == 0 else SFX2, vol=0.4)


def scene_built():
    text(T2, 114.2, 119.8, "OPEN-SOURCE HARDWARE & FIRMWARE", (96, 70, 1728, 46),
         style(28, 700, MINT, align="center", spacing=4, shadow=False), anim_in="fade", srt=False)
    c = place("card_proto.png", G3, 114.0, 2.1, (442, 150, 1036, 638.6), fade=(0.3, 0.0))
    apply(push(c, 114.0, 116.1, (442, 150, 1036, 638.6), 1.04))
    c = place("card_pcb.png", G4, 116.0, 2.1, (560, 140, 800, 666), fade=(0.15, 0.0))
    apply(push(c, 116.0, 118.1, (560, 140, 800, 666), 1.04))
    c = place("render_top.png", G3, 118.0, 2.0, (420, 110, 540.8, 720), fade=(0.2, 0.3))
    apply(pop(c, 118.0, (420, 110, 540.8, 720), 0.95, 0.4))
    c = place("render_bottom.png", G4, 118.15, 1.85, (980, 110, 524.2, 720), fade=(0.2, 0.3))
    apply(pop(c, 118.15, (980, 110, 524.2, 720), 0.95, 0.4))
    for t0, t1, s in ((114.2, 115.95, "From breadboard"), (116.15, 117.95, "to custom PCB"),
                      (118.15, 119.8, "to Ranger")):
        text(T1, t0, t1, s, (96, 850, 1728, 110), style(72, 800, align="center"))
    sfx("sfx_whoosh.wav", 113.8, lane=SFX2, vol=0.5)


def scene_end():
    hb = (110, 20, 548.4, 800)
    h = place("hero_front.png", G3, 120.0, 10.0, hb, fade=(0.6, 0.6))
    apply(push(h, 120.0, 130.0, hb, 1.04))
    lb = (680, 250, 560, 324.2)
    lg = place("oled_01.png", G4, 120.3, 9.7, lb, fade=(0.2, 0.6))
    apply(pop(lg, 120.3, lb, 0.98, 0.2))
    call("place_clip", {"asset": "ranger_startup_voice_8khz.wav", "at": 120.3, "track": VOICE})
    qb = (1290, 150, 546.8, 620)
    q = place("qr_end.png", G2, 120.7, 9.3, qb, fade=(0.27, 0.6))
    apply(pop(q, 120.7, qb, 0.9, 0.267))
    sfx("sfx_pop.wav", 120.7, vol=0.6)
    text(T1, 121.2, 130.0, "When the network goes down,\nRanger keeps you connected.", (150, 820, 1100, 140),
         style(54, 800, valign="top"), anim_out=None)
    text(T2, 122.0, 130.0, "nadeeshanj.dev/ranger   ·   hackster.io/nadeeshanj/ranger-421e83", (150, 965, 1200, 50),
         style(30, 500, MIST, spacing=0), anim_in="fade", anim_out=None)
    # fade the last text out with the film
    ids = call("inspect", {"clips": True})
    for t in ids["tracks"]:
        for c in t.get("items", []):
            if t["i"] in (T1, T2) and abs(c["start"] + c["duration"] - END) < 0.05:
                apply([{"tool": "set_fade", "args": {"clip": c["id"], "out": 0.6}}])


def write_srt(path):
    def ts(s):
        ms = int(round(s * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    rows = sorted(captions)
    with open(path, "w") as fh:
        for i, (a, b, t) in enumerate(rows, 1):
            fh.write(f"{i}\n{ts(a)} --> {ts(b)}\n{t}\n\n")


if __name__ == "__main__":
    setup()
    for fn in (scene_bg_music, scene_hook, scene_reveal, scene_network, scene_features, scene_phones,
               scene_uses, scene_built, scene_end):
        fn()
        print("built", fn.__name__, flush=True)
    write_srt(os.path.join(W, "build/ranger_main.srt"))
    try:
        print(call("save_project", {"path": os.path.join(W, "build/ranger_master.json")}))
    except RuntimeError as e:
        print("save failed", e)
    print(json.dumps({k: v for k, v in call("inspect", {}).items() if k in ("dur", "clips", "w", "h", "fps")}))
