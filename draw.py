#!/usr/bin/env python3
"""Draw the entry image for make.fun bounty news-image-20261119.

Deterministic newspaper-style infographic (1024x1024) summing up the
world news of Thursday 19 November 2026. No network, no randomness,
no timestamps: the same run always writes the same bytes.

Run:  python3 draw.py            (writes entry.png next to this file)
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))

PAPER = (253, 252, 247)   # warm paper white
INK = (18, 18, 18)        # near-black text
RED = (178, 34, 34)       # accent red (masthead rules, labels)
GRAY = (96, 96, 96)       # secondary text
LIGHT = (238, 236, 229)   # "also today" strip background
RULE = (205, 202, 193)    # hairline gray

FONT_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FONT_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w):
    """Greedy word wrap to a pixel width."""
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if fnt.getlength(t) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def center(draw, y, text, fnt, fill):
    x = (W - draw.textlength(text, font=fnt)) / 2
    draw.text((x, y), text, font=fnt, fill=fill)
    return y + fnt.size


# ---------------------------------------------------------------- icons
def icon_globe(d, x, y, s, c):
    d.ellipse([x, y, x + s, y + s], outline=c, width=4)
    d.ellipse([x + s * 0.28, y, x + s * 0.72, y + s], outline=c, width=3)
    d.line([x, y + s * 0.5, x + s, y + s * 0.5], fill=c, width=3)
    d.arc([x, y + s * 0.18, x + s, y + s * 0.82], 200, 340, fill=c, width=3)
    d.arc([x, y + s * 0.18, x + s, y + s * 0.82], 20, 160, fill=c, width=3)


def icon_burst(d, x, y, s, c):
    cx, cy = x + s / 2, y + s / 2
    pts = []
    import math
    for i in range(16):
        r = s * 0.5 if i % 2 == 0 else s * 0.22
        a = math.pi * i / 8 - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=c)
    d.ellipse([cx - s * 0.10, cy - s * 0.10, cx + s * 0.10, cy + s * 0.10],
              fill=PAPER)


def icon_bridge(d, x, y, s, c):
    d.arc([x, y + s * 0.15, x + s, y + s * 1.05], 180, 360, fill=c, width=5)
    d.line([x, y + s * 0.62, x + s, y + s * 0.62], fill=c, width=5)
    for fx in (0.22, 0.5, 0.78):
        d.line([x + s * fx, y + s * 0.30, x + s * fx, y + s * 0.62],
               fill=c, width=4)
    d.line([x + s * 0.5, y + s * 0.05, x + s * 0.5, y + s * 0.30],
           fill=c, width=4)


def icon_tank(d, x, y, s, c):
    d.rectangle([x + s * 0.08, y + s * 0.52, x + s * 0.92, y + s * 0.82],
                outline=c, width=4)
    for wx in (0.22, 0.42, 0.62, 0.80):
        d.ellipse([x + s * (wx - 0.07), y + s * 0.60,
                   x + s * (wx + 0.07), y + s * 0.74], fill=c)
    d.rectangle([x + s * 0.28, y + s * 0.32, x + s * 0.62, y + s * 0.52],
                fill=c)
    d.line([x + s * 0.62, y + s * 0.40, x + s * 0.95, y + s * 0.40],
           fill=c, width=5)


def icon_scales(d, x, y, s, c):
    d.line([x + s * 0.5, y + s * 0.08, x + s * 0.5, y + s * 0.92],
           fill=c, width=4)
    d.line([x + s * 0.12, y + s * 0.22, x + s * 0.88, y + s * 0.22],
           fill=c, width=4)
    d.line([x + s * 0.08, y + s * 0.92, x + s * 0.92, y + s * 0.92],
           fill=c, width=4)
    for fx in (0.16, 0.84):
        d.line([x + s * fx, y + s * 0.22, x + s * fx, y + s * 0.42],
               fill=c, width=3)
        d.polygon([(x + s * (fx - 0.14), y + s * 0.42),
                   (x + s * (fx + 0.14), y + s * 0.42),
                   (x + s * fx, y + s * 0.62)], outline=c, width=3)


def icon_frame(d, x, y, s, c):
    d.rectangle([x + s * 0.08, y + s * 0.08, x + s * 0.92, y + s * 0.92],
                outline=c, width=5)
    d.ellipse([x + s * 0.32, y + s * 0.24, x + s * 0.68, y + s * 0.60],
              fill=c)
    d.line([x + s * 0.5, y + s * 0.60, x + s * 0.5, y + s * 0.86],
           fill=c, width=4)
    d.line([x + s * 0.5, y + s * 0.86, x + s * 0.32, y + s * 0.78],
           fill=c, width=3)
    d.line([x + s * 0.5, y + s * 0.86, x + s * 0.68, y + s * 0.78],
           fill=c, width=3)


# ---------------------------------------------------------------- content
STORIES = [
    ("SUMMIT", icon_globe,
     "Trump, Xi & Putin meet in Shenzhen",
     "First three-way summit: nuclear arms control, Ukraine and Iran."),
    ("CONFLICT", icon_burst,
     "U.S. strikes Iran missile site",
     "Tehran hits back with drones on a Kuwait air base; Bahrain intercepts."),
    ("UKRAINE", icon_bridge,
     "Crimea Bridge hit again",
     "Traffic closed as the damage from the latest attack is assessed."),
    ("GAZA", icon_tank,
     "Israeli tanks cross Gaza ceasefire line",
     "Rare ground operation pushes beyond the truce boundary."),
    ("JUSTICE", icon_scales,
     "Myanmar faces genocide verdict",
     "Historic world court ruling over the Rohingya at The Hague."),
    ("CULTURE", icon_frame,
     "Van Gogh sells for $190.4m",
     "Record price after a Nazi-era ownership dispute is settled."),
]

ALSO_TODAY = (
    "Anthropic, maker of Claude, prepares a $1.4 trillion IPO.  "
    "GTA VI begins its global rollout.  "
    "NASA's Voyager 1 passes one light-day from Earth."
)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_kicker = font(FONT_SANS_B, 20)
    f_title = font(FONT_SERIF_B, 66)
    f_sub = font(FONT_SERIF, 20)
    f_label = font(FONT_SANS_B, 15)
    f_head = font(FONT_SANS_B, 27)
    f_cap = font(FONT_SANS, 18)
    f_also = font(FONT_SANS, 18)
    f_also_b = font(FONT_SANS_B, 18)
    f_foot = font(FONT_SANS, 13)

    # ---- masthead
    y = 30
    y = center(d, y, "THE WORLD IN ONE DAY", f_kicker, RED)
    y = center(d, y + 6, "19 NOVEMBER 2026", f_title, INK)
    y = center(d, y + 2, "Thursday  \u2022  Six stories that defined the day",
               f_sub, GRAY)
    d.line([36, 182, W - 36, 182], fill=RED, width=4)
    d.line([36, 189, W - 36, 189], fill=RULE, width=1)

    # ---- story grid: 2 cols x 3 rows
    col_x = [36, 524]
    col_w = 464
    row_y = [206, 436, 666]
    row_h = 214
    for i, (label, icon, head, cap) in enumerate(STORIES):
        x = col_x[i % 2]
        y = row_y[i // 2]
        icon(d, x, y + 6, 62, RED)
        tx = x + 80
        tw = col_w - 80
        d.text((tx, y), label, font=f_label, fill=RED)
        hy = y + 24
        for line in wrap(head, f_head, tw)[:2]:
            d.text((tx, hy), line, font=f_head, fill=INK)
            hy += 33
        cy = hy + 4
        for line in wrap(cap, f_cap, tw)[:2]:
            d.text((tx, cy), line, font=f_cap, fill=GRAY)
            cy += 23
        # hairline between rows
        if i // 2 < 2:
            d.line([x, y + row_h - 8, x + col_w, y + row_h - 8],
                   fill=RULE, width=1)

    # ---- also today strip
    sy = 896
    d.rectangle([36, sy, W - 36, sy + 74], fill=LIGHT)
    d.rectangle([36, sy, 44, sy + 74], fill=RED)
    label = "ALSO TODAY:  "
    lx = 58
    d.text((lx, sy + 10), label, font=f_also_b, fill=RED)
    lw = f_also_b.getlength(label)
    lines = wrap(ALSO_TODAY, f_also, W - 36 - lx - lw - 14)
    ty = sy + 10
    # first line sits next to the label, rest full width
    d.text((lx + lw, ty), lines[0], font=f_also, fill=INK)
    ty += 24
    for line in lines[1:]:
        d.text((lx, ty), line, font=f_also, fill=INK)
        ty += 24

    # ---- footer
    center(d, 986, "Sources: The New York Times  \u2022  Reuters  \u2022  BBC",
           f_foot, GRAY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
