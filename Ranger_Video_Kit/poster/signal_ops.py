"""Light-blue 'Wi-Fi style' signal arcs from each hero device's antenna tip, facing each other."""
import json, math, sys
P = "PBvtq4xpxV1qRWvd"
BLUE = "#4FC3F7"
ART = (16, 13)                     # antenna tip in 5_assembled_render.png (1667 x 2177)
devices = {                        # element left, top, width (from the design)
    "big": (964.712, 959.0, 660.698),
    "small": (222.708, 1135.2, 449.790),
}


def tip(name):
    l, t, w = devices[name]
    s = w / 1667
    return l + ART[0] * s, t + ART[1] * s


def arc_path(R, th, a0, a1, S):
    """Ring segment (centre (S,S) in an SxS*2 box) with rounded ends, angles in degrees (SVG, y down)."""
    ro, ri, rc = R + th / 2, R - th / 2, th / 2
    p = lambda r, a: (S + r * math.cos(math.radians(a)), S + r * math.sin(math.radians(a)))
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p(ro, a0), p(ro, a1), p(ri, a1), p(ri, a0)
    f = lambda v: f"{v:.2f}"
    return (f"M{f(x1)} {f(y1)}A{f(ro)} {f(ro)} 0 0 1 {f(x2)} {f(y2)}A{f(rc)} {f(rc)} 0 0 1 {f(x3)} {f(y3)}"
            f"A{f(ri)} {f(ri)} 0 0 0 {f(x4)} {f(y4)}A{f(rc)} {f(rc)} 0 0 1 {f(x1)} {f(y1)}Z")


ops, sets = [], {}
big, small = tip("big"), tip("small")
for name, (cx, cy), other, k in (("big", big, small, 1.0), ("small", small, big, 0.68)):
    d = math.degrees(math.atan2(other[1] - cy, other[0] - cx))     # face the other device
    d += 6 if name == "big" else -7                                 # tilt up a little, clear of the antenna wire
    spread = 42
    items = []
    for i, (R, op) in enumerate(((38, 1.0), (70, 0.8), (102, 0.6))):
        R, th = R * k, 13 * k
        for glow in (True, False):
            t = th * 2.6 if glow else th
            S = R + t / 2 + 2
            ops.append({"type": "insert_shape", "page_id": P, "left": round(cx - S, 2), "top": round(cy - S, 2),
                        "width": round(2 * S, 2), "height": round(2 * S, 2), "path": arc_path(R, t, d - spread, d + spread, S),
                        "view_box_width": round(2 * S, 2), "view_box_height": round(2 * S, 2), "color": BLUE,
                        "opacity": round(op * (0.2 if glow else 1.0), 3)})
            items.append((round(cx - S, 2), round(cy - S, 2)))
    r = 9 * k
    ops.append({"type": "insert_shape", "page_id": P, "left": round(cx - r, 2), "top": round(cy - r, 2),
                "width": round(2 * r, 2), "height": round(2 * r, 2), "path": f"M0 0H{2*r:.2f}V{2*r:.2f}H0Z",
                "view_box_width": round(2 * r, 2), "view_box_height": round(2 * r, 2), "color": BLUE,
                "corner_rounding": round(r, 2)})
    items.append((round(cx - r, 2), round(cy - r, 2)))
    sets[name] = {"tip": (cx, cy), "dir": d, "items": items}

# keep the long-standing groups at the end of the element list so the new shapes are visible in the reply
front = ["LBcYCwmkf2d4hMX0", "LB9Jbvjzd6PXJV9H", "LB1mRk3JlY5lStmn", "LBxfCNH0MNryylgv", "LBLkQ0h4nPP2xntR",
         "LB1LpGk3fMgzBDdf", "LBnJ1JZRPNDY927J", "LBZFvfp9jGxHPKlj", "LBSN40tBSBcfdPs3", "LBF74fk8jR3Xpz5q",
         "LB5VP1nCF5LqqrHl", "LB49mfpPrYl7qd6K", "LBvPXxVL0JmP8XLV", "LBcbnnFnbYh7NktQ", "LB8rjS5Vz2YtFSYz",
         "LBqY7wHHlk566Rf7", "LB0swCKKShKLl4vr"]
ops += [{"type": "layer_element", "locator_id": f"{P}-{g}", "position": "front"} for g in front]
json.dump({"ops": ops, "sets": sets}, open(sys.argv[1], "w"))
print(len(ops), "ops;", {k: (round(v["tip"][0]), round(v["tip"][1]), round(v["dir"], 1)) for k, v in sets.items()})
