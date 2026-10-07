"""Graphics for the Ranger expo poster (rendered at 2x the size they occupy on the Canva page)."""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIT = "/home/user/temp-video/Ranger_Video_Kit"
CUT = os.path.join(W, "build/cut")
OUT = "/home/user/temp-video/Ranger_Video_Kit/poster/assets"
os.makedirs(OUT, exist_ok=True)
FONT = "/usr/share/fonts/opentype/inter/Inter-{}.otf"

NAVY = (0x04, 0x20, 0x34)
INK = (0x16, 0x22, 0x2B)
GREEN = (0x2F, 0x6D, 0x4F)
MINT = (0x7C, 0xC4, 0xA0)
TINT = (0xEA, 0xF3, 0xEE)
RED = (0xB3, 0x26, 0x1E)
GREY = (0x5B, 0x66, 0x70)


def f(w, s):
    return ImageFont.truetype(FONT.format(w), s)


def shadow(img, box, r, blur, alpha, off=(0, 10)):
    m = Image.new("L", img.size, 0)
    x0, y0, x1, y1 = box
    ImageDraw.Draw(m).rounded_rectangle([x0 + off[0], y0 + off[1], x1 + off[0], y1 + off[1]], r, fill=alpha)
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sh.putalpha(m.filter(ImageFilter.GaussianBlur(blur)))
    img.alpha_composite(sh)


def paste_fit(img, src, box, mode="contain", radius=0):
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    s = (min if mode == "contain" else max)(bw / src.width, bh / src.height)
    im = src.resize((max(1, round(src.width * s)), max(1, round(src.height * s))), Image.LANCZOS)
    if mode == "cover":
        l, t = (im.width - bw) // 2, (im.height - bh) // 2
        im = im.crop((l, t, l + bw, t + bh))
        px, py = x0, y0
    else:
        px, py = x0 + (bw - im.width) // 2, y0 + (bh - im.height) // 2
    if radius:
        m = Image.new("L", im.size, 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius, fill=255)
        if im.mode == "RGBA":
            m = Image.fromarray(np.minimum(np.asarray(m), np.asarray(im.getchannel("A"))))
        im = im.convert("RGBA")
        im.putalpha(m)
    img.alpha_composite(im.convert("RGBA"), (px, py))
    return (px, py, px + im.width, py + im.height)


def arrow(d, p0, p1, color, width=8, head=26):
    d.line([p0, p1], fill=color, width=width)
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    a1 = (p1[0] - head * math.cos(ang - 0.45), p1[1] - head * math.sin(ang - 0.45))
    a2 = (p1[0] - head * math.cos(ang + 0.45), p1[1] - head * math.sin(ang + 0.45))
    d.polygon([p1, a1, a2], fill=color)


def lock(d, cx, cy, s, color=(255, 255, 255)):
    d.rounded_rectangle([cx - 11 * s, cy - 2 * s, cx + 11 * s, cy + 15 * s], 3 * s, fill=color)
    d.arc([cx - 8 * s, cy - 16 * s, cx + 8 * s, cy + 2 * s], 180, 360, fill=color, width=int(4 * s))
    d.line([cx - 8 * s, cy - 7 * s, cx - 8 * s, cy - 1 * s], fill=color, width=int(4 * s))
    d.line([cx + 8 * s, cy - 7 * s, cx + 8 * s, cy - 1 * s], fill=color, width=int(4 * s))


# ---------------------------------------------------------------- hero photo
def hero():
    w, h = 2800, 1840
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    bg = Image.new("RGBA", (w, h))
    t = np.linspace(0, 1, h)[:, None, None]
    c = np.array((247, 250, 248), np.float32) * (1 - t) + np.array((226, 237, 231), np.float32) * t
    bg = Image.fromarray(np.repeat(c, w, 1).astype(np.uint8)).convert("RGBA")
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 40, fill=255)
    img.paste(bg, (0, 0), m)
    dev = Image.open(os.path.join(CUT, "IMG_9673.png")).convert("RGBA")
    # soft floor shadow
    fl = Image.new("L", (w, h), 0)
    ImageDraw.Draw(fl).ellipse([700, 1640, 2100, 1760], fill=120)
    sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sh.putalpha(fl.filter(ImageFilter.GaussianBlur(40)))
    img.alpha_composite(sh)
    paste_fit(img, dev, (420, 60, 2380, 1740))
    d = ImageDraw.Draw(img)
    fnt = f("SemiBold", 44)
    txt = "Three working Ranger handsets, custom PCB"
    tw = d.textlength(txt, font=fnt)
    d.rounded_rectangle([60, h - 140, 60 + tw + 70, h - 60], 40, fill=NAVY + (235,))
    d.text((95, h - 100), txt, font=fnt, fill=(255, 255, 255), anchor="lm")
    img.save(os.path.join(OUT, "hero.png"))


# ---------------------------------------------------------------- mesh scenario
def mesh():
    w, h = 2912, 1312
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 40, fill=255)
    base = Image.new("RGBA", (w, h), (244, 248, 246, 255))
    # contour map
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32) / 260.0
    fld = np.sin(xx * 1.1 + np.sin(yy * 0.8) * 1.7) + np.cos(yy * 1.3 - np.sin(xx * 0.6) * 2.0) + 0.5 * np.sin((xx - yy) * 2.1)
    band = np.abs(((fld * 3.0) % 1.0) - 0.5) > 0.47
    arr = np.asarray(base).copy()
    arr[band] = (np.array([206, 226, 214, 255]) * 1).astype(np.uint8)
    base = Image.fromarray(arr)
    img.paste(base, (0, 0), m)
    d = ImageDraw.Draw(img)
    dev = Image.open(os.path.join(CUT, "IMG_9657.png")).convert("RGBA")
    dev = dev.resize((round(dev.width * 170 / dev.height), 170), Image.LANCZOS)
    nodes = [(330, 900), (930, 560), (1530, 860), (2130, 520), (2600, 900)]
    R = 380
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for x, y in nodes:
        od.ellipse([x - R, y - R, x + R, y + R], fill=(0x2F, 0x6D, 0x4F, 18), outline=(0x2F, 0x6D, 0x4F, 90), width=4)
    img.alpha_composite(ov)
    d = ImageDraw.Draw(img)
    for i in range(len(nodes) - 1):
        (x0, y0), (x1, y1) = nodes[i], nodes[i + 1]
        ux, uy = x1 - x0, y1 - y0
        L = math.hypot(ux, uy)
        ux, uy = ux / L, uy / L
        p0 = (x0 + ux * 120, y0 + uy * 120)
        p1 = (x1 - ux * 120, y1 - uy * 120)
        arrow(d, p0, p1, GREEN, 10, 34)
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        d.ellipse([mx - 34, my - 34, mx + 34, my + 34], fill=GREEN)
        lock(d, mx, my - 2, 1.5)
    for k, (x, y) in enumerate(nodes):
        img.alpha_composite(dev, (int(x - dev.width / 2), int(y - dev.height / 2)))
    d = ImageDraw.Draw(img)
    lab = f("Bold", 40)
    small = f("SemiBold", 34)
    # end labels
    d.text((nodes[0][0], nodes[0][1] + 130), "Trapped survivor", font=lab, fill=RED, anchor="mm")
    d.text((nodes[-1][0], nodes[-1][1] + 130), "Rescue team", font=lab, fill=GREEN, anchor="mm")
    for x, y in nodes[1:-1]:
        d.text((x, y + 125), "Relay", font=small, fill=GREY, anchor="mm")
    # collapsed building icon near survivor
    bx, by = 40, 560
    d.polygon([(bx, by + 160), (bx, by + 20), (bx + 60, by), (bx + 90, by + 50), (bx + 140, by + 10), (bx + 150, by + 160)], fill=(150, 150, 156))
    for k in range(5):
        d.polygon([(bx - 20 + k * 40, by + 190), (bx + 30 + k * 40, by + 160), (bx + 60 + k * 40, by + 200)], fill=(120, 120, 126))
    # crossed tower
    tx, ty = 2620, 150
    d.line([(tx - 70, ty + 230), (tx, ty), (tx + 70, ty + 230)], fill=GREY, width=10)
    d.line([(tx - 45, ty + 140), (tx + 45, ty + 140)], fill=GREY, width=8)
    for r in (40, 75):
        d.arc([tx - r, ty - r, tx + r, ty + r], 200, 340, fill=GREY, width=8)
    d.line([(tx - 120, ty - 70), (tx + 120, ty + 250)], fill=RED, width=16)
    d.text((tx, ty + 300), "Towers down", font=small, fill=RED, anchor="mm")
    # scale bar + callouts
    d.line([(120, 1210), (120 + R, 1210)], fill=INK, width=8)
    for xx in (120, 120 + R):
        d.line([(xx, 1190), (xx, 1230)], fill=INK, width=8)
    d.text((120 + R / 2, 1180), "up to 8 km per hop", font=small, fill=INK, anchor="ms")
    chips = [("Every Ranger relays", GREEN), ("AES-128 encrypted", NAVY), ("No towers, no SIM", RED)]
    x = 700
    for txt, col in chips:
        tw = d.textlength(txt, font=lab)
        d.rounded_rectangle([x, 1150, x + tw + 80, 1250], 50, fill=col)
        d.text((x + 40, 1200), txt, font=lab, fill=(255, 255, 255), anchor="lm")
        x += tw + 120
    d.text((70, 70), "Messages hop Ranger to Ranger: range grows with every device", font=f("Bold", 46), fill=INK)
    img.save(os.path.join(OUT, "mesh.png"))


# ---------------------------------------------------------------- system architecture
def box(d, xy, title, sub=None, fill=(255, 255, 255), outline=GREEN, tcol=INK, r=24, ts=40, ss=31):
    x0, y0, x1, y1 = xy
    d.rounded_rectangle(xy, r, fill=fill, outline=outline, width=5)
    cy = (y0 + y1) / 2
    if sub:
        d.text(((x0 + x1) / 2, cy - 22), title, font=f("Bold", ts), fill=tcol, anchor="mm")
        d.text(((x0 + x1) / 2, cy + 28), sub, font=f("Medium", ss), fill=GREY if tcol == INK else tcol, anchor="mm")
    else:
        d.text(((x0 + x1) / 2, cy), title, font=f("Bold", ts), fill=tcol, anchor="mm")


def arch():
    w, h = 3400, 1252
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 40, fill=(247, 250, 248))
    # column labels
    hl = f("Bold", 34)
    for x, t in ((330, "INPUTS"), (1440, "PROCESSING"), (2470, "OUTPUTS & RADIO")):
        d.text((x, 60), t, font=hl, fill=GREEN, anchor="mm")
    ins = [("T9 keypad + knob", "menus, typing"), ("Push-to-talk", "VOICE button"),
           ("MEMS microphone", "ICS-43434, I2S"), ("GPS + compass", "u-blox M10, QMC5883")]
    for i, (a, b) in enumerate(ins):
        y = 120 + i * 230
        box(d, (60, y, 600, y + 180), a, b)
        arrow(d, (600, y + 90), (880, y + 90 if i in (1, 2) else 560 + (i - 1.5) * 60), GREEN, 7, 26)
    # ESP32 core
    d.rounded_rectangle([880, 120, 2000, 1000], 30, fill=NAVY)
    d.text((1440, 200), "ESP32-WROOM-32E", font=f("ExtraBold", 54), fill=(255, 255, 255), anchor="mm")
    d.text((1440, 260), "dual-core 240 MHz, custom firmware", font=f("Medium", 32), fill=MINT, anchor="mm")
    tasks = ["Codec2 voice compression", "AES-128-CCM encryption", "Mesh routing & relaying", "UI, tracking & SOS",
             "Wi-Fi hotspot web page"]
    for i, t in enumerate(tasks):
        y = 330 + i * 128
        d.rounded_rectangle([950, y, 1930, y + 100], 20, fill=(0x12, 0x3C, 0x58), outline=(0x7C, 0xC4, 0xA0), width=3)
        d.text((1440, y + 50), t, font=f("SemiBold", 40), fill=(255, 255, 255), anchor="mm")
    outs = [("LoRa radio", "E28 SX1280, 2.4 GHz, 27 dBm"), ("OLED 128×64", "messages, map, compass"),
            ("Amp + speaker", "MAX98357A, I2S"), ("Phones (up to 3)", "Wi-Fi, browser, no app")]
    for i, (a, b) in enumerate(outs):
        y = 120 + i * 230
        fill = (0xEA, 0xF3, 0xEE) if i == 0 else (255, 255, 255)
        box(d, (2200, y, 2760, y + 180), a, b, fill=fill, ts=40, ss=28)
        arrow(d, (2000, 560 + (i - 1.5) * 60), (2200, y + 90), GREEN, 7, 26)
    # radio link to other Rangers
    dev = Image.open(os.path.join(CUT, "IMG_9657.png")).convert("RGBA")
    dev = dev.resize((round(dev.width * 300 / dev.height), 300), Image.LANCZOS)
    img.alpha_composite(dev, (3080 - dev.width // 2, 140))
    d = ImageDraw.Draw(img)
    for r in (40, 80, 120):
        d.arc([2860 - r, 210 - r, 2860 + r, 210 + r], -60, 60, fill=GREEN, width=8)
    arrow(d, (2770, 210), (2950, 210), GREEN, 8, 28)
    d.text((3080, 480), "Other Rangers", font=f("Bold", 40), fill=INK, anchor="mm")
    d.text((3080, 530), "mesh, up to 8 km/hop", font=f("Medium", 30), fill=GREY, anchor="mm")
    # power
    d.rounded_rectangle([880, 1060, 2760, 1180], 26, fill=(0xFF, 0xF4, 0xD6), outline=(0xC9, 0x93, 0x1A), width=4)
    d.text((1820, 1120), "Power: 3.7 V 1000 mAh LiPo  ·  USB-C charging  ·  low-power sleep, radio still listening",
           font=f("SemiBold", 38), fill=(0x6B, 0x4A, 0x05), anchor="mm")
    img.save(os.path.join(OUT, "architecture.png"))


# ---------------------------------------------------------------- build journey
def build():
    w, h = 5672, 860
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    proto = Image.open(f"{KIT}/product_images/First_Setup.jpeg").convert("RGBA")
    schem = Image.open(f"{KIT}/product_images/Esp32_schematic.png").convert("RGBA")
    pcb = Image.open(f"{KIT}/product_images/PCB_design.png").convert("RGBA")
    top = Image.open(os.path.join(CUT, "Top_3D.png")).convert("RGBA")
    bot = Image.open(os.path.join(CUT, "Bottom_3D.png")).convert("RGBA")
    real = Image.open(os.path.join(CUT, "IMG_9658.png")).convert("RGBA")
    fw, gap = 980, 193
    xs = [i * (fw + gap) for i in range(5)]
    d = ImageDraw.Draw(img)
    for i, x in enumerate(xs):
        box_ = (x + 10, 40, x + fw - 10, h - 40)
        shadow(img, box_, 30, 18, 90, (0, 8))
        d = ImageDraw.Draw(img)
        bg = (255, 255, 255) if i != 2 else (0x1A, 0x16, 0x3A)
        d.rounded_rectangle(box_, 30, fill=bg, outline=(0xD3, 0xE2, 0xD9) if i != 2 else GREEN, width=6 if i == 2 else 3)
        inner = (box_[0] + 24, box_[1] + 24, box_[2] - 24, box_[3] - 24)
        if i == 0:
            paste_fit(img, proto, inner, "cover", 20)
        elif i == 1:
            paste_fit(img, schem, inner, "contain", 12)
        elif i == 2:
            paste_fit(img, pcb, inner, "contain", 12)
        elif i == 3:
            mid = (inner[0] + inner[2]) // 2
            paste_fit(img, top, (inner[0], inner[1], mid - 6, inner[3]))
            paste_fit(img, bot, (mid + 6, inner[1], inner[2], inner[3]))
        else:
            paste_fit(img, real, inner)
        d = ImageDraw.Draw(img)
        cx, cy = x + 70, 90
        d.ellipse([cx - 46, cy - 46, cx + 46, cy + 46], fill=GREEN if i != 2 else (0xC9, 0x93, 0x1A))
        d.text((cx, cy), str(i + 1), font=f("ExtraBold", 54), fill=(255, 255, 255), anchor="mm")
        if i < 4:
            ax = x + fw + 20
            arrow(d, (ax, h / 2), (ax + gap - 40, h / 2), GREEN, 14, 44)
    img.save(os.path.join(OUT, "build_journey.png"))


if __name__ == "__main__":
    hero()
    mesh()
    arch()
    build()
    prev = Image.new("RGB", (2900, 3000), (255, 255, 255))
    y = 0
    for n, wd in (("hero.png", 1400), ("mesh.png", 1456), ("architecture.png", 1700), ("build_journey.png", 2836)):
        im = Image.open(os.path.join(OUT, n))
        im = im.resize((wd, round(im.height * wd / im.width)))
        prev.paste(im, (0, y), im)
        y += im.height + 30
    prev.crop((0, 0, 2900, y)).save(os.path.join(W, "poster_prev.jpg"), quality=85)
    print("ok")
