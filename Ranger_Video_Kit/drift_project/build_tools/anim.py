"""Frame-rendered motion pieces, piped to ffmpeg: hook, network, wifi link."""
import math
import os
import subprocess
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(W, "build/assets")
FONT = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
FPS = 30


def font(weight, size):
    return ImageFont.truetype(FONT.format(weight), size)


def ease(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def ease_out(t):
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3


def writer(path, size, alpha=False):
    w, h = size
    if alpha:
        args = ["-c:v", "ffv1", "-pix_fmt", "yuva420p", path]
        pix = "rgba"
    else:
        args = ["-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", path]
        pix = "rgb24"
    return subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", pix,
                             "-s", f"{w}x{h}", "-r", str(FPS), "-i", "-"] + args, stdin=subprocess.PIPE)


# ---------------------------------------------------------------- hook
def phone_layer(dim):
    """A phone at 420x860 showing No Service. dim scales screen brightness."""
    w, h = 460, 900
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([20, 20, w - 20, h - 20], 70, fill=(10, 12, 12, 255), outline=(60, 66, 64, 255), width=3)
    sx0, sy0, sx1, sy1 = 36, 36, w - 36, h - 36
    g = int(26 * dim)
    d.rounded_rectangle([sx0, sy0, sx1, sy1], 56, fill=(g, g + 3, g + 4, 255))
    d.rounded_rectangle([w // 2 - 34, 52, w // 2 + 54, 84], 16, fill=(0, 0, 0, 255))
    c = int(225 * dim)
    col = (c, c, c, 255)
    d.text((64, 56), "No Service", font=font("SemiBold", 22), fill=col)
    # empty signal bars
    for i in range(4):
        x = 330 + i * 12
        d.rectangle([x, 80 - 6 - i * 5, x + 7, 80], outline=(int(c * .6),) * 3 + (255,), width=2)
    d.rounded_rectangle([382, 62, 414, 80], 4, outline=col, width=2)
    d.rectangle([386, 66, 392, 76], fill=(int(220 * dim), 60, 50, 255))
    # big no-signal glyph
    cx, cy = w // 2, 400
    gc = (int(200 * dim),) * 3 + (255,)
    for r in (60, 105, 150):
        d.arc([cx - r, cy - r, cx + r, cy + r], 225, 315, fill=gc, width=12)
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=gc)
    red = (int(190 * dim + 20), int(48 * dim), int(40 * dim), 255)
    d.line([cx - 130, cy - 170, cx + 130, cy + 40], fill=red, width=14)
    d.text((cx, 520), "No connection", font=font("SemiBold", 40), fill=col, anchor="mm")
    d.text((cx, 570), "SOS only", font=font("Medium", 28), fill=(int(c * .7),) * 3 + (255,), anchor="mm")
    return im


def hook(path, secs=10.0):
    size = (1920, 1080)
    rng = np.random.default_rng(7)
    n = 520
    drops = np.stack([rng.uniform(-300, 2200, n), rng.uniform(-1100, 1080, n),
                      rng.uniform(26, 48, n), rng.uniform(40, 90, n), rng.uniform(0.15, 0.5, n)], 1)
    base = np.zeros((1080, 1920, 3), np.float32)
    yy, xx = np.mgrid[0:1080, 0:1920].astype(np.float32)
    d = np.sqrt(((xx - 1250) / 1300) ** 2 + ((yy - 520) / 900) ** 2)
    t = np.clip(d, 0, 1)[..., None]
    base = np.array([20, 26, 30], np.float32) * (1 - t) + np.array([5, 7, 8], np.float32) * t
    bg = Image.fromarray(base.astype(np.uint8)).convert("RGBA")
    p = writer(path, size)
    frames = int(secs * FPS)
    for f in range(frames):
        s = f / FPS
        # flicker / blackout envelope
        dim = 1.0
        for t0, dur, depth in ((2.2, 0.12, 0.6), (5.1, 0.08, 0.8), (6.6, 0.35, 0.95), (7.1, 0.1, 0.5), (8.7, 0.6, 1.0)):
            if t0 <= s < t0 + dur:
                dim = 1 - depth
        if s > 9.2:
            dim = max(0.0, 1 - (s - 9.2) / 0.5) * 0.5
        fr = bg.copy()
        ph = phone_layer(max(dim, 0.05))
        # glow from the screen onto the room
        glow = Image.new("RGBA", size, (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        gd.ellipse([1020, 160, 1660, 960], fill=(60, 80, 90, int(70 * dim)))
        glow = glow.filter(ImageFilter.GaussianBlur(120))
        fr = Image.alpha_composite(fr, glow)
        fr.alpha_composite(ph, (1110, 90))
        # rain
        rain = Image.new("RGBA", size, (0, 0, 0, 0))
        rd = ImageDraw.Draw(rain)
        for x, y, v, ln, a in drops:
            yy0 = (y + v * f) % 2200 - 1100
            xx0 = x - 0.25 * (v * f % 2200)
            rd.line([xx0, yy0, xx0 - ln * 0.25, yy0 + ln], fill=(170, 185, 190, int(255 * a * (0.5 + 0.5 * dim))), width=2)
        fr = Image.alpha_composite(fr, rain)
        # push-in 1.0 -> 1.08
        k = 1 + 0.08 * ease(s / secs)
        cw, ch = 1920 / k, 1080 / k
        x0, y0 = (1920 - cw) * 0.6, (1080 - ch) / 2
        fr = fr.resize(size, Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))
        arr = np.asarray(fr.convert("RGB"), np.float32)
        gray = arr.mean(2, keepdims=True)
        arr = gray + (arr - gray) * 0.35  # desaturate
        arr *= 0.35 + 0.65 * max(dim, 0.15) if s < 9.2 else 0.35 + 0.65 * dim
        p.stdin.write(np.clip(arr, 0, 255).astype(np.uint8).tobytes())
    p.stdin.close()
    p.wait()


# ---------------------------------------------------------------- network
def contour_map():
    h, w = 1080, 1920
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32) / 260.0
    f = (np.sin(xx * 1.3 + np.sin(yy * 0.7) * 1.6) + np.cos(yy * 1.1 - np.sin(xx * 0.5) * 2.0)
         + 0.5 * np.sin((xx + yy) * 2.3))
    band = np.abs(((f * 3.0) % 1.0) - 0.5)
    lines = (band > 0.47).astype(np.float32)
    img = np.zeros((h, w, 4), np.uint8)
    img[..., 0], img[..., 1], img[..., 2] = 0x3F, 0x8F, 0x68
    img[..., 3] = (lines * 38).astype(np.uint8)
    m = Image.fromarray(img, "RGBA").filter(ImageFilter.GaussianBlur(0.8))
    # fade the map toward the left (text side)
    fade = np.clip((np.arange(w) - 500) / 500, 0.25, 1.0)
    a = np.asarray(m.getchannel("A"), np.float32) * fade[None, :]
    m.putalpha(Image.fromarray(a.astype(np.uint8)))
    return m


def lock_icon(size=56):
    im = Image.new("RGBA", (size * 2, size * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = size
    d.ellipse([0, 0, size * 2 - 1, size * 2 - 1], fill=(0x2F, 0x6D, 0x4F, 255), outline=(0x8F, 0xD8, 0xB0, 255), width=4)
    d.rounded_rectangle([c - 22, c - 4, c + 22, c + 30], 6, fill=(255, 255, 255, 255))
    d.arc([c - 15, c - 30, c + 15, c + 6], 180, 360, fill=(255, 255, 255, 255), width=7)
    d.line([c - 15, c - 12, c - 15, c - 2], fill=(255, 255, 255, 255), width=7)
    d.line([c + 15, c - 12, c + 15, c - 2], fill=(255, 255, 255, 255), width=7)
    d.ellipse([c - 5, c + 6, c + 5, c + 16], fill=(0x2F, 0x6D, 0x4F, 255))
    return im.resize((size, size), Image.LANCZOS)


def network(path, secs=12.0):
    size = (1920, 1080)
    bg = Image.open(f"{A}/bg.png").convert("RGBA")
    cmap = contour_map()
    dev = Image.open(os.path.join(W, "build/cut/IMG_9657.png")).convert("RGBA")
    dev = dev.resize((round(dev.width * 200 / dev.height), 200), Image.LANCZOS)
    nodes = [(840, 800), (1250, 330), (1690, 770)]
    names = ["Ranger 1", "Ranger 2", "Ranger 3"]
    lock = lock_icon(64)
    f_lab = font("Medium", 28)
    f_tag = font("SemiBold", 26)
    # (start, from, to)
    hops = [(1.6, 0, 1), (3.7, 1, 2), (6.6, 2, 1), (8.7, 1, 0)]
    hop_d = 1.5
    p = writer(path, size)
    for fno in range(int(secs * FPS)):
        s = fno / FPS
        fr = bg.copy()
        cm = cmap.copy()
        cm.putalpha(cm.getchannel("A").point(lambda v: int(v * ease(s / 1.0))))
        fr = Image.alpha_composite(fr, cm)
        ov = Image.new("RGBA", size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        # links
        la = ease((s - 1.0) / 0.6)
        for i, j in ((0, 1), (1, 2)):
            (x0, y0), (x1, y1) = nodes[i], nodes[j]
            n = 26
            for k in range(n):
                if k % 2:
                    continue
                a0, a1 = k / n, (k + 1) / n
                d.line([x0 + (x1 - x0) * a0, y0 + (y1 - y0) * a0, x0 + (x1 - x0) * a1, y0 + (y1 - y0) * a1],
                       fill=(0x6F, 0xB8, 0x92, int(110 * la)), width=3)
        # rings: emitted at each hop start, from the sender
        for t0, i, j in hops:
            for r_off in (0.0, 0.35, 0.7):
                age = s - t0 - r_off
                if 0 <= age < 1.4:
                    r = 40 + 330 * ease_out(age / 1.4)
                    a = int(150 * (1 - age / 1.4))
                    x, y = nodes[i]
                    d.ellipse([x - r, y - r, x + r, y + r], outline=(0x8F, 0xD8, 0xB0, a), width=3)
            # arrival flash on receiver
            age = s - (t0 + hop_d)
            if 0 <= age < 0.8:
                r = 60 + 90 * ease_out(age / 0.8)
                x, y = nodes[j]
                d.ellipse([x - r, y - r, x + r, y + r], outline=(255, 255, 255, int(200 * (1 - age / 0.8))), width=4)
        fr = Image.alpha_composite(fr, ov)
        # nodes
        for k, (x, y) in enumerate(nodes):
            a = ease((s - 0.3 - 0.2 * k) / 0.5)
            if a <= 0:
                continue
            sc = 0.9 + 0.1 * a
            dv = dev.resize((max(1, int(dev.width * sc)), max(1, int(dev.height * sc))), Image.LANCZOS)
            dv.putalpha(dv.getchannel("A").point(lambda v: int(v * a)))
            halo = Image.new("RGBA", size, (0, 0, 0, 0))
            ImageDraw.Draw(halo).ellipse([x - 120, y - 120, x + 120, y + 120], fill=(0x2F, 0x6D, 0x4F, int(90 * a)))
            fr = Image.alpha_composite(fr, halo.filter(ImageFilter.GaussianBlur(40)))
            fr.alpha_composite(dv, (int(x - dv.width / 2), int(y - dv.height / 2)))
            ImageDraw.Draw(fr).text((x, y + 128), names[k], font=f_lab, fill=(0xC9, 0xD3, 0xCD, int(255 * a)), anchor="mm")
        # packet
        for t0, i, j in hops:
            u = (s - t0) / hop_d
            if 0 <= u <= 1:
                e = ease(u)
                (x0, y0), (x1, y1) = nodes[i], nodes[j]
                x, y = x0 + (x1 - x0) * e, y0 + (y1 - y0) * e - math.sin(math.pi * e) * 40
                fr.alpha_composite(lock, (int(x - 32), int(y - 32)))
        # tags
        dd = ImageDraw.Draw(fr)
        for t0, t1, txt, (x, y) in ((3.2, 6.4, "Relayed", (1250, 200)), (5.2, 8.4, "Delivered", (1690, 640)),
                                    (8.2, 12.0, "Relayed", (1250, 200)), (10.2, 12.0, "Delivered", (840, 670))):
            a = ease((s - t0) / 0.3) * (1 - ease((s - (t1 - 0.3)) / 0.3))
            if a > 0:
                tw = dd.textlength(txt, font=f_tag)
                box = Image.new("RGBA", size, (0, 0, 0, 0))
                bd = ImageDraw.Draw(box)
                bd.rounded_rectangle([x - tw / 2 - 20, y - 24, x + tw / 2 + 20, y + 24], 24, fill=(0x2F, 0x6D, 0x4F, int(235 * a)))
                bd.text((x, y), txt, font=f_tag, fill=(255, 255, 255, int(255 * a)), anchor="mm")
                fr = Image.alpha_composite(fr, box)
        p.stdin.write(np.asarray(fr.convert("RGB")).tobytes())
    p.stdin.close()
    p.wait()


# ---------------------------------------------------------------- wifi link
def wifi_link(path, secs=26.0):
    w, h = 520, 200
    p = writer(path, (w, h), alpha=True)
    for fno in range(int(secs * FPS)):
        s = fno / FPS
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        y = 150
        for k in range(0, w, 22):
            d.ellipse([k + 4, y - 3, k + 10, y + 3], fill=(0x8F, 0xD8, 0xB0, 90))
        for k in range(3):
            u = ((s * 0.6 + k / 3) % 1.0)
            x = 10 + u * (w - 20)
            a = int(255 * math.sin(math.pi * u))
            d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=(0xBF, 0xF0, 0xD4, a))
        cx, cy = w // 2, 104
        for i, r in enumerate((26, 50, 74)):
            ph = (s * 1.2 - i * 0.22) % 1.2
            a = int(255 * (0.35 + 0.65 * max(0.0, 1 - ph / 0.6)))
            d.arc([cx - r, cy - r, cx + r, cy + r], 225, 315, fill=(0xBF, 0xF0, 0xD4, a), width=9)
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(0xBF, 0xF0, 0xD4, 255))
        p.stdin.write(np.asarray(im).tobytes())
    p.stdin.close()
    p.wait()


if __name__ == "__main__":
    which = sys.argv[1]
    if which == "hook":
        hook(f"{A}/hook.mp4")
    elif which == "network":
        network(f"{A}/network.mp4")
    elif which == "wifi":
        wifi_link(f"{A}/wifi_link.mkv")
