"""用部件表組合 ν 鋼彈，輸出預覽圖"""
import json, sys
from PIL import Image

SHEET = "assets/PlayStation 2 - SD Gundam G Generation Wars - Units - n Gundam.png"
_sheet = Image.open(SHEET).convert("RGBA")

PARTS = {
    # 大型部件（band3, y=1561..2069）
    "rifle":     (1, 1561, 246, 1729),
    "shoulder":  (254, 1561, 376, 1660),
    "shoulder2": (391, 1564, 505, 1689),
    "head":      (161, 1733, 370, 1920),
    "chest":     (376, 1696, 509, 1917),
    "shield":    (772, 1712, 1027, 2067),
    "backpack":  (523, 1771, 762, 2067),
    "waist":     (1, 1948, 179, 2067),
    "hip":       (310, 1929, 508, 2068),
}

def part_img(name, flip=False):
    im = _sheet.crop(PARTS[name])
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    return im

def build(placements, size=(600, 640), bg=(24, 28, 38)):
    """placements: [(name, cx, cy, scale, flip, rot), ...] 由底層畫到頂層"""
    canvas = Image.new("RGBA", size, (0, 0, 0, 0) if bg is None else bg + (255,))
    for item in placements:
        name, cx, cy, sc, flip = item[:5]
        rot = item[5] if len(item) > 5 else 0
        im = part_img(name, flip)
        w, h = max(1, int(im.width * sc)), max(1, int(im.height * sc))
        im = im.resize((w, h), Image.LANCZOS)
        if rot:
            im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
        canvas.alpha_composite(im, (int(cx - im.width/2), int(cy - im.height/2)))
    return canvas

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    bg = spec.get("bg", [24, 28, 38])
    bg = None if bg is None else tuple(bg)
    out = build(spec["placements"], tuple(spec.get("size", [600, 640])), bg)
    if spec.get("alpha"):
        out.save(sys.argv[2])
    else:
        out.convert("RGB").save(sys.argv[2])
    print("saved", sys.argv[2])
