"""Draw the 23 November 2026 front page: a newspaper-style summary image.

Runs locally with PIL only. The graded program (main.py) never draws; it
just copies the PNG this script produces.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 232)
INK = (24, 22, 18)
RED = (178, 34, 34)
NAVY = (28, 52, 96)
TEAL = (18, 110, 108)
GOLD = (176, 128, 28)
GREY = (105, 100, 92)
RULE = (180, 172, 156)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, color=INK):
    """Draw wrapped paragraph, return y below it."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def kicker(draw, x, y, label, color):
    """Small coloured tag line above a story."""
    fnt = font(SANS_BOLD, 17)
    draw.text((x, y), label.upper(), font=fnt, fill=color)
    return y + 30


def headline(draw, x, y, text, fnt, max_w, leading):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=INK)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, color=RULE):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 44  # margin
    right = W - mx

    # ---- masthead ----
    d.text((mx, 26), "THE WORLD TODAY", font=font(SERIF_BOLD, 76), fill=INK)
    d.text((mx, 112), "MONDAY, 23 NOVEMBER 2026  •  ONE DAY, SEVEN STORIES",
           font=font(SANS_BOLD, 22), fill=RED)
    rule(d, mx, 152, right, 4, INK)
    rule(d, mx, 160, right, 1)

    # ---- lead story ----
    y = 182
    y = kicker(d, mx, y, "United States  •  Lead story", RED)
    y = headline(d, mx, y,
                 "Democrats clinch biggest House majority since 1992",
                 font(SERIF_BOLD, 56), right - mx, 64)
    y += 4
    y = headline(d, mx, y,
                 "258 seats, a gain of 44 — sealed Sunday as Chuck Hubbard "
                 "beat Virginia Foxx in North Carolina; the Senate flips blue too.",
                 font(SERIF, 28), right - mx, 36)
    y += 10
    # seat-count bar: 258 of 435
    bar_y = y
    d.rectangle([mx, bar_y, right, bar_y + 26], outline=INK, width=2)
    fill_w = int((right - mx) * 258 / 435)
    d.rectangle([mx + 2, bar_y + 2, mx + fill_w, bar_y + 24], fill=NAVY)
    d.text((mx, bar_y + 34),
           "Democrats 258  •  Republicans 177  •  218 needed for a majority",
           font=font(SANS_BOLD, 20), fill=NAVY)
    y = bar_y + 66
    rule(d, mx, y, right, 2, INK)

    # ---- three-column story grid, two rows of three ----
    y += 18
    gap = 24
    col_w = (right - mx - 2 * gap) // 3

    stories = [
        ("Ukraine war  •  Black Sea", NAVY,
         "Russian corvette hit off Libya",
         "The corvette Merkury was struck by suspected Ukrainian sea "
         "drones at Benghazi and is mostly sunk."),
        ("Middle East  •  Gulf", TEAL,
         "Two tankers hit in Strait of Hormuz",
         "Two oil tankers were struck by projectiles in the strait that "
         "carries a fifth of the world's seaborne oil."),
        ("Indonesia  •  Cikande", RED,
         "Candy-factory fire: 24 dead, dozens missing",
         "Rescuers recovered 24 body bags from the gutted factory in "
         "Cikande, Banten; the search resumes on Monday."),
        ("Ukraine  •  Kyiv region", NAVY,
         "Drone strike on homes, 14 missing",
         "A Russian drone hit a building in the Kyiv region, leaving at "
         "least 14 people missing in the rubble."),
        ("United States", GOLD,
         "FBI probes breach of its crime database",
         "The FBI is investigating an apparent breach of its criminal "
         "database, checking what was reached."),
        ("Baltic  •  Finland", TEAL,
         "Russian cargo ship still burning",
         "A Russian cargo ship remains ablaze off the Finnish coast, "
         "with coastguard vessels standing by."),
    ]

    def draw_cell(x, yy, tag, colour, head, body):
        yy = kicker(d, x, yy, tag, colour)
        yy = headline(d, x, yy, head, font(SERIF_BOLD, 26), col_w, 32)
        yy += 4
        yy = para(d, x, yy, body, font(SERIF, 18), col_w, 24)
        return yy

    row_y = y
    row_bottom = row_y
    for i, (tag, colour, head, body) in enumerate(stories):
        x = mx + (i % 3) * (col_w + gap)
        if i == 3:
            row_y = row_bottom + 18
            rule(d, mx, row_y - 9, right, 1)
        bottom = draw_cell(x, row_y, tag, colour, head, body)
        if i % 3 == 0:
            row_bottom = bottom
        else:
            row_bottom = max(row_bottom, bottom)
    y = row_bottom

    # ---- footer ----
    rule(d, mx, y + 8, right, 2, INK)
    d.text((mx, y + 20),
           "Compiled from wire reports  •  Monday 23 November 2026",
           font=font(SANS, 19), fill=GREY)
    brand = "THE WORLD TODAY"
    brand_fnt = font(SANS_BOLD, 19)
    d.text((right - d.textlength(brand, font=brand_fnt), y + 20),
           brand, font=brand_fnt, fill=GREY)

    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    page = draw_page()
    out = os.path.join(here, "entry.png")
    page.save(out, "PNG")
    print("wrote", out, page.size)


if __name__ == "__main__":
    main()
