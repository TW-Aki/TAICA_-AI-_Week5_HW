"""切出素材表中的獨立部件（連通區域分析）"""
import sys, json
from PIL import Image

SHEET = "assets/PlayStation 2 - SD Gundam G Generation Wars - Units - n Gundam.png"

def runs_of_row(alpha, y, w, thr=12, mingap=2):
    """回傳該列的不透明區段 [(x0,x1)]"""
    px = alpha.crop((0, y, w, y+1)).load()
    out, start = [], None
    gap = 0
    for x in range(w):
        on = px[x, 0] > thr
        if on:
            if start is None:
                start = x
            gap = 0
        else:
            if start is not None:
                gap += 1
                if gap > mingap:
                    out.append((start, x - gap))
                    start = None
    if start is not None:
        out.append((start, w - 1))
    return out

def components(img, y0, y1, thr=12, min_area=1500):
    alpha = img.split()[3]
    w = img.width
    parent = {}
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    nodes = {}   # id -> (x0,x1,y)
    prev = []
    nid = 0
    for y in range(y0, y1):
        cur = []
        for (x0, x1) in runs_of_row(alpha, y, w, thr):
            nid += 1
            nodes[nid] = (x0, x1, y)
            parent[nid] = nid
            cur.append((x0, x1, nid))
            for (px0, px1, pid) in prev:
                if not (x1 < px0 - 1 or x0 > px1 + 1):
                    union(pid, nid)
        prev = cur

    groups = {}
    for nid, (x0, x1, y) in nodes.items():
        r = find(nid)
        if r not in groups:
            groups[r] = [x0, y, x1, y, 0]
        g = groups[r]
        g[0] = min(g[0], x0); g[1] = min(g[1], y)
        g[2] = max(g[2], x1); g[3] = max(g[3], y)
        g[4] += (x1 - x0 + 1)

    out = []
    for g in groups.values():
        if g[4] >= min_area:
            out.append((g[0], g[1], g[2], g[3], g[4]))
    out.sort(key=lambda b: (b[1] // 60, b[0]))
    return out

if __name__ == "__main__":
    y0, y1 = int(sys.argv[1]), int(sys.argv[2])
    img = Image.open(SHEET).convert("RGBA")
    comps = components(img, y0, y1)
    print(json.dumps([[int(v) for v in c] for c in comps]))
