import sys, os
from PIL import Image, ImageOps
from rembg import remove, new_session
src, out = sys.argv[1], sys.argv[2]
s = new_session("isnet-general-use")
os.makedirs(out, exist_ok=True)
for name in sys.argv[3:]:
    im = ImageOps.exif_transpose(Image.open(os.path.join(src, name))).convert("RGB")
    im.thumbnail((2400, 2400))
    r = remove(im, session=s)
    bb = r.getchannel("A").point(lambda a: 255 if a > 20 else 0).getbbox()
    r = r.crop(bb)
    r.save(os.path.join(out, name.replace(".jpeg", ".png")))
    print(name, r.size)
