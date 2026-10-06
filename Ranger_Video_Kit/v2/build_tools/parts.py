"""Component cards for Ranger v2: drawn stand-in of each part + name, role, key spec (from components.json)."""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(W, "build/v2/parts")
os.makedirs(OUT, exist_ok=True)
FONT = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
MINT = (0x7C, 0xC4, 0xA0)
KEY_SPEC = {"esp32": "2 cores, 240 MHz", "lora": "27 dBm · up to 8 km", "oled": "128 × 64 px · 0.96 inch",
            "mic": "24-bit I2S digital", "amp": "Class D · I2S in", "gps": "u-blox M10 + compass"}


def f(w, s):
    return ImageFont.truetype(FONT.format(w), s)


def shield(d, box, label=None):
    x0, y0, x1, y1 = box
    for i in range(int(y1 - y0)):
        g = int(200 - 50 * i / (y1 - y0))
        d.line([x0, y0 + i, x1, y0 + i], fill=(g, g, g + 6, 255))
    d.rectangle(box, outline=(120, 124, 130, 255), width=2)
    if label:
        d.text(((x0 + x1) / 2, (y0 + y1) / 2), label, font=f("Bold", 22), fill=(70, 74, 80, 255), anchor="mm")


def pads(d, x0, y0, x1, y1, n, side, col=(214, 172, 80, 255)):
    for k in range(n):
        if side in ("l", "r"):
            y = y0 + (k + 0.5) * (y1 - y0) / n
            x = x0 if side == "l" else x1
            d.rectangle([x - 5, y - 4, x + 5, y + 4], fill=col)
        else:
            x = x0 + (k + 0.5) * (x1 - x0) / n
            y = y1 if side == "b" else y0
            d.rectangle([x - 4, y - 5, x + 4, y + 5], fill=col)


def draw_part(key, d, cx, cy):
    if key == "esp32":
        d.rectangle([cx - 90, cy - 110, cx + 90, cy + 110], fill=(20, 26, 36, 255))
        for k in range(6):
            x = cx - 70 + k * 28
            d.line([x, cy - 100, x, cy - 74, x + 14, cy - 74, x + 14, cy - 100], fill=(214, 172, 80, 255), width=3)
        shield(d, (cx - 80, cy - 60, cx + 80, cy + 100), "ESP32")
        pads(d, cx - 90, cy - 60, cx - 90, cy + 110, 9, "l")
        pads(d, cx + 90, cy - 60, cx + 90, cy + 110, 9, "r")
    elif key == "lora":
        d.rectangle([cx - 80, cy - 100, cx + 80, cy + 100], fill=(22, 60, 120, 255))
        shield(d, (cx - 64, cy - 60, cx + 64, cy + 86), "E28")
        d.ellipse([cx + 34, cy - 92, cx + 66, cy - 64], fill=(200, 180, 120, 255), outline=(120, 100, 60, 255), width=3)
        pads(d, cx - 80, cy - 90, cx - 80, cy + 100, 8, "l")
        pads(d, cx + 80, cy - 50, cx + 80, cy + 100, 6, "r")
    elif key == "oled":
        d.rectangle([cx - 130, cy - 80, cx + 130, cy + 50], fill=(8, 8, 10, 255), outline=(90, 96, 100, 255), width=3)
        for k in range(5):
            w_ = [180, 120, 200, 90, 150][k]
            d.rectangle([cx - 110, cy - 64 + k * 22, cx - 110 + w_, cy - 54 + k * 22], fill=(235, 240, 240, 255))
        d.polygon([(cx - 50, cy + 50), (cx + 50, cy + 50), (cx + 40, cy + 110), (cx - 40, cy + 110)], fill=(214, 150, 50, 255))
    elif key == "mic":
        d.rounded_rectangle([cx - 70, cy - 56, cx + 70, cy + 56], 8, fill=(190, 192, 196, 255), outline=(120, 124, 130, 255), width=3)
        d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(30, 30, 34, 255))
        d.text((cx, cy + 34), "ICS-43434", font=f("Bold", 16), fill=(80, 84, 90, 255), anchor="mm")
        d.text((cx, cy + 96), "3.5 × 2.7 mm (shown enlarged)", font=f("Medium", 18), fill=(150, 160, 155, 255), anchor="mm")
    elif key == "amp":
        d.rectangle([cx - 66, cy - 66, cx + 66, cy + 66], fill=(24, 24, 28, 255), outline=(70, 70, 76, 255), width=2)
        for side in "lrtb":
            if side in "lr":
                pads(d, cx - 66 if side == "l" else cx + 66, cy - 60, cx - 66 if side == "l" else cx + 66, cy + 60, 4, side, (190, 190, 196, 255))
            else:
                pads(d, cx - 60, cy - 66 if side == "t" else cy + 66, cx + 60, cy - 66 if side == "t" else cy + 66, 4, side, (190, 190, 196, 255))
        d.ellipse([cx - 52, cy - 52, cx - 40, cy - 40], fill=(110, 110, 116, 255))
        d.text((cx, cy), "98357A", font=f("Bold", 22), fill=(160, 160, 166, 255), anchor="mm")
    elif key == "gps":
        d.rounded_rectangle([cx - 100, cy - 100, cx + 100, cy + 100], 14, fill=(20, 20, 24, 255), outline=(60, 62, 66, 255), width=3)
        d.rectangle([cx - 66, cy - 66, cx + 66, cy + 66], fill=(206, 176, 130, 255))
        d.rectangle([cx - 46, cy - 46, cx + 46, cy + 46], fill=(214, 216, 220, 255))
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(150, 120, 80, 255))


def card(c):
    w, h = 540, 420
    pad = 40
    im = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([pad, pad, pad + w, pad + h], 26, fill=255)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sh.putalpha(m.filter(ImageFilter.GaussianBlur(20)).point(lambda v: int(v * 0.7)))
    im.alpha_composite(sh, (0, 10))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([pad, pad, pad + w, pad + h], 26, fill=(24, 30, 27, 255), outline=(60, 74, 66, 255), width=2)
    # drawing area
    glow = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([pad + 120, pad + 10, pad + w - 120, pad + 260], fill=(0x2F, 0x6D, 0x4F, 110))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(40)))
    d = ImageDraw.Draw(im)
    draw_part(c["key"], d, pad + w // 2, pad + 140)
    d.text((pad + 30, pad + 300), c["name"], font=f("ExtraBold", 36), fill=(242, 244, 241, 255))
    d.text((pad + 30, pad + 346), c["role"].upper(), font=f("Bold", 20), fill=MINT + (255,))
    d.text((pad + 30, pad + 376), KEY_SPEC[c["key"]], font=f("Medium", 22), fill=(180, 192, 185, 255))
    im.save(os.path.join(OUT, f"part_{c['key']}.png"))


if __name__ == "__main__":
    comps = json.load(open(sys.argv[1]))["components"]
    for c in comps:
        card(c)
    # preview
    prev = Image.new("RGB", (1860, 1000), (14, 18, 16))
    for i, c in enumerate(comps):
        p = Image.open(os.path.join(OUT, f"part_{c['key']}.png"))
        prev.paste(p, ((i % 3) * 620, (i // 3) * 500), p)
    prev.save(os.path.join(OUT, "preview.jpg"))
    print("ok")
