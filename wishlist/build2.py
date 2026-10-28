"""Wishlist reels batch 2: mug warmer, vanity mirror, desk organizer."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B
from PIL import ImageDraw

S = B.S


def mug_warmer(im, cx, base_y):
    d = ImageDraw.Draw(im)
    # warmer pad
    pw, ph = 460 * S, 70 * S
    B.shadow(im, [cx - pw // 2 - 20 * S, base_y - 30 * S, cx + pw // 2 + 20 * S, base_y + 40 * S])
    d.rounded_rectangle([cx - pw // 2, base_y - ph, cx + pw // 2, base_y], radius=34 * S, fill=(244, 150, 186))
    d.rounded_rectangle([cx - pw // 2 + 14 * S, base_y - ph + 8 * S, cx + pw // 2 - 14 * S, base_y - ph + 30 * S], radius=12 * S, fill=(252, 196, 216))
    # tiny glowing light
    d.ellipse([cx + pw // 2 - 70 * S, base_y - 48 * S, cx + pw // 2 - 46 * S, base_y - 24 * S], fill=(255, 238, 180))
    # mug
    mw, mh = 300 * S, 340 * S
    mx0, my1 = cx - mw // 2 - 20 * S, base_y - ph + 6 * S
    my0 = my1 - mh
    d.rounded_rectangle([mx0 + mw - 30 * S, my0 + 70 * S, mx0 + mw + 110 * S, my0 + 250 * S], radius=70 * S, outline=(255, 244, 248), width=36 * S)
    d.rounded_rectangle([mx0, my0, mx0 + mw, my1], radius=40 * S, fill=(255, 244, 248))
    d.rounded_rectangle([mx0 + 26 * S, my0 + 20 * S, mx0 + 56 * S, my1 - 30 * S], radius=14 * S, fill=(255, 255, 255))
    d.ellipse([mx0 + 10 * S, my0 - 26 * S, mx0 + mw - 10 * S, my0 + 30 * S], fill=(140, 86, 70))
    # heart on mug
    hx, hy = mx0 + mw // 2 + 10 * S, my0 + 170 * S
    c = (236, 110, 160)
    d.ellipse([hx - 44 * S, hy - 34 * S, hx, hy + 10 * S], fill=c)
    d.ellipse([hx - 4 * S, hy - 34 * S, hx + 40 * S, hy + 10 * S], fill=c)
    d.polygon([(hx - 42 * S, hy - 4 * S), (hx + 38 * S, hy - 4 * S), (hx - 2 * S, hy + 48 * S)], fill=c)
    # steam
    for i, dx in enumerate([-60, 0, 60]):
        x = mx0 + mw // 2 + dx * S
        pts = [(x + (18 * S if j % 2 else -18 * S), my0 - 50 * S - j * 50 * S) for j in range(4)]
        d.line(pts, fill=(255, 255, 255), width=12 * S, joint="curve")


def vanity_mirror(im, cx, base_y):
    d = ImageDraw.Draw(im)
    mw, mh = 520 * S, 640 * S
    x0, y1 = cx - mw // 2, base_y - 70 * S
    y0 = y1 - mh
    B.shadow(im, [cx - 220 * S, base_y - 30 * S, cx + 220 * S, base_y + 36 * S])
    # stand
    d.rounded_rectangle([cx - 30 * S, y1 - 10 * S, cx + 30 * S, base_y - 40 * S], radius=10 * S, fill=(240, 140, 178))
    d.rounded_rectangle([cx - 200 * S, base_y - 60 * S, cx + 200 * S, base_y], radius=30 * S, fill=(240, 140, 178))
    # frame + glass
    d.rounded_rectangle([x0, y0, x0 + mw, y1], radius=46 * S, fill=(244, 150, 186))
    d.rounded_rectangle([x0 + 34 * S, y0 + 34 * S, x0 + mw - 34 * S, y1 - 34 * S], radius=30 * S, fill=(236, 232, 240))
    d.polygon([(x0 + 70 * S, y0 + 60 * S), (x0 + 180 * S, y0 + 60 * S), (x0 + 60 * S, y0 + 260 * S)], fill=(250, 250, 255))
    # bulbs
    for i in range(6):
        yy = y0 + 70 * S + i * 100 * S
        for xx in (x0 + 17 * S, x0 + mw - 17 * S):
            d.ellipse([xx - 15 * S, yy - 15 * S, xx + 15 * S, yy + 15 * S], fill=(255, 246, 214))
    for i in range(4):
        xx = x0 + 110 * S + i * 100 * S
        d.ellipse([xx - 15 * S, y0 + 2 * S, xx + 15 * S, y0 + 32 * S], fill=(255, 246, 214))


def desk_organizer(im, cx, base_y):
    d = ImageDraw.Draw(im)
    ow, oh = 600 * S, 300 * S
    x0, y0 = cx - ow // 2 - 40 * S, base_y - oh
    B.shadow(im, [x0 - 20 * S, base_y - 34 * S, x0 + ow + 20 * S, base_y + 40 * S])
    # pens + scissors sticking out of top cups
    for i, (dx, col, h) in enumerate([(60, (255, 214, 120), 260), (100, (130, 180, 230), 300), (140, (236, 110, 160), 240), (420, (255, 244, 248), 200), (470, (200, 160, 230), 230)]):
        d.rounded_rectangle([x0 + dx * S, y0 - h * S, x0 + (dx + 22) * S, y0 + 40 * S], radius=10 * S, fill=col)
    # cups on top
    d.rounded_rectangle([x0 + 30 * S, y0 - 120 * S, x0 + 200 * S, y0 + 10 * S], radius=18 * S, fill=(240, 128, 170))
    d.rounded_rectangle([x0 + 390 * S, y0 - 90 * S, x0 + 540 * S, y0 + 10 * S], radius=18 * S, fill=(240, 128, 170))
    # body with drawers
    d.rounded_rectangle([x0, y0, x0 + ow, base_y], radius=26 * S, fill=(244, 150, 186))
    for r in range(3):
        dy0 = y0 + 24 * S + r * 90 * S
        d.rounded_rectangle([x0 + 24 * S, dy0, x0 + ow - 24 * S, dy0 + 74 * S], radius=16 * S, fill=(252, 196, 216))
        d.rounded_rectangle([x0 + ow // 2 - 50 * S, dy0 + 28 * S, x0 + ow // 2 + 50 * S, dy0 + 46 * S], radius=9 * S, fill=(255, 244, 248))
    # sticky notes beside
    sx = x0 + ow + 50 * S
    d.rounded_rectangle([sx, base_y - 130 * S, sx + 140 * S, base_y - 10 * S], radius=10 * S, fill=(255, 236, 160))
    d.rounded_rectangle([sx + 20 * S, base_y - 150 * S, sx + 160 * S, base_y - 30 * S], radius=10 * S, fill=(255, 214, 230))


DARK, PINK = B.DARK, B.PINK

REELS = [
    ("W4_calentador_taza", [("Mi cafecito se enfría", DARK, []), ("más rápido que", PINK, []), ("mi paciencia.", PINK, ["☕", "😂"])], mug_warmer, "Calentador de taza"),
    ("W5_espejo_luz", [("Mi cara a las 6 AM", DARK, []), ("necesita", PINK, []), ("buena luz.", PINK, ["😂", "💡"])], vanity_mirror, "Espejo con luz rosa"),
    ("W6_organizador_rosa", [("Mi escritorio:", DARK, []), ("organizado.", PINK, []), ("Mi vida:", DARK, []), ("en proceso.", DARK, ["🙏🏽"])], desk_organizer, "Organizador rosa"),
]

if __name__ == "__main__":
    for r in (REELS if len(sys.argv) < 2 else [x for x in REELS if x[0] in sys.argv[1:]]):
        B.render(*r)
