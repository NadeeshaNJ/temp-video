"""Native Canva version of the 'Built From Scratch' strip: one card per step, each photo its own image."""
import json, sys
P = "PBvtq4xpxV1qRWvd"
GREEN, GOLD = "#2F6D4F", "#C9931A"
ops, fmt, groups = [], [], []


def rect(l, t, w, h, color, r=0, stroke=None, sw=0):
    o = {"type": "insert_shape", "page_id": P, "left": l, "top": t, "width": w, "height": h,
         "path": f"M0 0H{w}V{h}H0Z", "view_box_width": w, "view_box_height": h, "color": color}
    if r:
        o["corner_rounding"] = r
    if stroke:
        o["stroke_color"], o["stroke_weight"] = stroke, sw
    ops.append(o)
    return ("shape", l, t)


def image(asset, l, t, w, h, alt):
    ops.append({"type": "insert_fill", "page_id": P, "asset_type": "image", "asset_id": asset,
                "left": round(l, 1), "top": round(t, 1), "width": round(w, 1), "height": round(h, 1), "alt_text": alt})
    return ("rect", round(l, 1), round(t, 1))


def fit(l, t, bw, bh, iw, ih):
    s = min(bw / iw, bh / ih)
    w, h = iw * s, ih * s
    return l + (bw - w) / 2, t + (bh - h) / 2, w, h


# (asset id, pixel size, alt text) per step; step 4 has two renders side by side
steps = [
    [("MAHXTt8DSvI", (897, 720), "Breadboard prototype of Ranger")],
    [("MAHXTkbeQfE", (881, 620), "Ranger ESP32 schematic")],
    [("MAHXTqLQACM", (862, 691), "Custom 4-layer PCB layout")],
    [("MAHXTk_Qo-w", (524, 780), "3D render, front of the PCB"), ("MAHXTu8vmHA", (478, 745), "3D render, back of the PCB")],
    [("MAHXTtOrZwI", (1301, 2176), "Assembled Ranger handset")],
]
captions = ["LB7BBw1j8Qz8Tc7P", "LBvQfYdzl0jgjbs2", "LBgwhcL2vggj8dzr", "LBbVrv57PGbYkb48", "LB6kjDcX01wWZg22"]

ops.append({"type": "delete_element", "locator_id": f"{P}-LBtX446YLwpLHJpZ"})
TOP, CW, CH, PAD = 2956, 480, 390, 12
for i, imgs in enumerate(steps):
    x0 = round(176 + i * 586.5)
    pcb = i == 2
    g = [rect(x0, TOP, CW, CH, "#1A163A" if pcb else "#FFFFFF", 15, GREEN if pcb else "#D3E2D9", 3 if pcb else 1.5)]
    il, it, iw, ih = x0 + PAD, TOP + PAD, CW - 2 * PAD, CH - 2 * PAD
    if len(imgs) == 1:
        a, (pw, ph), alt = imgs[0]
        g.append(image(a, *fit(il, it, iw, ih, pw, ph), alt))
    else:
        half = (iw - 6) / 2
        for k, (a, (pw, ph), alt) in enumerate(imgs):
            g.append(image(a, *fit(il + k * (half + 6), it, half, ih, pw, ph), alt))
    cx, cy = x0 + 35, 2981
    g.append(rect(cx - 23, cy - 23, 46, 46, GOLD if pcb else GREEN, 23))
    ops.append({"type": "add_text", "page_id": P, "left": cx - 23, "top": cy - 16, "width": 46, "text": str(i + 1)})
    fmt.append(((cx - 23, cy - 16), {"font_size": 27, "color": "#FFFFFF", "font_weight": "bold", "text_align": "center",
                                     "line_height": 1.2}))
    g.append(("text", cx - 23, cy - 16))
    g.append(("caption", captions[i]))
    groups.append(g)
    if i < 4:   # arrow to the next card
        w, h = 86, 22
        ops.append({"type": "insert_shape", "page_id": P, "left": x0 + 495, "top": 3151 - h / 2, "width": w, "height": h,
                    "path": f"M0 7.5H{w-18}V0L{w} 11L{w-18} {h}V14.5H0Z", "view_box_width": w, "view_box_height": h,
                    "color": GREEN})

json.dump({"ops": ops, "fmt": fmt, "groups": groups}, open(sys.argv[1], "w"))
print(len(ops), "ops")
