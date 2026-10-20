"""依 JSON 描述合成部件，輸出去背 PNG"""
import json, sys
from PIL import Image

def render(spec, out, bg=None, scale=1.0):
    W, H = spec["size"]
    W, H = int(W*scale), int(H*scale)
    canvas = Image.new("RGBA", (W, H), (0,0,0,0) if bg is None else bg+(255,))
    for item in spec["placements"]:
        idx, x, y, sc, flip = item[:5]
        rot = item[5] if len(item) > 5 else 0
        im = Image.open(f"assets/parts_raw/part_{idx:02d}.png").convert("RGBA")
        if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
        w, h = max(1,int(im.width*sc*scale)), max(1,int(im.height*sc*scale))
        im = im.resize((w,h), Image.LANCZOS)
        if rot:
            im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
        canvas.alpha_composite(im, (int(x*scale-im.width/2), int(y*scale-im.height/2)))
    canvas.save(out)
    return canvas.size

if __name__ == "__main__":
    spec = json.loads(sys.argv[1]) if sys.argv[1].startswith("{") else json.load(open(sys.argv[1], encoding="utf-8"))
    print(render(spec, sys.argv[2]))
