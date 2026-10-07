"""Clean product-style illustration of the assembled Ranger handset (front view).

Layout, parts and silkscreen follow the real board (photos IMG_9658/9673, Top_3D.png, PCB_design.png).
Drawn at 2x and downsampled for smooth edges. Output: transparent PNG.
"""
import math
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SS = 2                      # supersampling
W = 1000 * SS               # front board width in render px
H = int(W * 1.5625)         # board aspect 0.64
KIT = "/home/user/temp-video/Ranger_Video_Kit"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SILK = (236, 239, 242, 255)

# canvas: room for the antenna (upper left), battery wires (upper right) and the shadow
CW, CH = int(W * 2.05), int(H * 1.45)
OX, OY = int(W * 0.78), int(H * 0.36)
img = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))


def X(f):
    return OX + f * W


def Y(f):
    return OY + f * H


def box(x0, y0, x1, y1):
    return [X(x0), Y(y0), X(x1), Y(y1)]


def font(size_w, bold=False):
    return ImageFont.truetype(SANS_B if bold else SANS, max(1, int(size_w * W)))


def lin_grad(size, c0, c1, angle=90):
    """Linear gradient RGBA image; angle 90 = top->bottom, 0 = left->right."""
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    a = math.radians(angle)
    t = (xx * math.cos(a) + yy * math.sin(a))
    t = (t - t.min()) / max(1e-6, (t.max() - t.min()))
    c0, c1 = np.array(c0, np.float32), np.array(c1, np.float32)
    arr = c0[None, None, :] * (1 - t[..., None]) + c1[None, None, :] * t[..., None]
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


def grad_rrect(b, r, c0, c1, angle=90, outline=None, ow=0):
    x0, y0, x1, y1 = [int(round(v)) for v in b]
    w, h = x1 - x0, y1 - y0
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], int(r), fill=255)
    g = lin_grad((w, h), c0, c1, angle)
    img.paste(g, (x0, y0), m)
    if outline:
        ImageDraw.Draw(img).rounded_rectangle([x0, y0, x1, y1], int(r), outline=outline, width=int(ow))


def text(s, fx, fy, size, fill=SILK, anchor="mm", bold=False, rot=0):
    f = font(size, bold)
    if rot:
        l, t, r, b = f.getbbox(s)
        tw, th = r - l + 8, b - t + 8
        t_im = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
        ImageDraw.Draw(t_im).text((tw / 2, th / 2), s, font=f, fill=fill, anchor="mm")
        t_im = t_im.rotate(rot, expand=True, resample=Image.BICUBIC)
        img.alpha_composite(t_im, (int(X(fx) - t_im.width / 2), int(Y(fy) - t_im.height / 2)))
    else:
        ImageDraw.Draw(img).text((X(fx), Y(fy)), s, font=f, fill=fill, anchor=anchor)


def bezier(p0, p1, p2, p3, n=80):
    pts = []
    for i in range(n + 1):
        t = i / n
        a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t ** 2, t ** 3
        pts.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return pts


def cable(pts, width, color, hi=None):
    d = ImageDraw.Draw(img)
    d.line(pts, fill=color, width=int(width), joint="curve")
    for p in (pts[0], pts[-1]):
        d.ellipse([p[0] - width / 2, p[1] - width / 2, p[0] + width / 2, p[1] + width / 2], fill=color)
    if hi:   # thin specular line
        d.line([(x - width * 0.18, y - width * 0.18) for x, y in pts], fill=hi, width=max(1, int(width * 0.18)),
               joint="curve")


def smd(cx, cy, w, h, kind="cap", vertical=False, silk=True):
    """Small 0603-ish part: cap (tan) or resistor (black) with tinned ends and a silkscreen frame."""
    d = ImageDraw.Draw(img)
    if vertical:
        w, h = h, w
    x0, y0, x1, y1 = X(cx - w / 2), Y(cy - h / 2), X(cx + w / 2), Y(cy + h / 2)
    if silk:
        p = 0.012 * W
        d.rounded_rectangle([x0 - p, y0 - p, x1 + p, y1 + p], int(0.006 * W), outline=SILK, width=int(0.0045 * W))
    body = (196, 160, 112, 255) if kind == "cap" else (26, 26, 28, 255)
    d.rectangle([x0, y0, x1, y1], fill=body)
    e = (w if not vertical else h) * 0.22
    tin = (196, 198, 202, 255)
    if vertical:
        d.rectangle([x0, y0, x1, Y(cy - h / 2 + e)], fill=tin)
        d.rectangle([x0, Y(cy + h / 2 - e), x1, y1], fill=tin)
    else:
        d.rectangle([x0, y0, X(cx - w / 2 + e), y1], fill=tin)
        d.rectangle([X(cx + w / 2 - e), y0, x1, y1], fill=tin)


def pad_ring(fx, fy, r_out, r_in, glow=None):
    d = ImageDraw.Draw(img)
    cx, cy = X(fx), Y(fy)
    ro, ri = r_out * W, r_in * W
    g = lin_grad((int(2 * ro), int(2 * ro)), (238, 240, 243, 255), (150, 154, 160, 255), 60)
    m = Image.new("L", g.size, 0)
    ImageDraw.Draw(m).ellipse([0, 0, g.width - 1, g.height - 1], fill=255)
    img.paste(g, (int(cx - ro), int(cy - ro)), m)
    d.ellipse([cx - ri, cy - ri, cx + ri, cy + ri], fill=(10, 11, 13, 255))
    if glow:
        gl = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(gl).ellipse([cx - ri * 0.7, cy - ri * 0.7, cx + ri * 0.7, cy + ri * 0.7], fill=glow)
        img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(ri * 0.35)))


# ------------------------------------------------------------------ shadow + board stack
sil = Image.new("L", img.size, 0)
sd = ImageDraw.Draw(sil)
sd.rounded_rectangle(box(0.0, 0.0, 1.0, 1.04), int(0.035 * W), fill=255)
shadow = Image.new("RGBA", img.size, (12, 24, 32, 0))
shadow.putalpha(sil.point(lambda v: v * 0.42).filter(ImageFilter.GaussianBlur(0.05 * W)))
img.alpha_composite(shadow, (int(0.035 * W), int(0.05 * W)))

# lower (main) board: peeks out at the bottom with "Made by NadeeshaNJ"; side edge gives depth
grad_rrect(box(0.012, 0.03, 1.012, 1.046), 0.03 * W, (20, 22, 25, 255), (8, 9, 11, 255), 90)
grad_rrect(box(0.0, 0.02, 1.0, 1.036), 0.03 * W, (24, 27, 30, 255), (14, 15, 17, 255), 90,
           outline=(44, 48, 54, 255), ow=0.004 * W)
text("Made by NadeeshaNJ", 0.05, 1.0185, 0.034, fill=(225, 228, 232, 255), anchor="lm", bold=True)
# front (keypad) board edge thickness, then the board face
grad_rrect(box(0.006, 0.006, 1.006, 1.006), 0.03 * W, (10, 11, 13, 255), (4, 5, 6, 255), 90)
grad_rrect(box(0.0, 0.0, 1.0, 0.997), 0.03 * W, (30, 33, 37, 255), (13, 15, 17, 255), 70,
           outline=(52, 57, 63, 255), ow=0.004 * W)

rng = np.random.default_rng(3)
noise = (rng.normal(0, 1, (img.height // 4, img.width // 4)) * 3).clip(-8, 8)
nz = Image.fromarray((noise + 128).astype(np.uint8)).resize(img.size, Image.BILINEAR)
face = Image.new("L", img.size, 0)
ImageDraw.Draw(face).rounded_rectangle(box(0.0, 0.0, 1.0, 0.997), int(0.03 * W), fill=255)
tex = Image.merge("RGBA", (nz, nz, nz, face.point(lambda v: v * 0.10)))
img.alpha_composite(tex)

# ------------------------------------------------------------------ copper traces under the mask
TR = (38, 42, 47, 255)
tw = int(0.006 * W)
d = ImageDraw.Draw(img)
traces = [
    [(0.205, 0.43), (0.205, 0.47), (0.10, 0.50), (0.06, 0.53), (0.06, 0.80), (0.10, 0.83)],
    [(0.225, 0.43), (0.225, 0.48), (0.24, 0.50), (0.24, 0.80), (0.30, 0.83), (0.40, 0.83), (0.42, 0.90)],
    [(0.31, 0.43), (0.31, 0.46), (0.40, 0.48), (0.40, 0.76), (0.36, 0.79)],
    [(0.325, 0.43), (0.325, 0.455), (0.56, 0.47), (0.60, 0.50), (0.60, 0.74), (0.55, 0.77), (0.49, 0.77)],
    [(0.08, 0.47), (0.04, 0.50), (0.04, 0.78)],
    [(0.56, 0.52), (0.565, 0.70)],
    [(0.70, 0.52), (0.70, 0.86), (0.62, 0.90), (0.54, 0.90)],
    [(0.735, 0.53), (0.735, 0.88), (0.66, 0.93), (0.56, 0.93)],
    [(0.77, 0.53), (0.77, 0.92), (0.70, 0.965), (0.30, 0.965)],
    [(0.90, 0.52), (0.90, 0.95), (0.86, 0.975)],
    [(0.62, 0.36), (0.62, 0.45), (0.66, 0.48)],
    [(0.86, 0.38), (0.94, 0.36), (0.94, 0.12)],
]
for t in traces:
    d.line([(X(a), Y(b)) for a, b in t], fill=TR, width=tw, joint="curve")

# ------------------------------------------------------------------ silkscreen outlines
sw = int(0.005 * W)
d.rounded_rectangle(box(0.022, 0.012, 0.655, 0.345), int(0.03 * W), outline=SILK, width=sw)
d.line([(X(0.675), Y(0.045)), (X(0.675), Y(0.95))], fill=SILK, width=int(0.0035 * W))
d.line([(X(0.035), Y(0.832)), (X(0.27), Y(0.832)), (X(0.27), Y(0.99))], fill=SILK, width=sw)
text("VOICE2", 0.15, 0.815, 0.038)

# ------------------------------------------------------------------ OLED module
grad_rrect(box(0.045, 0.02, 0.605, 0.326), 0.012 * W, (24, 26, 29, 255), (14, 15, 17, 255), 90,
           outline=(48, 52, 57, 255), ow=0.003 * W)
for hx, hy in ((0.08, 0.042), (0.57, 0.042), (0.08, 0.303), (0.57, 0.303)):
    pad_ring(hx, hy, 0.022, 0.012)
for i, lab in enumerate(("GND", "VCC", "SCL", "SDA")):
    hx = 0.23 + i * 0.062
    pad_ring(hx, 0.038, 0.015, 0.006)
    d = ImageDraw.Draw(img)
    d.ellipse([X(hx) - 0.008 * W, Y(0.038) - 0.008 * W, X(hx) + 0.008 * W, Y(0.038) + 0.008 * W], fill=(170, 150, 90, 255))
    text(lab, hx, 0.064, 0.02)
# flex cable (behind the glass, folding down)
grad_rrect(box(0.235, 0.262, 0.415, 0.318), 0.006 * W, (226, 160, 60, 255), (176, 112, 30, 255), 90)
grad_rrect(box(0.27, 0.262, 0.38, 0.30), 0.004 * W, (24, 26, 29, 255), (20, 22, 24, 255), 90)
# glass + active area
grad_rrect(box(0.065, 0.082, 0.585, 0.272), 0.006 * W, (22, 25, 30, 255), (6, 7, 9, 255), 90,
           outline=(70, 76, 84, 255), ow=0.002 * W)
ax0, ay0, ax1, ay1 = [int(v) for v in box(0.088, 0.096, 0.562, 0.248)]
grad_rrect([ax0, ay0, ax1, ay1], 0, (6, 8, 10, 255), (2, 3, 4, 255), 90)
scr = Image.open(f"{KIT}/oled_screens/transparent_overlay/02_main_menu.png").convert("RGBA")
scr = scr.resize((ax1 - ax0, ay1 - ay0), Image.NEAREST)
a = np.asarray(scr)[..., 3].astype(np.float32) / 255
lum = Image.fromarray((a * 255).astype(np.uint8))
pix = Image.new("RGBA", scr.size, (236, 246, 255, 255))
pix.putalpha(lum)
glow = Image.new("RGBA", scr.size, (150, 200, 255, 255))
glow.putalpha(lum.filter(ImageFilter.GaussianBlur(0.004 * W)).point(lambda v: int(v * 0.55)))
img.alpha_composite(glow, (ax0, ay0))
img.alpha_composite(pix, (ax0, ay0))
# soft glass reflection
refl = Image.new("L", img.size, 0)
ImageDraw.Draw(refl).polygon([(X(0.065), Y(0.082)), (X(0.30), Y(0.082)), (X(0.16), Y(0.272)), (X(0.065), Y(0.272))],
                             fill=26)
clip = Image.new("L", img.size, 0)
ImageDraw.Draw(clip).rectangle(box(0.065, 0.082, 0.585, 0.272), fill=255)
refl = Image.fromarray(np.minimum(np.asarray(refl), np.asarray(clip)))
white = Image.new("RGBA", img.size, (255, 255, 255, 0))
white.putalpha(refl.filter(ImageFilter.GaussianBlur(0.01 * W)))
img.alpha_composite(white)

# ------------------------------------------------------------------ IO-expander IC (TSSOP) + passives
d = ImageDraw.Draw(img)
for i in range(12):
    lx = 0.198 + i * 0.0118
    d.rectangle(box(lx, 0.351, lx + 0.0065, 0.362), fill=(200, 203, 207, 255))
    d.rectangle(box(lx, 0.418, lx + 0.0065, 0.429), fill=(200, 203, 207, 255))
grad_rrect(box(0.19, 0.36, 0.34, 0.42), 0.004 * W, (62, 66, 72, 255), (34, 36, 40, 255), 90,
           outline=(80, 84, 90, 255), ow=0.002 * W)
d = ImageDraw.Draw(img)
d.ellipse([X(0.2) - 0.006 * W, Y(0.406) - 0.006 * W, X(0.2) + 0.006 * W, Y(0.406) + 0.006 * W], fill=(55, 58, 63, 255))
smd(0.135, 0.366, 0.036, 0.016, "cap")
smd(0.135, 0.418, 0.036, 0.016, "res")

# mounting hole with the blue status LED of the main board glowing through it
pad_ring(0.46, 0.405, 0.03, 0.017, glow=(70, 120, 255, 230))

# ------------------------------------------------------------------ keypad
keys = [("1", ".↑#"), ("2↑", "abc"), ("3", "def"),
        ("←4", "ghi"), ("5 Enter", "jkl"), ("6→", "mno"),
        ("7", "pqrs"), ("8↓", "tuv"), ("9", "wxys"),
        ("0", "␣")]
cols, rows = (0.15, 0.335, 0.52), (0.487, 0.591, 0.695, 0.799)
for i, (top, bot) in enumerate(keys):
    cx = cols[i % 3] if i < 9 else cols[1]
    cy = rows[i // 3] if i < 9 else rows[3]
    bw, bh = 0.11, 0.044
    # white switch body with tinned corner tabs
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):
        for sy in (-1, 1):
            tx, ty = cx + sx * (bw / 2 - 0.004), cy + sy * (bh / 2 - 0.006)
            d.rectangle(box(tx - 0.016, ty - 0.008, tx + 0.016, ty + 0.008), fill=(205, 208, 212, 255))
    grad_rrect(box(cx - bw / 2 + 0.006, cy - bh / 2, cx + bw / 2 - 0.006, cy + bh / 2), 0.008 * W,
               (246, 244, 238, 255), (214, 210, 200, 255), 90)
    # beige cap
    grad_rrect(box(cx - 0.041, cy - 0.016, cx + 0.041, cy + 0.016), 0.024 * W,
               (214, 205, 176, 255), (172, 162, 132, 255), 90, outline=(150, 141, 112, 255), ow=0.002 * W)
    hl = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(hl).ellipse(box(cx - 0.03, cy - 0.014, cx + 0.012, cy - 0.004), fill=(255, 255, 255, 70))
    img.alpha_composite(hl.filter(ImageFilter.GaussianBlur(0.004 * W)))
    if top == "5 Enter":
        text("5", cx - 0.03, cy - 0.036, 0.03)
        text("Enter", cx + 0.022, cy - 0.035, 0.022, bold=True)
    else:
        text(top, cx, cy - 0.036, 0.03)
    text(bot, cx, cy + 0.034, 0.029)

# ------------------------------------------------------------------ VOICE (push-to-talk) button
d = ImageDraw.Draw(img)
for ly in (0.865, 0.955):
    d.ellipse([X(0.29) - 0.018 * W, Y(ly) - 0.018 * W, X(0.29) + 0.018 * W, Y(ly) + 0.018 * W], fill=(196, 199, 204, 255))
grad_rrect(box(0.03, 0.848, 0.272, 0.995), 0.02 * W, (230, 230, 226, 255), (190, 190, 186, 255), 90)
# cap sides (height), then the top face
grad_rrect(box(0.045, 0.852, 0.262, 0.99), 0.03 * W, (150, 20, 16, 255), (110, 12, 10, 255), 90)
grad_rrect(box(0.04, 0.845, 0.252, 0.978), 0.03 * W, (238, 64, 52, 255), (196, 34, 26, 255), 75)
hl = Image.new("RGBA", img.size, (0, 0, 0, 0))
ImageDraw.Draw(hl).rounded_rectangle(box(0.06, 0.852, 0.20, 0.872), int(0.02 * W), fill=(255, 255, 255, 80))
img.alpha_composite(hl.filter(ImageFilter.GaussianBlur(0.008 * W)))

# programming header pads
for i in range(3):
    for j in range(2):
        pad_ring(0.43 + i * 0.06, 0.915 + j * 0.037, 0.016, 0.0075)

# ------------------------------------------------------------------ right column: power + volume
# slide switch
grad_rrect(box(0.70, 0.026, 0.885, 0.072), 0.006 * W, (232, 234, 238, 255), (150, 154, 160, 255), 90,
           outline=(110, 114, 120, 255), ow=0.002 * W)
grad_rrect(box(0.72, 0.034, 0.865, 0.064), 0.004 * W, (90, 94, 100, 255), (60, 63, 68, 255), 90)
grad_rrect(box(0.73, 0.036, 0.785, 0.062), 0.004 * W, (40, 42, 46, 255), (18, 19, 21, 255), 90)
d = ImageDraw.Draw(img)
for lx in (0.735, 0.792, 0.85):
    d.rectangle(box(lx - 0.011, 0.072, lx + 0.011, 0.092), fill=(205, 208, 212, 255))
    d.rectangle(box(lx - 0.016, 0.075, lx + 0.016, 0.096), outline=SILK, width=int(0.004 * W))
text("ON", 0.735, 0.113, 0.034)
text("OFF", 0.85, 0.113, 0.034)

# battery wires (behind) + JST connector
w1 = bezier((X(0.925), Y(0.03)), (X(0.93), Y(-0.06)), (X(1.05), Y(-0.07)), (X(1.12), Y(-0.02)))
w2 = bezier((X(0.958), Y(0.03)), (X(0.965), Y(-0.035)), (X(1.06), Y(-0.04)), (X(1.13), Y(0.0)))
cable(w2, 0.018 * W, (22, 22, 24, 255), hi=(90, 90, 96, 255))
cable(w1, 0.018 * W, (206, 30, 36, 255), hi=(255, 140, 140, 255))
grad_rrect(box(0.895, 0.012, 0.985, 0.088), 0.006 * W, (250, 250, 247, 255), (214, 212, 205, 255), 0,
           outline=(190, 188, 182, 255), ow=0.002 * W)
d = ImageDraw.Draw(img)
for lx in (0.925, 0.958):
    d.rectangle(box(lx - 0.011, 0.03, lx + 0.011, 0.06), fill=(200, 198, 190, 255))

# volume thumbwheel
vx, vy, vr = 0.80, 0.19, 0.068
grad_rrect([X(vx) - vr * W, Y(vy) - vr * W, X(vx) + vr * W, Y(vy) + vr * W], vr * W, (70, 74, 80, 255),
           (10, 11, 13, 255), 60)
grad_rrect([X(vx) - vr * 0.72 * W, Y(vy) - vr * 0.72 * W, X(vx) + vr * 0.72 * W, Y(vy) + vr * 0.72 * W],
           vr * 0.72 * W, (22, 24, 27, 255), (52, 55, 60, 255), 60)
d = ImageDraw.Draw(img)
d.rounded_rectangle([X(vx) - 0.012 * W, Y(vy) - vr * 0.6 * W, X(vx) + 0.012 * W, Y(vy) + vr * 0.6 * W], int(0.01 * W),
                    fill=(6, 7, 8, 255))
text("VOL", 0.935, 0.183, 0.036)

# power inductor "4R7"
grad_rrect(box(0.695, 0.243, 0.81, 0.318), 0.006 * W, (172, 174, 178, 255), (118, 120, 124, 255), 70,
           outline=(96, 98, 102, 255), ow=0.002 * W)
text("4R7", 0.752, 0.281, 0.04, fill=(70, 72, 76, 255), rot=90)
smd(0.845, 0.272, 0.034, 0.015, "cap", vertical=True)
# SOT-23-6 regulator
d = ImageDraw.Draw(img)
for i in range(3):
    lx = 0.838 + i * 0.022
    d.rectangle(box(lx - 0.004, 0.297, lx + 0.004, 0.304), fill=(200, 203, 207, 255))
    d.rectangle(box(lx - 0.004, 0.326, lx + 0.004, 0.333), fill=(200, 203, 207, 255))
grad_rrect(box(0.826, 0.303, 0.906, 0.327), 0.003 * W, (62, 66, 72, 255), (34, 36, 40, 255), 90)
for cx_, cy_ in ((0.735, 0.345), (0.735, 0.37), (0.885, 0.352), (0.885, 0.377)):
    smd(cx_, cy_, 0.034, 0.015, "cap")
# charger IC (QFN) + passives + LEDs
grad_rrect(box(0.765, 0.432, 0.835, 0.476), 0.004 * W, (62, 66, 72, 255), (34, 36, 40, 255), 90,
           outline=(80, 84, 90, 255), ow=0.002 * W)
d = ImageDraw.Draw(img)
for i in range(5):
    t = 0.772 + i * 0.012
    d.rectangle(box(t, 0.427, t + 0.006, 0.431), fill=(190, 193, 198, 255))
    d.rectangle(box(t, 0.477, t + 0.006, 0.481), fill=(190, 193, 198, 255))
smd(0.718, 0.414, 0.032, 0.014, "res", vertical=True)
smd(0.718, 0.455, 0.032, 0.014, "cap", vertical=True)
smd(0.718, 0.496, 0.032, 0.014, "res", vertical=True)
smd(0.80, 0.405, 0.032, 0.014, "cap")
smd(0.80, 0.505, 0.034, 0.015, "cap")
# LEDs: CHG (off) and PWR (on, green)
for ly, lab, on in ((0.428, "CHG", False), (0.468, "PWR", True)):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(box(0.885, ly - 0.009, 0.945, ly + 0.009), int(0.004 * W), outline=SILK, width=int(0.0045 * W))
    d.rectangle(box(0.895, ly - 0.006, 0.935, ly + 0.006), fill=(236, 236, 228, 255) if not on else (180, 255, 190, 255))
    if on:
        g = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).ellipse(box(0.88, ly - 0.02, 0.95, ly + 0.02), fill=(60, 230, 110, 200))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(0.014 * W)))
text("CHG", 0.915, 0.405, 0.03)
text("PWR", 0.915, 0.492, 0.03)

# ------------------------------------------------------------------ antenna (pigtail -> sleeve -> wire tip)
cab = bezier((X(0.30), Y(0.012)), (X(0.30), Y(-0.06)), (X(0.14), Y(-0.075)), (X(0.02), Y(-0.07)))
ang = math.radians(57)                           # from vertical, leaning left
ux, uy = -math.sin(ang), -math.cos(ang)
sx, sy = cab[-1]
lead = [(sx + ux * t, sy + uy * t) for t in np.linspace(0, 0.10 * W, 12)]
cable(cab + lead[1:], 0.014 * W, (20, 20, 22, 255), hi=(84, 86, 92, 255))
bx, by = lead[-1]
px_, py_ = -uy, ux
whip = Image.new("RGBA", img.size, (0, 0, 0, 0))
wd = ImageDraw.Draw(whip)


def seg(t0, t1, w0, w1, col):
    wd.polygon([(bx + ux * t0 + px_ * w0, by + uy * t0 + py_ * w0), (bx + ux * t1 + px_ * w1, by + uy * t1 + py_ * w1),
                (bx + ux * t1 - px_ * w1, by + uy * t1 - py_ * w1), (bx + ux * t0 - px_ * w0, by + uy * t0 - py_ * w0)],
               fill=col)


k = W
seg(0.0, 0.30 * k, 0.017 * k, 0.017 * k, (26, 27, 30, 255))           # black sleeve
seg(0.0, 0.012 * k, 0.019 * k, 0.019 * k, (44, 46, 50, 255))          # sleeve end caps
seg(0.288 * k, 0.30 * k, 0.019 * k, 0.019 * k, (44, 46, 50, 255))
seg(0.30 * k, 0.52 * k, 0.0045 * k, 0.0035 * k, (222, 226, 232, 255))  # bare wire tip
wd.line([(bx + px_ * 0.008 * k + ux * 0.02 * k, by + py_ * 0.008 * k + uy * 0.02 * k),
         (bx + px_ * 0.008 * k + ux * 0.28 * k, by + py_ * 0.008 * k + uy * 0.28 * k)], fill=(92, 96, 102, 255),
        width=int(0.004 * k))
img.alpha_composite(whip)

# ------------------------------------------------------------------ finish: downsample, crop
out = img.resize((CW // SS, CH // SS), Image.LANCZOS)
bb = out.getchannel("A").point(lambda v: 255 if v > 6 else 0).getbbox()
pad = 12
out = out.crop((bb[0] - pad, bb[1] - pad, bb[2] + pad, bb[3] + pad))
out.save(sys.argv[1])
print(out.size)
