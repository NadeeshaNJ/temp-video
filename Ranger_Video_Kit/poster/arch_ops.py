"""Native Canva version of the system architecture diagram (replaces the flat image)."""
import json, math, sys
P = "PBvtq4xpxV1qRWvd"
GREEN, NAVY, INK, GREY, MINT = "#2F6D4F", "#042034", "#16222B", "#4A5560", "#7CC4A0"
ops, fmt, groups = [], [], []   # fmt: ((left, top), formatting); groups: lists of (kind, left, top)


def rect(l, t, w, h, color, r=0, stroke=None, sw=0, tag=None):
    o = {"type": "insert_shape", "page_id": P, "left": l, "top": t, "width": w, "height": h,
         "path": f"M0 0H{w}V{h}H0Z", "view_box_width": w, "view_box_height": h, "color": color}
    if r:
        o["corner_rounding"] = r
    if stroke:
        o["stroke_color"], o["stroke_weight"] = stroke, sw
    ops.append(o)
    return ("shape", l, t)


def path(l, t, w, h, d, color):
    ops.append({"type": "insert_shape", "page_id": P, "left": l, "top": t, "width": w, "height": h,
                "path": d, "view_box_width": w, "view_box_height": h, "color": color})
    return ("shape", l, t)


def text(l, t, w, s, size, color=INK, bold=False, align="center", lh=1.2):
    ops.append({"type": "add_text", "page_id": P, "left": l, "top": t, "width": w, "text": s})
    fmt.append(((l, t), {"font_size": size, "color": color, "font_weight": "bold" if bold else "normal",
                         "text_align": align, "line_height": lh}))
    return ("text", l, t)


def arrow(x0, x1, yc, h=24):
    w = x1 - x0
    d = f"M0 {h/2-3}H{w-18}V0L{w} {h/2}L{w-18} {h}V{h/2+3}H0Z"
    return path(x0, yc - h / 2, w, h, d, GREEN)


def node(l, t, w, h, title, sub, fill="#FFFFFF"):
    g = [rect(l, t, w, h, fill, 14, GREEN, 3),
         text(l + 10, t + 16, w - 20, title, 28, INK, True),
         text(l + 10, t + 56, w - 20, sub, 20, GREY)]
    groups.append(g)


# panel (the old flat image is deleted)
ops.append({"type": "delete_element", "locator_id": f"{P}-LBHcXvC4z3wt9Wr8"})
rect(131, 2026, 1700, 626, "#F7FAF8", 20)

# column labels
IN_L, IN_W = 151, 330
CPU_L, CPU_W = 571, 530
OUT_L, OUT_W = 1191, 340
TOP, BH, STEP = 2076, 100, 118
text(IN_L, 2038, IN_W, "INPUTS", 22, GREEN, True)
text(CPU_L, 2038, CPU_W, "PROCESSING", 22, GREEN, True)
text(OUT_L, 2038, OUT_W, "OUTPUTS & RADIO", 22, GREEN, True)

# inputs -> ESP32
ins = [("T9 keypad + knob", "menus, typing"), ("Push-to-talk", "VOICE button"),
       ("MEMS microphone", "ICS-43434, I2S"), ("GPS + compass", "u-blox M10, QMC5883")]
for i, (a, b) in enumerate(ins):
    y = TOP + i * STEP
    node(IN_L, y, IN_W, BH, a, b)
    arrow(IN_L + IN_W, CPU_L, y + BH / 2)

# ESP32 core
CPU_B = TOP + 3 * STEP + BH            # 2530
g = [rect(CPU_L, TOP, CPU_W, CPU_B - TOP, NAVY, 20),
     text(CPU_L + 10, 2090, CPU_W - 20, "ESP32-WROOM-32E", 34, "#FFFFFF", True),
     text(CPU_L + 10, 2134, CPU_W - 20, "dual-core 240 MHz, custom firmware", 20, MINT)]
tasks = ["Codec2 voice compression", "AES-128-CCM encryption", "Mesh routing & relaying", "UI, tracking & SOS",
         "Wi-Fi hotspot web page"]
for i, s in enumerate(tasks):
    y = 2174 + i * 70
    g.append(rect(CPU_L + 30, y, CPU_W - 60, 56, "#123C58", 10, MINT, 2))
    g.append(text(CPU_L + 40, y + 14, CPU_W - 80, s, 24, "#FFFFFF", True))
groups.append(g)

# ESP32 -> outputs
outs = [("LoRa radio", "E28 SX1280, 2.4 GHz, 27 dBm"), ("OLED 128×64", "messages, map, compass"),
        ("Amp + speaker", "MAX98357A, I2S"), ("Phones (up to 3)", "Wi-Fi, browser, no app")]
for i, (a, b) in enumerate(outs):
    y = TOP + i * STEP
    node(OUT_L, y, OUT_W, BH, a, b, "#EAF3EE" if i == 0 else "#FFFFFF")
    arrow(CPU_L + CPU_W, OUT_L, y + BH / 2)

# LoRa link to other Rangers: arrow, radio waves, handset icon, label
LY = TOP + BH / 2                       # 2126
arrow(OUT_L + OUT_W, 1594, LY)
cx, cy, th, ang = 0, 34, 5, math.radians(55)
d = ""
for R in (14, 26, 38):
    r = R - th
    p = lambda rad, a: (cx + rad * math.cos(a), cy + rad * math.sin(a))
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p(R, -ang), p(R, ang), p(r, ang), p(r, -ang)
    d += (f"M{x0:.2f} {y0:.2f}A{R} {R} 0 0 1 {x1:.2f} {y1:.2f}L{x2:.2f} {y2:.2f}"
          f"A{r} {r} 0 0 0 {x3:.2f} {y3:.2f}Z")
waves = path(1600, LY - 34, 40, 68, d, GREEN)
icon = [rect(1722, 2050, 6, 36, NAVY, 3), rect(1719, 2042, 12, 12, NAVY, 6),
        rect(1660, 2080, 80, 130, NAVY, 14), rect(1670, 2092, 60, 40, MINT, 6)]
for row in range(3):
    for col in range(3):
        icon.append(rect(1674 + col * 19, 2144 + row * 16, 14, 10, "#C9D3DA", 3))
icon.append(rect(1688, 2193, 24, 9, "#D9534F", 4))
groups.append(icon + [waves])
groups.append([text(1561, 2222, 250, "Other Rangers", 26, INK, True),
               text(1561, 2256, 250, "mesh, up to 8 km/hop", 20, GREY)])

# power bar
groups.append([rect(151, 2550, 1660, 70, "#FFF4D6", 14, "#C9931A", 3),
               text(171, 2570, 1620, "Power: 3.7 V 1000 mAh LiPo  ·  USB-C charging  ·  low-power sleep, radio still listening",
                    24, "#6B4A05", True)])

json.dump({"ops": ops, "fmt": fmt, "groups": groups}, open(sys.argv[1], "w"))
print(len(ops), "ops,", len(fmt), "texts,", len(groups), "groups")
