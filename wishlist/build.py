import os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
S = 2  # supersample
OUT = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.expanduser("~/fonts/PlayfairDisplay-VF.ttf")
SCRIPT = os.path.expanduser("~/fonts/GreatVibes-Regular.ttf")
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
BOW = "/home/claude/oficina-rosa-media/faceless/bow_la_china.png"
DARK = (92, 22, 48)
PINK = (226, 30, 120)
SOFT = (140, 70, 95)

if not os.path.exists(EMOJI):
    import glob
    EMOJI = glob.glob("/usr/share/fonts/**/NotoColorEmoji*.ttf", recursive=True)[0]


def serif(size, weight=700):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def emoji_img(ch, size):
    f = ImageFont.truetype(EMOJI, 109)
    im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
    im = im.crop(im.getbbox())
    r = size / max(im.size)
    return im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)


def vgrad(w, h, top, bot):
    g = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(g)
    for y in range(h):
        t = y / max(1, h - 1)
        d.line([(0, y), (w, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    return g


def base_bg():
    return vgrad(W, H, (246, 226, 232), (236, 200, 214)).convert("RGBA")


def add_bow(im, y=200, w=240):
    if os.path.exists(BOW):
        b = Image.open(BOW).convert("RGBA")
        r = w / b.width
        b = b.resize((w, int(b.height * r)), Image.LANCZOS)
        im.alpha_composite(b, ((W - w) // 2, y))


def footer(im):
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(SCRIPT, 64)
    t = "La China · Oficina Rosita"
    tw = d.textlength(t, font=f)
    d.text(((W - tw) / 2, 1660), t, font=f, fill=DARK)


def centered_lines(im, lines, y0, size=104, gap=22):
    """lines: list of (text, color, emojis_after)"""
    d = ImageDraw.Draw(im)
    f = serif(size)
    y = y0
    for text, color, emos in lines:
        tw = d.textlength(text, font=f)
        esz = int(size * 0.95)
        total = tw + (len(emos) * (esz + 12) + (14 if emos else 0))
        x = (W - total) / 2
        d.text((x, y), text, font=f, fill=color)
        ex = x + tw + 14
        for e in emos:
            ei = emoji_img(e, esz)
            im.alpha_composite(ei, (int(ex), int(y + size * 0.22)))
            ex += esz + 12
        y += size + gap + 20
    return y


def text_scene(lines, sub=None, size=104):
    im = base_bg()
    add_bow(im)
    n = len(lines)
    y0 = 860 - (n * (size + 42)) // 2
    y = centered_lines(im, lines, y0, size)
    if sub:
        d = ImageDraw.Draw(im)
        f = serif(50, 500)
        tw = d.textlength(sub, font=f)
        d.text(((W - tw) / 2, y + 40), sub, font=f, fill=SOFT)
    footer(im)
    return im


# ---------- desk + product illustrations (drawn at 2x) ----------

def desk_canvas():
    w, h = W * S, H * S
    wall = vgrad(w, h, (248, 230, 236), (240, 214, 224)).convert("RGBA")
    d = ImageDraw.Draw(wall)
    top = int(h * 0.60)
    desk = vgrad(w, h - top, (233, 178, 198), (214, 150, 176)).convert("RGBA")
    wall.alpha_composite(desk, (0, top))
    d.rectangle([0, top, w, top + 10 * S], fill=(250, 220, 230))
    # soft window light
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([-300 * S, -200 * S, 700 * S, 800 * S], fill=(255, 255, 255, 70))
    wall.alpha_composite(glow.filter(ImageFilter.GaussianBlur(120 * S)))
    return wall, top


def shadow(im, box, blur=30):
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse(box, fill=(120, 40, 70, 90))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur * S)))


def vase(im, x, base_y):
    d = ImageDraw.Draw(im)
    shadow(im, [x - 70 * S, base_y - 20 * S, x + 70 * S, base_y + 20 * S], 14)
    # stems
    for dx, top in [(-30, 360), (0, 420), (35, 380)]:
        d.line([(x, base_y - 120 * S), (x + dx * S, base_y - top * S)], fill=(120, 150, 110), width=5 * S)
    for dx, top, c in [(-30, 360, (245, 160, 190)), (0, 420, (255, 196, 214)), (35, 380, (236, 120, 160))]:
        cx, cy = x + dx * S, base_y - top * S
        for ox, oy in [(-22, 0), (22, 0), (0, -22), (0, 22)]:
            d.ellipse([cx + ox * S - 26 * S, cy + oy * S - 26 * S, cx + ox * S + 26 * S, cy + oy * S + 26 * S], fill=c)
        d.ellipse([cx - 14 * S, cy - 14 * S, cx + 14 * S, cy + 14 * S], fill=(255, 236, 200))
    d.rounded_rectangle([x - 55 * S, base_y - 150 * S, x + 55 * S, base_y], radius=40 * S, fill=(255, 245, 248))
    d.rounded_rectangle([x - 40 * S, base_y - 140 * S, x - 25 * S, base_y - 30 * S], radius=8 * S, fill=(255, 255, 255))


def tumbler(im, cx, base_y):
    d = ImageDraw.Draw(im)
    hgt, wt, wb = 640 * S, 300 * S, 220 * S
    top = base_y - hgt
    shadow(im, [cx - 200 * S, base_y - 30 * S, cx + 230 * S, base_y + 30 * S])
    # handle
    d.rounded_rectangle([cx + 80 * S, top + 140 * S, cx + 250 * S, top + 470 * S], radius=70 * S, outline=(214, 92, 140), width=46 * S)
    # body (tapered)
    body = Image.new("RGBA", im.size, (0, 0, 0, 0))
    bd = ImageDraw.Draw(body)
    bd.polygon([(cx - wt // 2, top + 110 * S), (cx + wt // 2, top + 110 * S), (cx + wb // 2, base_y), (cx - wb // 2, base_y)], fill=(236, 110, 160))
    # highlight stripe
    bd.polygon([(cx - wt // 2 + 40 * S, top + 130 * S), (cx - wt // 2 + 80 * S, top + 130 * S), (cx - wb // 2 + 70 * S, base_y - 20 * S), (cx - wb // 2 + 40 * S, base_y - 20 * S)], fill=(250, 170, 205))
    bd.polygon([(cx + wt // 2 - 50 * S, top + 130 * S), (cx + wt // 2 - 30 * S, top + 130 * S), (cx + wb // 2 - 20 * S, base_y - 20 * S), (cx + wb // 2 - 35 * S, base_y - 20 * S)], fill=(214, 84, 138))
    im.alpha_composite(body)
    d = ImageDraw.Draw(im)
    # straw
    d.rounded_rectangle([cx + 20 * S, top - 170 * S, cx + 46 * S, top + 40 * S], radius=12 * S, fill=(255, 230, 240))
    d.line([(cx + 33 * S, top - 170 * S), (cx + 90 * S, top - 230 * S)], fill=(255, 230, 240), width=26 * S)
    # lid
    d.rounded_rectangle([cx - wt // 2 - 14 * S, top + 40 * S, cx + wt // 2 + 14 * S, top + 120 * S], radius=24 * S, fill=(250, 238, 242))
    d.rounded_rectangle([cx - wt // 2 + 10 * S, top, cx + wt // 2 - 10 * S, top + 60 * S], radius=24 * S, fill=(255, 248, 250))
    # little heart decal
    hx, hy = cx - 10 * S, top + 330 * S
    d.ellipse([hx - 40 * S, hy - 30 * S, hx, hy + 10 * S], fill=(255, 236, 244))
    d.ellipse([hx - 4 * S, hy - 30 * S, hx + 36 * S, hy + 10 * S], fill=(255, 236, 244))
    d.polygon([(hx - 38 * S, hy - 2 * S), (hx + 34 * S, hy - 2 * S), (hx - 2 * S, hy + 44 * S)], fill=(255, 236, 244))


def keyboard(im, cx, base_y):
    d = ImageDraw.Draw(im)
    kw, kh = 620 * S, 240 * S
    x0, y0 = cx - kw // 2 - 120 * S, base_y - kh
    shadow(im, [x0 - 20 * S, base_y - 40 * S, x0 + kw + 20 * S, base_y + 40 * S])
    d.rounded_rectangle([x0, y0, x0 + kw, base_y], radius=34 * S, fill=(244, 150, 186))
    d.rounded_rectangle([x0 + 10 * S, y0 + 8 * S, x0 + kw - 10 * S, base_y - 14 * S], radius=28 * S, fill=(250, 186, 210))
    cols, rows = 13, 4
    pad = 26 * S
    kwid = (kw - 2 * pad) / cols
    khei = (kh - 2 * pad) / (rows + 1)
    for r in range(rows):
        for c in range(cols):
            kx = x0 + pad + c * kwid
            ky = y0 + pad + r * khei
            d.rounded_rectangle([kx + 5 * S, ky + 5 * S, kx + kwid - 5 * S, ky + khei - 6 * S], radius=12 * S, fill=(255, 240, 246))
    # space row
    ky = y0 + pad + rows * khei
    for c, span in [(0, 2), (2, 1), (3, 6), (9, 1), (10, 3)]:
        kx = x0 + pad + c * kwid
        d.rounded_rectangle([kx + 5 * S, ky + 5 * S, kx + span * kwid - 5 * S, ky + khei - 6 * S], radius=12 * S, fill=(255, 240, 246))
    # mouse
    mx = x0 + kw + 100 * S
    shadow(im, [mx - 80 * S, base_y - 30 * S, mx + 80 * S, base_y + 30 * S], 18)
    d.ellipse([mx - 75 * S, base_y - 230 * S, mx + 75 * S, base_y], fill=(244, 150, 186))
    d.ellipse([mx - 62 * S, base_y - 220 * S, mx + 62 * S, base_y - 12 * S], fill=(250, 186, 210))
    d.line([(mx, base_y - 220 * S), (mx, base_y - 140 * S)], fill=(230, 130, 170), width=5 * S)
    d.rounded_rectangle([mx - 8 * S, base_y - 200 * S, mx + 8 * S, base_y - 160 * S], radius=8 * S, fill=(255, 240, 246))


def planner(im, cx, base_y):
    d = ImageDraw.Draw(im)
    pw, ph = 470 * S, 640 * S
    x0, y0 = cx - pw // 2, base_y - ph
    shadow(im, [x0 - 30 * S, base_y - 40 * S, x0 + pw + 40 * S, base_y + 40 * S])
    d.rounded_rectangle([x0 + 18 * S, y0 + 14 * S, x0 + pw + 14 * S, base_y + 6 * S], radius=20 * S, fill=(255, 250, 246))
    d.rounded_rectangle([x0, y0, x0 + pw, base_y], radius=22 * S, fill=(240, 128, 170))
    d.rounded_rectangle([x0 + 70 * S, y0 + 30 * S, x0 + pw - 30 * S, base_y - 30 * S], radius=16 * S, outline=(255, 214, 230), width=4 * S)
    # spiral
    for i in range(14):
        yy = y0 + 40 * S + i * 42 * S
        d.ellipse([x0 - 20 * S, yy, x0 + 40 * S, yy + 26 * S], outline=(235, 225, 230), width=8 * S)
    # elastic band
    d.rectangle([x0 + pw - 70 * S, y0, x0 + pw - 52 * S, base_y], fill=(200, 70, 120))
    # label
    lx0, ly0, lx1, ly1 = x0 + 120 * S, y0 + 200 * S, x0 + pw - 80 * S, y0 + 330 * S
    d.rounded_rectangle([lx0, ly0, lx1, ly1], radius=20 * S, fill=(255, 245, 248))
    f = serif(58 * S, 700)
    t = "planner"
    tw = d.textlength(t, font=f)
    d.text(((lx0 + lx1) / 2 - tw / 2, ly0 + 22 * S), t, font=f, fill=(200, 60, 115))
    # flower
    fx, fy = (lx0 + lx1) // 2, y0 + 470 * S
    for ox, oy in [(-30, 0), (30, 0), (0, -30), (0, 30)]:
        d.ellipse([fx + ox * S - 34 * S, fy + oy * S - 34 * S, fx + ox * S + 34 * S, fy + oy * S + 34 * S], fill=(255, 210, 226))
    d.ellipse([fx - 20 * S, fy - 20 * S, fx + 20 * S, fy + 20 * S], fill=(255, 236, 200))
    # pen
    d.rounded_rectangle([x0 + pw + 60 * S, base_y - 520 * S, x0 + pw + 90 * S, base_y - 20 * S], radius=14 * S, fill=(255, 245, 248))
    d.polygon([(x0 + pw + 60 * S, base_y - 20 * S), (x0 + pw + 90 * S, base_y - 20 * S), (x0 + pw + 75 * S, base_y + 30 * S)], fill=(230, 160, 120))


def product_scene(draw_fn, tag_top, tag_name):
    big, top = desk_canvas()
    base_y = top + 260 * S
    vase(big, int(W * S * 0.87), top + 120 * S)
    draw_fn(big, int(W * S * 0.47), base_y)
    im = big.resize((W, H), Image.LANCZOS)
    add_bow(im, 150, 180)
    d = ImageDraw.Draw(im)
    # tag pill
    f1 = serif(46, 600)
    f2 = serif(78, 800)
    t1w = d.textlength(tag_top, font=f1)
    t2w = d.textlength(tag_name, font=f2)
    pw = max(t1w, t2w) + 120
    px0 = (W - pw) / 2
    d.rounded_rectangle([px0, 380, px0 + pw, 590], radius=50, fill=(255, 247, 250))
    d.text(((W - t1w) / 2, 410), tag_top, font=f1, fill=SOFT)
    d.text(((W - t2w) / 2, 470), tag_name, font=f2, fill=PINK)
    fs = serif(34, 500)
    note = "Imagen ilustrativa. El producto real está en el link."
    nw = d.textlength(note, font=fs)
    d.text(((W - nw) / 2, 1560), note, font=fs, fill=(110, 50, 75))
    footer(im)
    return im


REELS = [
    ("W1_tumbler_rosa", [("Mi cafecito", DARK, []), ("merece", PINK, []), ("casa nueva.", PINK, ["😂", "☕"])], tumbler, "Tumbler rosa 40 oz"),
    ("W2_teclado_rosa", [("Si voy a trabajar,", DARK, []), ("que por lo menos", PINK, []), ("se vea bonito.", PINK, ["💗"])], keyboard, "Teclado y mouse rosa"),
    ("W3_planner_rosa", [("Este año sí", DARK, []), ("me organizo.", DARK, []), ("Otra vez.", PINK, ["😂", "🙏🏽"])], planner, "Planner rosa"),
]

CTA = [("¿Lo compro", DARK, []), ("o no?", PINK, ["🤔"])]
CTA_SUB = "Te dejo el link en el reel. Dime abajo."


def render(name, hook, fn, pname):
    d = os.path.join(OUT, name)
    os.makedirs(d, exist_ok=True)
    s1 = text_scene(hook, size=100 if len(hook) > 2 else 108)
    s2 = product_scene(fn, "Wishlist de la Oficina Rosita", pname)
    s3 = text_scene(CTA, sub=CTA_SUB, size=120)
    paths = []
    for i, s in enumerate([s1, s2, s3], 1):
        p = os.path.join(d, f"s{i}.png")
        s.convert("RGB").save(p)
        paths.append(p)
    durs = [3.0, 4.0, 3.0]
    fps = 30
    inputs, filt = [], []
    for i, (p, du) in enumerate(zip(paths, durs)):
        inputs += ["-loop", "1", "-t", str(du + 0.5), "-i", p]
        n = int((du + 0.5) * fps)
        z = "1+0.0006*on" if i != 1 else "1.0+0.0012*on"
        filt.append(f"[{i}:v]scale=2160:3840,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=1080x1920:fps={fps},format=yuv420p,setsar=1[v{i}]")
    filt.append(f"[v0][v1]xfade=transition=fade:duration=0.5:offset={durs[0]}[a1]")
    filt.append(f"[a1][v2]xfade=transition=fade:duration=0.5:offset={durs[0]+durs[1]}[vout]")
    out = os.path.join(OUT, f"{name}.mp4")
    cmd = ["ffmpeg", "-y", "-v", "error", *inputs, "-f", "lavfi", "-t", str(sum(durs) + 0.5), "-i", "anullsrc=r=44100:cl=stereo",
           "-filter_complex", ";".join(filt), "-map", "[vout]", "-map", "3:a", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-c:a", "aac", "-shortest", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    print("built", out)


if __name__ == "__main__":
    for r in REELS:
        render(*r)
