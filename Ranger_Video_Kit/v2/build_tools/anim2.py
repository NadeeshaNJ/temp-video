"""Illustrated story scenes for Ranger v2 (silhouette style, parallax), rendered to mp4."""
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(W, "build/v2/scenes")
os.makedirs(OUT, exist_ok=True)
FONT = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
FPS = 30
SZ = (1920, 1080)
GREEN = (0x2F, 0x6D, 0x4F)
MINT = (0x7C, 0xC4, 0xA0)
PALE = (0xBF, 0xF0, 0xD4)
RED = (0xB3, 0x26, 0x1E)
rng = np.random.default_rng(11)


def font(w, s):
    return ImageFont.truetype(FONT.format(w), s)


def ease(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def eout(t):
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3


def writer(path):
    return subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080",
                             "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "14", "-preset", "medium",
                             "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)


def gradient(top, bottom, h=1080, w=1920):
    t = np.linspace(0, 1, h)[:, None, None]
    c = np.array(top, np.float32) * (1 - t) + np.array(bottom, np.float32) * t
    return Image.fromarray(np.repeat(c, w, 1).astype(np.uint8)).convert("RGBA")


def ridge(w, base, amp, seed, rough=0.5, color=(0, 0, 0), h=1080, step=8):
    r = np.random.default_rng(seed)
    xs = np.arange(0, w + step, step)
    y = np.zeros_like(xs, np.float64)
    for k, f in enumerate((1.3, 2.9, 6.1, 13.0)):
        y += amp * (rough ** k) * np.sin(xs / w * f * math.pi + r.uniform(0, 6))
    pts = [(int(x), int(base - v)) for x, v in zip(xs, y)] + [(w, h), (0, h)]
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).polygon(pts, fill=tuple(color) + (255,))
    return im


def ground_y(layer_img, x):
    a = np.asarray(layer_img.getchannel("A"))[:, int(min(max(x, 0), layer_img.width - 1))]
    idx = np.where(a > 0)[0]
    return int(idx[0]) if len(idx) else 1080


def figure(d, x, y, s, phase=0.0, walk=True, color=(10, 12, 12, 255), helmet=False, pack=True, vest=None,
           device=False, lie=False, arm_up=False):
    """Simple silhouette person standing on (x, y) = feet point, height ~ 180*s."""
    c = color
    if lie:
        # lying figure, head to the left
        d.ellipse([x - 90 * s, y - 34 * s, x - 56 * s, y], fill=c)
        d.rounded_rectangle([x - 60 * s, y - 30 * s, x + 30 * s, y - 2 * s], 12 * s, fill=c)
        d.line([x + 26 * s, y - 14 * s, x + 90 * s, y - 8 * s], fill=c, width=int(14 * s))
        d.line([x + 26 * s, y - 20 * s, x + 86 * s, y - 26 * s], fill=c, width=int(14 * s))
        d.line([x - 40 * s, y - 24 * s, x - 70 * s, y - 64 * s], fill=c, width=int(11 * s))  # arm raised
        return (x - 72 * s, y - 72 * s)
    sw = math.sin(phase) if walk else 0.0
    hip = (x, y - 92 * s)
    for sgn in (1, -1):
        a = 0.45 * sw * sgn
        knee = (hip[0] + math.sin(a) * 46 * s, hip[1] + math.cos(a) * 46 * s)
        foot = (knee[0] + math.sin(a - 0.25 * abs(sw)) * 46 * s, knee[1] + 46 * s)
        d.line([hip, knee, foot], fill=c, width=int(15 * s), joint="curve")
    d.rounded_rectangle([x - 20 * s, y - 160 * s, x + 20 * s, y - 86 * s], 14 * s, fill=c)
    if pack:
        d.rounded_rectangle([x - 40 * s, y - 156 * s, x - 12 * s, y - 100 * s], 8 * s, fill=c)
    if vest:
        d.rectangle([x - 20 * s, y - 128 * s, x + 20 * s, y - 120 * s], fill=vest)
        d.rectangle([x - 20 * s, y - 108 * s, x + 20 * s, y - 100 * s], fill=vest)
    d.ellipse([x - 17 * s, y - 196 * s, x + 17 * s, y - 162 * s], fill=c)
    if helmet:
        d.chord([x - 22 * s, y - 202 * s, x + 22 * s, y - 166 * s], 180, 360, fill=c)
        d.rectangle([x - 24 * s, y - 185 * s, x + 24 * s, y - 181 * s], fill=c)
    hand = None
    for sgn in (1, -1):
        sh = (x, y - 150 * s)
        if device and sgn == 1:
            el = (x + 26 * s, y - 120 * s)
            hand = (x + 34 * s, y - 146 * s) if not arm_up else (x + 30 * s, y - 196 * s)
            d.line([sh, el, hand], fill=c, width=int(12 * s), joint="curve")
        else:
            a = -0.45 * sw * sgn
            el = (sh[0] + math.sin(a) * 34 * s, sh[1] + 34 * s)
            hd = (el[0] + math.sin(a + 0.2) * 32 * s, el[1] + 30 * s)
            d.line([sh, el, hd], fill=c, width=int(12 * s), joint="curve")
    return hand


def device_glow(img, xy, s=1.0, a=1.0, color=PALE):
    x, y = xy
    g = Image.new("RGBA", SZ, (0, 0, 0, 0))
    ImageDraw.Draw(g).ellipse([x - 60 * s, y - 60 * s, x + 60 * s, y + 60 * s], fill=color + (int(150 * a),))
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(26 * s)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x - 9 * s, y - 13 * s, x + 9 * s, y + 13 * s], 3 * s, fill=(20, 24, 22, 255))
    d.rectangle([x - 6 * s, y - 10 * s, x + 6 * s, y - 2 * s], fill=color + (int(255 * a),))


def rings(img, xy, t, color=MINT, r0=20, r1=260, period=1.2, n=3, width=3, alpha=170):
    d = ImageDraw.Draw(img)
    x, y = xy
    for k in range(n):
        age = (t + k * period / n) % period / period
        r = r0 + (r1 - r0) * eout(age)
        a = int(alpha * (1 - age))
        d.ellipse([x - r, y - r, x + r, y + r], outline=color + (a,), width=width)


def bubble(img, xy, text, a, fs=34, color=(255, 255, 255), bg=(0x2F, 0x6D, 0x4F), tail="down"):
    if a <= 0:
        return
    f = font("SemiBold", fs)
    layer = Image.new("RGBA", SZ, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    tw = d.textlength(text, font=f)
    x, y = xy
    w, h = tw + 44, fs + 32
    d.rounded_rectangle([x - w / 2, y - h, x + w / 2, y], 18, fill=bg + (int(240 * a),))
    if tail == "down":
        d.polygon([(x - 14, y - 1), (x + 14, y - 1), (x, y + 16)], fill=bg + (int(240 * a),))
    d.text((x, y - h / 2), text, font=f, fill=color + (int(255 * a),), anchor="mm")
    img.alpha_composite(layer)


def chip(img, xy, text, a, fs=30, icon_red=False):
    if a <= 0:
        return
    f = font("SemiBold", fs)
    layer = Image.new("RGBA", SZ, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    tw = d.textlength(text, font=f)
    x, y = xy
    d.rounded_rectangle([x, y, x + tw + 96, y + fs + 30], (fs + 30) // 2, fill=(12, 14, 14, int(220 * a)),
                        outline=(255, 255, 255, int(60 * a)), width=2)
    cx, cy = x + 34, y + (fs + 30) / 2
    for i in range(4):
        bx = cx - 14 + i * 8
        d.rectangle([bx, cy + 10 - i * 6, bx + 5, cy + 10], outline=(200, 200, 200, int(255 * a)), width=2)
    if icon_red:
        d.line([cx - 18, cy - 14, cx + 18, cy + 14], fill=RED + (int(255 * a),), width=4)
    d.text((x + 66, cy), text, font=f, fill=(240, 240, 240, int(255 * a)), anchor="lm")
    img.alpha_composite(layer)


def finish(fr, p, sat=1.0, dark=1.0):
    arr = np.asarray(fr.convert("RGB"), np.float32)
    if sat != 1.0:
        g = arr.mean(2, keepdims=True)
        arr = g + (arr - g) * sat
    arr *= dark
    # vignette
    if not hasattr(finish, "vig"):
        yy, xx = np.mgrid[0:1080, 0:1920].astype(np.float32)
        dd = np.sqrt(((xx - 960) / 1100) ** 2 + ((yy - 540) / 750) ** 2)
        finish.vig = np.clip(1.15 - 0.45 * dd, 0.55, 1.0)[..., None]
    arr *= finish.vig
    p.stdin.write(np.clip(arr, 0, 255).astype(np.uint8).tobytes())


def pan(layers, t, speeds):
    """layers wider than canvas; return composite shifted by speed*t."""
    out = Image.new("RGBA", SZ)
    for im, sp in zip(layers, speeds):
        off = int(sp * t) % max(1, im.width - 1920) if im.width > 1920 else 0
        out.alpha_composite(im.crop((off, 0, off + 1920, 1080)))
    return out


# ---------------------------------------------------------------- scenes
def trail(path, secs, day=False):
    sky = gradient((26, 36, 52), (196, 120, 84)) if not day else gradient((120, 170, 200), (230, 214, 170))
    w = 2600
    far = ridge(w, 640, 120, 1, color=(64, 62, 84) if not day else (120, 140, 160), h=1080)
    mid = ridge(w, 760, 90, 2, color=(40, 40, 54) if not day else (78, 100, 92), h=1080)
    near = ridge(w, 900, 40, 3, rough=0.4, color=(16, 18, 22) if not day else (40, 56, 44), h=1080)
    sun = Image.new("RGBA", SZ, (0, 0, 0, 0))
    ImageDraw.Draw(sun).ellipse([1240, 420, 1420, 600], fill=(255, 200, 140, 200) if not day else (255, 250, 220, 230))
    sun = sun.filter(ImageFilter.GaussianBlur(6))
    p = writer(path)
    for fno in range(int(secs * FPS)):
        t = fno / FPS
        fr = sky.copy()
        fr.alpha_composite(sun)
        base = pan([far, mid], t, [6, 14])
        fr.alpha_composite(base)
        off = int(30 * t)
        nr = near.crop((off, 0, off + 1920, 1080))
        fr.alpha_composite(nr)
        d = ImageDraw.Draw(fr)
        walkers = [(780, 0.0), (1010, 1.7)] if not day else [(600, 0.0), (900, 1.2), (1250, 2.1)]
        heads = []
        for x0, ph in walkers:
            x = x0 + 18 * t
            y = ground_y(nr, x) + 4
            figure(d, x, y, 1.15, phase=t * 5.5 + ph, color=(10, 11, 14, 255))
            heads.append((x, y - 240))
        if not day:
            chip(fr, (1380, 120), "No Service", ease((t - 1.0) / 0.4), icon_red=True)
            if 2.0 < t:
                bubble(fr, (heads[0][0], heads[0][1] - 10), "Call failed", ease((t - 2.2) / 0.3) * (1 - ease((t - 6.0) / 0.3)),
                       bg=(60, 20, 20))
        else:
            fn = font("SemiBold", 28)
            for k, (hx, hy) in enumerate(heads):
                a = ease((t - 0.6 - 0.4 * k) / 0.4)
                lab = ["Kasun · 120 m", "Amaya · 60 m", "You"][k]
                bubble(fr, (hx, hy - 10), lab, a, fs=26, bg=GREEN)
        finish(fr, p, sat=0.8 if not day else 1.0)
    p.stdin.close()
    p.wait()


def collapse(path, secs):
    sky = gradient((10, 12, 18), (30, 30, 36))
    slabs = Image.new("RGBA", SZ, (0, 0, 0, 0))
    d = ImageDraw.Draw(slabs)
    r = np.random.default_rng(4)
    # standing broken wall left
    d.polygon([(120, 1080), (120, 380), (260, 330), (330, 420), (420, 360), (440, 1080)], fill=(46, 46, 52, 255))
    for k in range(5):
        for j in range(3):
            d.rectangle([150 + j * 90, 430 + k * 110, 210 + j * 90, 490 + k * 110], fill=(20, 20, 24, 255))
    # rubble pile
    for k in range(70):
        cx, cy = r.uniform(300, 1900), r.uniform(700, 1080)
        if cy < 760 + 120 * math.sin(cx / 300):
            continue
        w_, h_ = r.uniform(60, 220), r.uniform(20, 70)
        ang = r.uniform(-0.6, 0.6)
        pts = [(-w_ / 2, -h_ / 2), (w_ / 2, -h_ / 2), (w_ / 2, h_ / 2), (-w_ / 2, h_ / 2)]
        pts = [(cx + x * math.cos(ang) - y * math.sin(ang), cy + x * math.sin(ang) + y * math.cos(ang)) for x, y in pts]
        g = int(r.uniform(40, 78))
        d.polygon(pts, fill=(g, g, g + 4, 255), outline=(g + 18, g + 18, g + 20, 255))
    # big slab over the pocket
    d.polygon([(780, 790), (1500, 690), (1520, 740), (800, 850)], fill=(70, 70, 76, 255), outline=(96, 96, 100, 255))
    for x in range(820, 1480, 60):
        d.line([x, 830 - (x - 800) * 0.14, x + 16, 790 - (x - 800) * 0.14], fill=(40, 40, 44, 255), width=4)
    pocket = Image.new("RGBA", SZ, (0, 0, 0, 0))
    ImageDraw.Draw(pocket).polygon([(840, 860), (1440, 760), (1460, 930), (860, 960)], fill=(6, 6, 8, 255))
    dust = [(r.uniform(0, 1920), r.uniform(0, 1080), r.uniform(10, 40), r.uniform(1, 3)) for _ in range(260)]
    p = writer(path)
    for fno in range(int(secs * FPS)):
        t = fno / FPS
        fr = sky.copy()
        fr.alpha_composite(slabs)
        fr.alpha_composite(pocket)
        d = ImageDraw.Draw(fr)
        figure(d, 1150, 935, 1.0, lie=True, color=(92, 98, 108, 255))
        flick = 1.0 if (t % 1.7) > 0.12 else 0.4
        # phone glow on the survivor's hand
        g = Image.new("RGBA", SZ, (0, 0, 0, 0))
        ImageDraw.Draw(g).ellipse([1010, 800, 1150, 940], fill=(140, 170, 200, int(120 * flick)))
        fr.alpha_composite(g.filter(ImageFilter.GaussianBlur(30)))
        d.rounded_rectangle([1066, 846, 1100, 900], 6, fill=(160, 190, 220, int(255 * flick)))
        # dust
        dl = Image.new("RGBA", SZ, (0, 0, 0, 0))
        dd = ImageDraw.Draw(dl)
        for x, y, v, s_ in dust:
            yy = (y + v * t) % 1080
            dd.ellipse([x, yy, x + s_, yy + s_], fill=(200, 196, 186, 90))
        fr.alpha_composite(dl)
        chip(fr, (1380, 120), "No signal", ease((t - 1.0) / 0.4), icon_red=True)
        bubble(fr, (1083, 820), "Calling…  failed", ease((t - 2.6) / 0.3), fs=28, bg=(60, 20, 20))
        k = 1.0 + 0.05 * ease(t / secs)
        cw, ch = 1920 / k, 1080 / k
        fr = fr.resize(SZ, Image.BILINEAR, box=((1920 - cw) * 0.55, (1080 - ch) * 0.7, (1920 - cw) * 0.55 + cw, (1080 - ch) * 0.7 + ch))
        finish(fr, p, sat=0.5, dark=0.9)
    p.stdin.close()
    p.wait()


def load_dev(h):
    dev = Image.open(os.path.join(W, "build/cut/IMG_9657.png")).convert("RGBA")
    return dev.resize((round(dev.width * h / dev.height), h), Image.LANCZOS)


def rangescene(path, secs):
    sky = gradient((16, 22, 30), (34, 44, 46))
    land = ridge(1920, 860, 14, 9, rough=0.3, color=(20, 26, 24))
    dev = load_dev(230)
    f_big = font("ExtraBold", 64)
    f_s = font("Medium", 28)
    p = writer(path)
    xa, xb = 300, 1620
    for fno in range(int(secs * FPS)):
        t = fno / FPS
        fr = sky.copy()
        fr.alpha_composite(land)
        d = ImageDraw.Draw(fr)
        # stars
        if not hasattr(rangescene, "stars"):
            rangescene.stars = [(rng.uniform(0, 1920), rng.uniform(0, 600), rng.uniform(1, 2.5)) for _ in range(160)]
        for x, y, s in rangescene.stars:
            d.ellipse([x, y, x + s, y + s], fill=(220, 230, 230, 140))
        for x in (xa, xb):
            fr.alpha_composite(dev, (int(x - dev.width / 2), 860 - dev.height + 30))
        u = ease((t - 1.0) / 4.5)
        # wave front travelling from A to B
        for k in range(8):
            rr = (t * 420 + k * 170) % 1500
            if rr < u * 1350 + 60:
                a = int(150 * (1 - rr / 1500))
                d.arc([xa + 60 - rr, 640 - rr * 0.55, xa + 60 + rr, 640 + rr * 0.55], -40, 40, fill=MINT + (a,), width=4)
        # distance bar
        y0 = 960
        d.line([xa, y0, xb, y0], fill=(255, 255, 255, 50), width=4)
        xe = xa + (xb - xa) * u
        d.line([xa, y0, xe, y0], fill=MINT + (255,), width=6)
        d.ellipse([xe - 10, y0 - 10, xe + 10, y0 + 10], fill=PALE + (255,))
        km = 8.0 * u
        d.text(((xa + xe) / 2, y0 - 44), f"{km:.1f} km", font=f_big if u >= 0.999 else font("Bold", 48),
               fill=(242, 244, 241, 255), anchor="ms")
        if u >= 0.999:
            d.text((960, y0 + 54), "open line of sight · maker rating", font=f_s, fill=(180, 192, 185, 255), anchor="ms")
        finish(fr, p)
    p.stdin.close()
    p.wait()


def contour_map(seed=0, tint=(0x3F, 0x8F, 0x68), alpha=40):
    h, w = 1080, 1920
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32) / 240.0
    f = (np.sin(xx * 1.1 + np.sin(yy * 0.8 + seed) * 1.7) + np.cos(yy * 1.3 - np.sin(xx * 0.6) * 2.0)
         + 0.5 * np.sin((xx - yy) * 2.1 + seed))
    band = np.abs(((f * 3.0) % 1.0) - 0.5)
    img = np.zeros((h, w, 4), np.uint8)
    img[..., :3] = tint
    img[..., 3] = ((band > 0.47) * alpha).astype(np.uint8)
    return Image.fromarray(img, "RGBA")


def mesh(path, secs):
    bg = gradient((14, 18, 16), (24, 30, 27))
    bg.alpha_composite(contour_map(1))
    # river
    rv = Image.new("RGBA", SZ, (0, 0, 0, 0))
    ImageDraw.Draw(rv).line([(0, 300), (300, 420), (640, 380), (900, 560), (1300, 520), (1600, 760), (1920, 820)],
                            fill=(40, 80, 110, 120), width=18, joint="curve")
    bg.alpha_composite(rv.filter(ImageFilter.GaussianBlur(3)))
    chain = [(170, 820), (420, 640), (690, 760), (930, 520), (1190, 650), (1430, 430), (1700, 300)]
    extra = [(560, 900), (820, 330), (1090, 860), (1350, 220), (1600, 620), (300, 420)]
    nodes = chain + extra
    links = [(i, i + 1) for i in range(len(chain) - 1)] + [(1, 7), (2, 7), (3, 8), (4, 9), (4, 8), (5, 10), (6, 11), (5, 11),
                                                          (0, 12), (1, 12), (3, 9)]
    R = 250  # 8 km on the drawn scale
    f_lab = font("SemiBold", 26)
    f_big = font("ExtraBold", 56)
    p = writer(path)
    n_chain = len(chain)
    for fno in range(int(secs * FPS)):
        t = fno / FPS
        fr = bg.copy()
        ov = Image.new("RGBA", SZ, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        appear = [0.4 + 0.75 * i for i in range(n_chain)] + [6.0 + 0.3 * k for k in range(len(extra))]
        # range circles
        for i, (x, y) in enumerate(nodes):
            a = ease((t - appear[i]) / 0.5)
            if a > 0:
                d.ellipse([x - R, y - R, x + R, y + R], fill=(0x2F, 0x6D, 0x4F, int(22 * a)),
                          outline=(0x7C, 0xC4, 0xA0, int(70 * a)), width=2)
        for i, j in links:
            a = ease((t - max(appear[i], appear[j]) - 0.2) / 0.4)
            if a > 0:
                d.line([nodes[i], nodes[j]], fill=(0x8F, 0xD8, 0xB0, int(150 * a)), width=3)
        fr.alpha_composite(ov)
        d = ImageDraw.Draw(fr)
        for i, (x, y) in enumerate(nodes):
            a = ease((t - appear[i]) / 0.4)
            if a <= 0:
                continue
            r_ = 13 + 3 * (1 - a)
            d.ellipse([x - 26, y - 26, x + 26, y + 26], fill=(0x2F, 0x6D, 0x4F, int(120 * a)))
            d.ellipse([x - r_, y - r_, x + r_, y + r_], fill=(230, 245, 236, int(255 * a)))
        # message pulse along the chain, repeating after the chain is built
        if t > 6.0:
            u = ((t - 6.0) / 4.5) % 1.0
            seg = u * (n_chain - 1)
            i = int(seg)
            fpart = seg - i
            (x0, y0), (x1, y1) = chain[i], chain[min(i + 1, n_chain - 1)]
            x, y = x0 + (x1 - x0) * fpart, y0 + (y1 - y0) * fpart
            gl = Image.new("RGBA", SZ, (0, 0, 0, 0))
            ImageDraw.Draw(gl).ellipse([x - 40, y - 40, x + 40, y + 40], fill=(191, 240, 212, 200))
            fr.alpha_composite(gl.filter(ImageFilter.GaussianBlur(14)))
            ImageDraw.Draw(fr).ellipse([x - 12, y - 12, x + 12, y + 12], fill=(255, 255, 255, 255))
        d = ImageDraw.Draw(fr)
        # scale bar
        d.line([120, 1010, 120 + R, 1010], fill=(230, 236, 232, 255), width=4)
        for xx in (120, 120 + R):
            d.line([xx, 998, xx, 1022], fill=(230, 236, 232, 255), width=4)
        d.text((120 + R / 2, 990), "8 km", font=f_lab, fill=(230, 236, 232, 255), anchor="ms")
        # reach counter
        hops = sum(1 for i in range(1, n_chain) if t > appear[i])
        reach = 8 * (hops + 1) if t > appear[0] else 0
        d.text((1800, 1000), f"{reach} km" if reach else "", font=f_big, fill=(242, 244, 241, 255), anchor="rs")
        d.text((1800, 1032), "reach with relays (illustration)", font=font("Medium", 24), fill=(170, 184, 176, 255), anchor="rs")
        finish(fr, p)
    p.stdin.close()
    p.wait()


def desert(path, secs):
    sky = gradient((120, 160, 196), (236, 196, 140))
    w = 2400
    d1 = ridge(w, 700, 70, 21, rough=0.35, color=(206, 160, 104))
    d2 = ridge(w, 820, 60, 22, rough=0.3, color=(184, 136, 84))
    d3 = ridge(w, 960, 50, 23, rough=0.3, color=(150, 104, 62))
    sun = Image.new("RGBA", SZ, (0, 0, 0, 0))
    ImageDraw.Draw(sun).ellipse([1460, 120, 1640, 300], fill=(255, 246, 220, 255))
    sun = sun.filter(ImageFilter.GaussianBlur(10))
    p = writer(path)
    msg_t = 3.2
    for fno in range(int(secs * FPS)):
        t = fno / FPS
        fr = sky.copy()
        fr.alpha_composite(sun)
        fr.alpha_composite(pan([d1, d2], t, [5, 10]))
        off = int(16 * t)
        n3 = d3.crop((off, 0, off + 1920, 1080))
        fr.alpha_composite(n3)
        d = ImageDraw.Draw(fr)
        # far patrol member on the second dune line
        xa = 1480
        ya = ground_y(fr.crop((0, 0, 1920, 1080)), xa) if False else 0
        y_far = ground_y(pan([d2], t, [10]), xa)
        ha = figure(d, xa, y_far + 2, 0.55, walk=False, color=(70, 50, 32, 255), helmet=True, device=True)
        xb = 520
        yb = ground_y(n3, xb) + 4
        hb = figure(d, xb, yb, 1.3, phase=t * 4, walk=True, color=(40, 28, 18, 255), helmet=True, device=True)
        device_glow(fr, ha, 0.6, 0.9)
        device_glow(fr, hb, 1.2, 0.9)
        # signal arc between them
        if t > 1.2:
            u = ((t - 1.2) / 1.6) % 1.0
            for k in range(14):
                v = k / 13
                if v > u:
                    break
                x = hb[0] + (ha[0] - hb[0]) * v
                y = hb[1] + (ha[1] - hb[1]) * v - math.sin(math.pi * v) * 160
                ImageDraw.Draw(fr).ellipse([x - 5, y - 5, x + 5, y + 5], fill=(255, 255, 255, 200))
            rings(fr, ha, t, color=(255, 255, 255), r0=10, r1=110, alpha=150)
        bubble(fr, (ha[0], ha[1] - 60), "Copy. Moving to the ridge.", ease((t - msg_t) / 0.3), fs=28)
        # heat shimmer
        arr = np.asarray(fr).copy()
        rows = slice(680, 1080)
        shift = (np.sin(np.arange(400) / 7 + t * 8) * 2).astype(int)
        for i, s_ in enumerate(shift):
            if s_:
                arr[680 + i] = np.roll(arr[680 + i], s_, axis=0)
        fr = Image.fromarray(arr)
        finish(fr, p, sat=0.95)
    p.stdin.close()
    p.wait()


def rubble(path, secs):
    sky = gradient((22, 26, 34), (40, 42, 46))
    sec = Image.new("RGBA", SZ, (0, 0, 0, 0))
    d = ImageDraw.Draw(sec)
    # surface line at y=430; underground cross-section below
    d.rectangle([0, 430, 1920, 1080], fill=(34, 32, 32, 255))
    r = np.random.default_rng(7)
    for _ in range(120):
        cx, cy = r.uniform(0, 1920), r.uniform(440, 1080)
        w_, h_ = r.uniform(70, 240), r.uniform(26, 70)
        ang = r.uniform(-0.5, 0.5)
        pts = [(-w_ / 2, -h_ / 2), (w_ / 2, -h_ / 2), (w_ / 2, h_ / 2), (-w_ / 2, h_ / 2)]
        pts = [(cx + x * math.cos(ang) - y * math.sin(ang), cy + x * math.sin(ang) + y * math.cos(ang)) for x, y in pts]
        g = int(r.uniform(48, 84))
        d.polygon(pts, fill=(g, g - 2, g - 4, 255), outline=(g + 16, g + 14, g + 12, 255))
    # air pocket with survivor
    d.polygon([(760, 860), (1240, 800), (1280, 990), (780, 1010)], fill=(8, 8, 10, 255))
    d.line([(0, 430), (1920, 430)], fill=(120, 116, 110, 255), width=4)
    p = writer(path)
    for fno in range(int(secs * FPS)):
        t = fno / FPS
        fr = sky.copy()
        fr.alpha_composite(sec)
        d = ImageDraw.Draw(fr)
        figure(d, 1060, 985, 1.0, lie=True, color=(92, 98, 108, 255))
        dev_s = (1010, 900)
        # responders on the surface
        h1 = figure(d, 1180, 432, 1.0, walk=False, color=(12, 12, 14, 255), helmet=True, pack=False,
                    vest=(230, 210, 60, 255), device=True)
        figure(d, 1380, 432, 1.0, walk=False, color=(12, 12, 14, 255), helmet=True, pack=False, vest=(230, 210, 60, 255))
        # floodlight
        fl = Image.new("RGBA", SZ, (0, 0, 0, 0))
        ImageDraw.Draw(fl).polygon([(1600, 160), (900, 430), (1500, 430)], fill=(255, 250, 220, 40))
        fr.alpha_composite(fl.filter(ImageFilter.GaussianBlur(20)))
        device_glow(fr, dev_s, 1.0, 1.0)
        device_glow(fr, h1, 1.0, 1.0)
        # voice packets rising through the rubble
        if t > 1.0:
            for k in range(5):
                u = ((t - 1.0) * 0.6 + k / 5) % 1.0
                x = dev_s[0] + (h1[0] - dev_s[0]) * u + math.sin(u * 9) * 18
                y = dev_s[1] + (h1[1] - dev_s[1]) * u
                gl = Image.new("RGBA", SZ, (0, 0, 0, 0))
                ImageDraw.Draw(gl).ellipse([x - 16, y - 16, x + 16, y + 16], fill=PALE + (int(220 * math.sin(math.pi * u)),))
                fr.alpha_composite(gl.filter(ImageFilter.GaussianBlur(5)))
        # waveform bubble at responder
        a = ease((t - 2.0) / 0.3)
        if a > 0:
            layer = Image.new("RGBA", SZ, (0, 0, 0, 0))
            dl = ImageDraw.Draw(layer)
            bx, by = h1[0] - 360, h1[1] - 200
            dl.rounded_rectangle([bx, by, bx + 330, by + 96], 22, fill=(0x2F, 0x6D, 0x4F, int(235 * a)))
            for k in range(22):
                hh = 8 + 30 * abs(math.sin(k * 0.9 + t * 9)) * (0.5 + 0.5 * math.sin(k * 0.35))
                x = bx + 28 + k * 13
                dl.rounded_rectangle([x, by + 48 - hh / 2, x + 6, by + 48 + hh / 2], 3, fill=(255, 255, 255, int(255 * a)))
            fr.alpha_composite(layer)
        bubble(fr, (1010, 860), "I'm under the stairwell", ease((t - 1.4) / 0.3) * (1 - ease((t - 6.0) / 0.3)), fs=28)
        finish(fr, p, sat=0.8)
    p.stdin.close()
    p.wait()


def jungle(path, secs):
    sky = gradient((18, 40, 30), (40, 74, 52))
    r = np.random.default_rng(5)

    def leaves(n, ymin, ymax, col, smin, smax, seed):
        im = Image.new("RGBA", (2400, 1080), (0, 0, 0, 0))
        dd = ImageDraw.Draw(im)
        rr = np.random.default_rng(seed)
        for _ in range(n):
            x, y = rr.uniform(0, 2400), rr.uniform(ymin, ymax)
            s_ = rr.uniform(smin, smax)
            a = rr.uniform(0, math.pi)
            pts = []
            for k in range(16):
                th = k / 16 * 2 * math.pi
                rad = s_ * (0.35 + 0.65 * abs(math.cos(th)))
                pts.append((x + rad * math.cos(th + a), y + rad * 0.45 * math.sin(th + a)))
            dd.polygon(pts, fill=col)
        for _ in range(n // 8):
            x = rr.uniform(0, 2400)
            dd.rectangle([x, ymin - 200, x + rr.uniform(14, 40), 1080], fill=col)
        return im

    back = leaves(260, 0, 1080, (30, 60, 42, 255), 40, 110, 1)
    mid = leaves(200, 100, 1080, (18, 40, 28, 255), 60, 150, 2)
    front = leaves(70, 700, 1080, (8, 18, 12, 255), 120, 260, 3)
    p = writer(path)
    team = (1640, 300)
    for fno in range(int(secs * FPS)):
        t = fno / FPS
        fr = sky.copy()
        # light shafts
        ls = Image.new("RGBA", SZ, (0, 0, 0, 0))
        ImageDraw.Draw(ls).polygon([(700, 0), (900, 0), (1200, 1080), (900, 1080)], fill=(220, 255, 220, 26))
        fr.alpha_composite(ls.filter(ImageFilter.GaussianBlur(30)))
        fr.alpha_composite(pan([back, mid], t, [6, 12]))
        off = int(24 * t)
        fr.alpha_composite(front.crop((off, 0, off + 1920, 1080)))
        rim = Image.new("RGBA", SZ, (0, 0, 0, 0))
        figure(ImageDraw.Draw(rim), 560, 900, 1.25, walk=False, color=(150, 210, 170, 255), device=True, arm_up=True)
        fr.alpha_composite(rim.filter(ImageFilter.GaussianBlur(5)))
        d = ImageDraw.Draw(fr)
        h = figure(d, 560, 900, 1.25, walk=False, color=(10, 20, 14, 255), device=True, arm_up=True)
        device_glow(fr, h, 1.1, 1.0)
        # hops through the canopy to the team marker
        hops = [h, (820, 560), (1100, 640), (1360, 420), team]
        dd = ImageDraw.Draw(fr)
        for i, (x, y) in enumerate(hops[1:-1], 1):
            a = ease((t - 0.8 - 0.6 * i) / 0.3)
            if a > 0:
                dd.ellipse([x - 12, y - 12, x + 12, y + 12], fill=PALE + (int(255 * a),))
                rings(fr, (x, y), t + i, color=PALE, r0=14, r1=70, alpha=int(120 * a))
        for i in range(len(hops) - 1):
            a = ease((t - 0.8 - 0.6 * (i + 1)) / 0.3)
            if a > 0:
                dd.line([hops[i], hops[i + 1]], fill=PALE + (int(150 * a),), width=3)
        # team marker
        ta = ease((t - 3.4) / 0.3)
        if ta > 0:
            tx, ty = team
            dd.ellipse([tx - 30, ty - 30, tx + 30, ty + 30], fill=(0x2F, 0x6D, 0x4F, int(240 * ta)), outline=(255, 255, 255, int(255 * ta)), width=3)
            dd.text((tx, ty + 60), "Search team", font=font("SemiBold", 28), fill=(255, 255, 255, int(255 * ta)), anchor="ms")
        bubble(fr, (h[0], h[1] - 70), "SOS · location shared", ease((t - 0.6) / 0.3), fs=28, bg=RED)
        bubble(fr, (team[0], team[1] - 50), "Got you. Stay put.", ease((t - 4.6) / 0.3), fs=28)
        finish(fr, p, sat=0.9)
    p.stdin.close()
    p.wait()


SCENES = {
    "trail": lambda: trail(f"{OUT}/sc_trail.mp4", 9.0),
    "collapse": lambda: collapse(f"{OUT}/sc_collapse.mp4", 9.0),
    "range": lambda: rangescene(f"{OUT}/sc_range.mp4", 13.0),
    "mesh": lambda: mesh(f"{OUT}/sc_mesh.mp4", 16.0),
    "desert": lambda: desert(f"{OUT}/sc_desert.mp4", 9.0),
    "rubble": lambda: rubble(f"{OUT}/sc_rubble.mp4", 8.0),
    "jungle": lambda: jungle(f"{OUT}/sc_jungle.mp4", 8.0),
    "trail_day": lambda: trail(f"{OUT}/sc_trail_day.mp4", 5.0, day=True),
}

if __name__ == "__main__":
    for k in sys.argv[1:]:
        SCENES[k]()
        print("done", k, flush=True)
