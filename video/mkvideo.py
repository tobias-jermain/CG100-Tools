#!/usr/bin/env python3
"""Turn a GIF or a folder of images into a clip for video.py (runs on a PC, needs Pillow).

  python3 mkvideo.py clip.gif                 # black and white, 48 cells wide
  python3 mkvideo.py clip.gif -c 8 -s 6       # 8 colours, 6-pixel cells
  python3 mkvideo.py frames/ --step 2         # folder of images, every 2nd frame
  python3 mkvideo.py --demo                   # rebuild the bundled demo clip

It rewrites the DATA block of video.py (or of the file given with -o).
"""
import argparse, os, re, sys
from PIL import Image, ImageDraw, ImageSequence

W, H, MAXLINES = 384, 192, 300
HERE = os.path.dirname(os.path.abspath(__file__))


def ch(v):
    # Same mapping as video.py: ord(c)-35, skipping the backslash (92).
    o = 35 + v
    return chr(o + 1 if o >= 92 else o)


def num(v):
    s = ""
    while v >= 63:
        s += ch(63)
        v -= 63
    return s + ch(v)


def load(src, step, limit):
    if os.path.isdir(src):
        names = sorted(n for n in os.listdir(src) if n.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")))
        frames = [Image.open(os.path.join(src, n)).convert("RGB") for n in names]
    else:
        frames = [f.convert("RGB") for f in ImageSequence.Iterator(Image.open(src))]
    frames = frames[::step]
    return frames[:limit] if limit else frames


def demo():
    # A ball bouncing over a sunset: 4 colours, 60 frames.
    out = []
    for t in range(60):
        im = Image.new("RGB", (96, 48), (20, 24, 60))
        d = ImageDraw.Draw(im)
        d.rectangle((0, 36, 95, 47), fill=(40, 140, 60))
        x = (t * 3) % 160
        x = x if x < 80 else 160 - x
        y = 30 - abs(((t * 2) % 40) - 20) * 3 // 2
        d.ellipse((x + 2, y - 8, x + 14, y + 4), fill=(250, 200, 40))
        out.append(im)
    return out


def fit(img, cw, s):
    cw = min(cw, W // s)
    ch_ = min(H // s, max(1, round(cw * img.height / img.width)))
    return cw, ch_


def quantise(frames, cw, chh, colours):
    small = [f.resize((cw, chh), Image.LANCZOS) for f in frames]
    if colours == 2:
        pal = [(0, 0, 0), (255, 255, 255)]
        idx = [[1 if p >= 128 else 0 for p in f.convert("L").tobytes()] for f in small]
    else:
        # One palette for the whole clip, taken from a strip of sampled frames.
        pick = small[:: max(1, len(small) // 32)]
        strip = Image.new("RGB", (cw, chh * len(pick)))
        for i, f in enumerate(pick):
            strip.paste(f, (0, i * chh))
        pimg = strip.quantize(colours, method=Image.Quantize.FASTOCTREE)
        raw = pimg.getpalette()[: colours * 3]
        pal = [tuple(raw[i:i + 3]) for i in range(0, len(raw), 3)]
        idx = [list(f.quantize(palette=pimg, dither=Image.Dither.NONE).tobytes()) for f in small]
    # Most used colour first: the player starts from a screen filled with P[0].
    count = [0] * len(pal)
    for f in idx:
        for v in f:
            count[v] += 1
    order = sorted((i for i in range(len(pal)) if count[i]), key=lambda i: -count[i])
    remap = {o: n for n, o in enumerate(order)}
    return [pal[o] for o in order], [[remap[v] for v in f] for f in idx]


def encode(idx, ncell):
    cur = [0] * ncell
    out = []
    for f in idx:
        s, pos, i = "", 0, 0
        while i < ncell:
            if f[i] == cur[i]:
                i += 1
                continue
            j = i
            while j < ncell and f[j] != cur[j] and f[j] == f[i]:
                j += 1
            s += num(i - pos) + num(j - i) + ch(f[i])
            pos = i = j
        cur = f
        out.append(s + "!")
    return "".join(out) + "}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", nargs="?", help="GIF/WebP/PNG animation, or a folder of images")
    ap.add_argument("--demo", action="store_true", help="build the bundled bouncing-ball demo")
    ap.add_argument("-w", "--cols", type=int, default=48, help="cells across (default 48)")
    ap.add_argument("-s", "--size", type=int, default=8, help="cell size in pixels (default 8)")
    ap.add_argument("-c", "--colours", type=int, default=2, help="palette size, 2-64 (default 2)")
    ap.add_argument("--step", type=int, default=1, help="keep every Nth frame")
    ap.add_argument("--max", type=int, default=0, help="stop after this many frames")
    ap.add_argument("--line", type=int, default=120, help="characters per data line (default 120)")
    ap.add_argument("-o", "--out", default=os.path.join(HERE, "video.py"), help="player file to rewrite")
    a = ap.parse_args()
    if not (a.demo or a.src) or not 2 <= a.colours <= 64:
        ap.error("give a source (or --demo) and 2-64 colours")

    frames = demo() if a.demo else load(a.src, a.step, a.max)
    if not frames:
        sys.exit("no frames found")
    cw, chh = fit(frames[0], a.cols, a.size)
    pal, idx = quantise(frames, cw, chh, a.colours)
    data = encode(idx, cw * chh)
    lines = [data[i:i + a.line] for i in range(0, len(data), a.line)]
    block = "CW=%d;CH=%d;S=%d;NF=%d\nP=(%s,)\nD=(\n%s)\n" % (
        cw, chh, a.size, len(idx), ",".join("(%d,%d,%d)" % c for c in pal),
        "".join('"%s",\n' % l for l in lines))

    src = open(a.out).read()
    new = re.sub(r"(?s)(#<DATA\n).*?(#DATA>)", lambda m: m.group(1) + block + m.group(2), src)
    total = new.count("\n")
    print("%d frames, %dx%d cells of %dpx, %d colours, %d bytes of data, %d lines"
          % (len(idx), cw, chh, a.size, len(pal), len(data), total))
    if total > MAXLINES:
        sys.exit("too long for the calculator (%d > %d lines): use --step, --max, fewer --cols or a longer --line"
                 % (total, MAXLINES))
    open(a.out, "w").write(new)
    print("wrote", a.out)


if __name__ == "__main__":
    main()
