"""Static graphics kit for the Ranger film: background plate, OLED cards,
phone mockups, hero cut-outs with rim light, QR cards, photo cards."""
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

KIT = "/home/user/temp-video/Ranger_Video_Kit"
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUT = os.path.join(W, "build/cut")
OUT = os.path.join(W, "build/assets")
os.makedirs(OUT, exist_ok=True)
FONT = "/usr/share/fonts/opentype/inter/Inter-{}.otf"

BG0 = (0x0E, 0x12, 0x10)
BG1 = (0x1C, 0x22, 0x1F)
GREEN = (0x2F, 0x6D, 0x4F)


def font(weight, size):
    return ImageFont.truetype(FONT.format(weight), size)


def background():
    h, w = 1080, 1920
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xx - w * 0.5) / (w * 0.62)) ** 2 + ((yy - h * 0.42) / (h * 0.75)) ** 2)
    t = np.clip(d, 0, 1)[..., None]
    c = np.array(BG1, np.float32) * (1 - t) + np.array(BG0, np.float32) * t
    rng = np.random.default_rng(1)
    c += rng.normal(0, 1.2, c.shape)
    Image.fromarray(np.clip(c, 0, 255).astype(np.uint8)).save(f"{OUT}/bg.png")


def shadow(alpha, blur, opacity, offset=(0, 0), color=(0, 0, 0)):
    a = alpha.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * opacity))
    layer = Image.new("RGBA", alpha.size, color + (0,))
    layer.putalpha(a)
    if offset != (0, 0):
        moved = Image.new("RGBA", alpha.size, color + (0,))
        moved.paste(layer, offset)
        layer = moved
    return layer


def rounded_mask(size, r):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], r, fill=255)
    return m


def oled_card(name):
    scr = Image.open(f"{KIT}/oled_screens/black_background/{name}.png").convert("RGB")
    sw, sh = scr.size  # 1024 x 512
    bez, pad = 26, 70
    cw, ch = sw + 2 * bez + 2 * pad, sh + 2 * bez + 2 * pad
    card = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    body = Image.new("L", (cw, ch), 0)
    ImageDraw.Draw(body).rounded_rectangle([pad, pad, cw - pad, ch - pad], 30, fill=255)
    card = Image.alpha_composite(card, shadow(body, 34, 0.75, (0, 14)))
    frame = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle([pad, pad, cw - pad, ch - pad], 30, fill=(8, 10, 9, 255), outline=(52, 64, 58, 255), width=2)
    card = Image.alpha_composite(card, frame)
    # emissive bloom: blurred copy of the pixels added on top
    arr = np.asarray(scr, np.float32)
    bloom = np.asarray(scr.filter(ImageFilter.GaussianBlur(10)), np.float32)
    lit = np.clip(arr + bloom * 0.55, 0, 255).astype(np.uint8)
    lit_im = Image.fromarray(lit).convert("RGBA")
    card.paste(lit_im, (pad + bez, pad + bez), rounded_mask((sw, sh), 8))
    card.save(f"{OUT}/oled_{name[:2]}.png")


def phone(name):
    scr = Image.open(f"{KIT}/phone_screens/{name}_dark.png").convert("RGB")
    scr = scr.resize((scr.width // 2, scr.height // 2), Image.LANCZOS)  # 585 x 1266
    sw, sh = scr.size
    bez, pad = 18, 70
    cw, ch = sw + 2 * bez + 2 * pad, sh + 2 * bez + 2 * pad
    body = Image.new("L", (cw, ch), 0)
    ImageDraw.Draw(body).rounded_rectangle([pad, pad, cw - pad, ch - pad], 86, fill=255)
    card = shadow(body, 36, 0.8, (0, 16))
    f = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    d = ImageDraw.Draw(f)
    d.rounded_rectangle([pad, pad, cw - pad, ch - pad], 86, fill=(14, 16, 15, 255), outline=(70, 82, 76, 255), width=3)
    card = Image.alpha_composite(card, f)
    card.paste(scr, (pad + bez, pad + bez), rounded_mask((sw, sh), 68))
    d = ImageDraw.Draw(card)
    ix = cw // 2
    d.rounded_rectangle([ix - 70, pad + bez + 14, ix + 70, pad + bez + 52], 19, fill=(0, 0, 0, 255))
    card.save(f"{OUT}/phone_{name[:2]}.png")


def hero(src, out, height, rim=0.55):
    im = Image.open(f"{CUT}/{src}").convert("RGBA")
    im = im.resize((round(im.width * height / im.height), height), Image.LANCZOS)
    # gentle lift: shadows up a touch, neutral
    rgb = np.asarray(im.convert("RGB"), np.float32) / 255
    rgb = np.clip(rgb ** 0.92 * 1.03, 0, 1)
    im2 = Image.fromarray((rgb * 255).astype(np.uint8)).convert("RGBA")
    im2.putalpha(im.getchannel("A"))
    pad = 120
    cw, ch = im.width + 2 * pad, im.height + 2 * pad
    a = Image.new("L", (cw, ch), 0)
    a.paste(im.getchannel("A"), (pad, pad))
    canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    # floor shadow
    fl = Image.new("L", (cw, ch), 0)
    ImageDraw.Draw(fl).ellipse([pad + im.width * 0.08, pad + im.height - 30, pad + im.width * 0.92, pad + im.height + 40], fill=200)
    canvas = Image.alpha_composite(canvas, shadow(fl, 28, 0.8))
    canvas = Image.alpha_composite(canvas, shadow(a, 48, rim, color=(0x4F, 0xB0, 0x82)))
    canvas = Image.alpha_composite(canvas, shadow(a, 14, 0.5, color=(0x2F, 0x6D, 0x4F)))
    canvas.paste(im2, (pad, pad), im2)
    canvas.save(f"{OUT}/{out}.png")
    print(out, canvas.size)


def qr_cards():
    q = Image.open(f"{KIT}/qr_code/qr_end_card_nadeeshanj_ranger.png").convert("RGBA")
    pad = 80
    c = Image.new("RGBA", (q.width + 2 * pad, q.height + 2 * pad), (0, 0, 0, 0))
    a = Image.new("L", c.size, 0)
    a.paste(q.getchannel("A"), (pad, pad))
    c = Image.alpha_composite(c, shadow(a, 40, 0.7, (0, 18)))
    c.paste(q, (pad, pad), q)
    c.save(f"{OUT}/qr_end.png")
    print("qr_end", c.size)
    # small corner tag: white rounded card, QR, url
    s = Image.open(f"{KIT}/qr_code/qr_nadeeshanj_ranger_dark.png").convert("RGBA")
    qs = 300
    s = s.resize((qs, qs), Image.NEAREST)
    cw, ch = qs + 40, qs + 92
    tag = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    ImageDraw.Draw(tag).rounded_rectangle([0, 0, cw - 1, ch - 1], 26, fill=(255, 255, 255, 255))
    tag.paste(s, (20, 18), s)
    d = ImageDraw.Draw(tag)
    f = font("SemiBold", 27)
    t = "nadeeshanj.dev/ranger"
    tw = d.textlength(t, font=f)
    d.text(((cw - tw) / 2, qs + 34), t, font=f, fill=(20, 28, 24, 255))
    tag.save(f"{OUT}/qr_corner.png")
    print("qr_corner", tag.size)


def photo_card(src, out, box_h, radius=28, from_cut=False):
    im = Image.open(src)
    im = ImageOps.exif_transpose(im).convert("RGBA")
    im = im.resize((round(im.width * box_h / im.height), box_h), Image.LANCZOS)
    pad = 70
    cw, ch = im.width + 2 * pad, im.height + 2 * pad
    a = Image.new("L", (cw, ch), 0)
    a.paste(rounded_mask(im.size, radius), (pad, pad))
    c = shadow(a, 34, 0.75, (0, 14))
    if from_cut:
        c = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        c.paste(im, (pad, pad), im)
    else:
        layer = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        layer.paste(im, (pad, pad), rounded_mask(im.size, radius))
        c = Image.alpha_composite(c, layer)
        ImageDraw.Draw(c).rounded_rectangle([pad, pad, pad + im.width - 1, pad + im.height - 1], radius, outline=(255, 255, 255, 40), width=2)
    c.save(f"{OUT}/{out}.png")
    print(out, c.size)


if __name__ == "__main__":
    background()
    for n in ["01_startup_logo", "02_main_menu", "04_people_list", "05_people_list_phone_selected",
              "07_track_gps_compass", "08_track_radio_ranging_no_gps", "10_location_gps_compass",
              "15_location_shared", "17_chat", "18_chat_typing_t9", "19_broadcast",
              "20_broadcast_sos_sent", "21_talk_ready", "22_talk_talking", "25_settings_phone_wifi_on",
              "26_settings_auto_sleep", "11_location_gps_from_phone"]:
        oled_card(n)
    for n in ["01_join_enter_name", "02_messages_everyone", "03_messages_private_chat",
              "04_people_distance_direction", "05_sos_share_location_phone_gps",
              "06_gps_page_sharing_phone_location"]:
        phone(n)
    hero("IMG_9658.png", "hero_front", 860)
    hero("IMG_9673.png", "hero_three", 820, rim=0.45)
    hero("IMG_9663.png", "hero_back", 760, rim=0.45)
    hero("IMG_9657.png", "hero_side", 760, rim=0.45)
    hero("Top_3D.png", "render_top", 760, rim=0.4)
    hero("Bottom_3D.png", "render_bottom", 760, rim=0.4)
    qr_cards()
    photo_card(f"{KIT}/product_images/First_Setup.jpeg", "card_proto", 560)
    photo_card(f"{KIT}/product_images/PCB_design.png", "card_pcb", 620)
    photo_card(f"{KIT}/product_images/Esp32_schematic.png", "card_schem", 600)
