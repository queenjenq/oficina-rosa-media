"""Regalitos para la comadre (December gift reels): candle, block calendar, slippers, phone stand, pens, blanket."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B
from PIL import ImageDraw

S = B.S
ROSE = (240, 128, 170)
ROSE_L = (252, 196, 216)
CREAM = (255, 244, 248)


def heart(d, hx, hy, r, c):
    d.ellipse([hx - 2 * r, hy - r * 1.6, hx, hy + r * 0.4], fill=c)
    d.ellipse([hx - r * 0.1, hy - r * 1.6, hx + r * 1.9, hy + r * 0.4], fill=c)
    d.polygon([(hx - 1.95 * r, hy - 0.3 * r), (hx + 1.85 * r, hy - 0.3 * r), (hx - 0.05 * r, hy + 2.2 * r)], fill=c)


def candle(im, cx, base_y):
    d = ImageDraw.Draw(im)
    w, h = 360 * S, 420 * S
    x0, y0 = cx - w // 2, base_y - h
    B.shadow(im, [x0 - 30 * S, base_y - 30 * S, x0 + w + 30 * S, base_y + 36 * S])
    # glass jar
    d.rounded_rectangle([x0, y0, x0 + w, base_y], radius=60 * S, fill=(246, 170, 198))
    d.rounded_rectangle([x0 + 18 * S, y0 + 60 * S, x0 + w - 18 * S, base_y - 18 * S], radius=48 * S, fill=(250, 190, 212))
    d.rounded_rectangle([x0 + 34 * S, y0 + 80 * S, x0 + 64 * S, base_y - 60 * S], radius=14 * S, fill=(255, 226, 236))
    # label
    d.rounded_rectangle([x0 + 70 * S, y0 + 170 * S, x0 + w - 70 * S, y0 + 300 * S], radius=18 * S, fill=CREAM)
    heart(d, cx + 4 * S, y0 + 232 * S, 18 * S, (226, 30, 120))
    # wax top + wick + flame
    d.ellipse([x0 + 20 * S, y0 + 10 * S, x0 + w - 20 * S, y0 + 80 * S], fill=(255, 236, 242))
    d.line([(cx, y0 + 45 * S), (cx, y0 - 10 * S)], fill=(80, 50, 50), width=6 * S)
    d.ellipse([cx - 26 * S, y0 - 100 * S, cx + 26 * S, y0 - 8 * S], fill=(255, 200, 90))
    d.ellipse([cx - 13 * S, y0 - 66 * S, cx + 13 * S, y0 - 16 * S], fill=(255, 246, 210))


def block_calendar(im, cx, base_y):
    d = ImageDraw.Draw(im)
    bw, bh = 560 * S, 70 * S
    x0 = cx - bw // 2 - 30 * S
    B.shadow(im, [x0 - 20 * S, base_y - 30 * S, x0 + bw + 20 * S, base_y + 36 * S])
    d.rounded_rectangle([x0, base_y - bh, x0 + bw, base_y], radius=20 * S, fill=ROSE)
    # two number cubes + month block
    f = B.serif(150 * S, 800)
    for i, n in enumerate(["2", "7"]):
        cx0 = x0 + 40 * S + i * 190 * S
        d.rounded_rectangle([cx0, base_y - bh - 180 * S, cx0 + 170 * S, base_y - bh + 6 * S], radius=22 * S, fill=CREAM)
        tw = d.textlength(n, font=f)
        d.text((cx0 + 85 * S - tw / 2, base_y - bh - 200 * S), n, font=f, fill=(226, 30, 120))
    mx0 = x0 + 420 * S
    d.rounded_rectangle([mx0, base_y - bh - 120 * S, mx0 + 120 * S, base_y - bh + 6 * S], radius=18 * S, fill=ROSE_L)
    fm = B.serif(46 * S, 700)
    tw = d.textlength("ENE", font=fm)
    d.text((mx0 + 60 * S - tw / 2, base_y - bh - 96 * S), "ENE", font=fm, fill=(118, 32, 61))
    # little bow on top
    bx, by = x0 + 95 * S, base_y - bh - 190 * S
    d.polygon([(bx, by), (bx - 60 * S, by - 34 * S), (bx - 60 * S, by + 34 * S)], fill=(226, 30, 120))
    d.polygon([(bx, by), (bx + 60 * S, by - 34 * S), (bx + 60 * S, by + 34 * S)], fill=(226, 30, 120))
    d.ellipse([bx - 16 * S, by - 16 * S, bx + 16 * S, by + 16 * S], fill=(200, 20, 100))


def slippers(im, cx, base_y):
    d = ImageDraw.Draw(im)
    for i, dx in enumerate([-170, 170]):
        sx = cx + dx * S - 40 * S
        B.shadow(im, [sx - 130 * S, base_y - 30 * S, sx + 130 * S, base_y + 30 * S], 20)
        # sole
        d.ellipse([sx - 120 * S, base_y - 80 * S, sx + 120 * S, base_y + 6 * S], fill=(236, 120, 160))
        # fuzzy cross bands: cluster of circles
        for j in range(16):
            ox = -100 + (j % 8) * 28
            oy = -150 + (j // 8) * 46
            d.ellipse([sx + ox * S - 34 * S, base_y + oy * S - 34 * S, sx + ox * S + 34 * S, base_y + oy * S + 34 * S], fill=(250, 186, 210) if (j % 3) else (255, 210, 228))


def phone_stand(im, cx, base_y):
    d = ImageDraw.Draw(im)
    B.shadow(im, [cx - 200 * S, base_y - 30 * S, cx + 200 * S, base_y + 36 * S])
    # base
    d.rounded_rectangle([cx - 180 * S, base_y - 40 * S, cx + 180 * S, base_y], radius=18 * S, fill=(236, 150, 170))
    # arm
    d.polygon([(cx - 30 * S, base_y - 40 * S), (cx + 30 * S, base_y - 40 * S), (cx + 90 * S, base_y - 300 * S), (cx + 40 * S, base_y - 310 * S)], fill=(230, 140, 162))
    # phone (tilted rectangle)
    ph = [(cx - 160 * S, base_y - 120 * S), (cx + 40 * S, base_y - 80 * S), (cx + 150 * S, base_y - 560 * S), (cx - 50 * S, base_y - 600 * S)]
    d.polygon(ph, fill=(60, 40, 50))
    inner = [(cx - 140 * S, base_y - 132 * S), (cx + 30 * S, base_y - 98 * S), (cx + 128 * S, base_y - 548 * S), (cx - 42 * S, base_y - 582 * S)]
    d.polygon(inner, fill=(252, 210, 226))
    # chat bubbles on screen
    for k, (ox, oy, c) in enumerate([(-60, -470, (255, 255, 255)), (0, -390, (236, 110, 160)), (-80, -300, (255, 255, 255)), (-20, -220, (236, 110, 160))]):
        d.rounded_rectangle([cx + ox * S, base_y + oy * S, cx + (ox + 110) * S, base_y + (oy + 44) * S], radius=20 * S, fill=c)


def pens(im, cx, base_y):
    d = ImageDraw.Draw(im)
    B.shadow(im, [cx - 300 * S, base_y - 30 * S, cx + 300 * S, base_y + 36 * S])
    cols = [(236, 110, 160), (250, 186, 210), (226, 30, 120), (255, 214, 228), (240, 140, 178), (200, 70, 120)]
    for i, c in enumerate(cols):
        x = cx - 260 * S + i * 95 * S
        top = base_y - (420 + (i % 3) * 40) * S
        d.rounded_rectangle([x, top, x + 50 * S, base_y - 10 * S], radius=22 * S, fill=c)
        d.rounded_rectangle([x, top, x + 50 * S, top + 110 * S], radius=22 * S, fill=CREAM)
        d.rectangle([x + 34 * S, top + 20 * S, x + 44 * S, top + 160 * S], fill=(255, 255, 255))
        d.polygon([(x + 8 * S, base_y - 10 * S), (x + 42 * S, base_y - 10 * S), (x + 25 * S, base_y + 26 * S)], fill=(90, 60, 70))
    # ribbon around the set
    d.rectangle([cx - 280 * S, base_y - 200 * S, cx + 290 * S, base_y - 160 * S], fill=(255, 244, 248))
    heart(d, cx + 10 * S, base_y - 186 * S, 16 * S, (226, 30, 120))


def blanket(im, cx, base_y):
    d = ImageDraw.Draw(im)
    w = 620 * S
    x0 = cx - w // 2
    B.shadow(im, [x0 - 20 * S, base_y - 30 * S, x0 + w + 20 * S, base_y + 40 * S])
    layers = [(246, 170, 198), (240, 150, 184), (246, 170, 198), (236, 140, 176)]
    for i, c in enumerate(layers):
        y1 = base_y - i * 90 * S
        d.rounded_rectangle([x0 + i * 6 * S, y1 - 100 * S, x0 + w - i * 6 * S, y1], radius=48 * S, fill=c)
        for k in range(10):
            xx = x0 + 50 * S + k * 56 * S
            d.line([(xx, y1 - 80 * S), (xx, y1 - 20 * S)], fill=(250, 196, 216), width=6 * S)
    # gift tag
    tx, ty = x0 + w - 60 * S, base_y - 380 * S
    d.rounded_rectangle([tx - 70 * S, ty, tx + 70 * S, ty + 100 * S], radius=14 * S, fill=CREAM)
    heart(d, tx, ty + 46 * S, 16 * S, (226, 30, 120))
    d.line([(tx, ty), (tx - 60 * S, ty - 60 * S)], fill=(226, 30, 120), width=6 * S)


DARK, PINK = B.DARK, B.PINK
TAG = "Regalitos para la comadre"

REELS = [
    ("G1_velita_rosa", [("Para la comadre que", DARK, []), ("trabaja desde casa:", DARK, []), ("paz y velita.", PINK, ["🕯", "💗"])], candle, "Velita Pink Sands"),
    ("G2_calendario_rosa", [("2027 ya viene.", DARK, []), ("Que nos agarre", PINK, []), ("organizadas.", PINK, ["😂", "🙏🏽"])], block_calendar, "Calendario rosa"),
    ("G3_pantuflas_rosas", [("Dress code de", DARK, []), ("home office:", DARK, []), ("pantuflas rosas.", PINK, ["😂"])], slippers, "Pantuflas rosas"),
    ("G4_porta_celular", [("Para la que vive", DARK, []), ("pegada al", PINK, []), ("teléfono.", PINK, ["📱", "😂"])], phone_stand, "Porta celular rosa"),
    ("G5_plumas_rosas", [("Plumas bonitas,", DARK, []), ("firmas bonitas.", PINK, ["💗"])], pens, "Plumas rosas"),
    ("G6_cobijita_rosa", [("¿Hace frío", DARK, []), ("en la oficina?", DARK, []), ("Cobijita rosa.", PINK, ["🥶", "💗"])], blanket, "Cobijita rosa"),
]

B.CTA = [("¿Se lo regalo", DARK, []), ("o me lo quedo?", PINK, ["😂"])]


def render(name, hook, fn, pname):
    orig = B.product_scene
    B.product_scene = lambda f, top, n: orig(f, TAG, n)
    try:
        B.render(name, hook, fn, pname)
    finally:
        B.product_scene = orig


if __name__ == "__main__":
    for r in (REELS if len(sys.argv) < 2 else [x for x in REELS if x[0] in sys.argv[1:]]):
        render(*r)
