"""Draw the 23 November 2026 world-news image (1024x1024, deterministic).

Layout is a newspaper front page: masthead with the date, one big lead
story (Democrats clinch their biggest US House majority since 1992),
four smaller panels (Libya, Indonesia, Ukraine, Strait of Hormuz) and a
bottom strip with two more stories.
Everything is drawn with PIL primitives; the output PNG is byte-stable.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (244, 239, 228)
INK = (18, 18, 18)
RED = (178, 34, 34)
GOLD = (232, 184, 75)
NAVY = (18, 59, 79)
LIGHT = (215, 227, 232)
GREY = (110, 110, 105)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, fnt, fill, leading=1.18):
    """Draw lines starting at (x, y); return y after the last line."""
    lh = int(fnt.size * leading)
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def centered(d, cx, y, text, fnt, fill):
    w = d.textlength(text, font=fnt)
    d.text((cx - w / 2, y), text, font=fnt, fill=fill)


def draw_capitol(d, cx, cy, r):
    """A stylised US Capitol dome in white and gold on the navy lead."""
    # dome
    d.ellipse([cx - 78, cy - 88, cx + 78, cy + 40], fill=(240, 240, 235))
    d.rectangle([cx - 78, cy - 22, cx + 78, cy + 40], fill=(240, 240, 235))
    # dome ribs
    for dx in (-52, -26, 0, 26, 52):
        d.line([cx + dx, cy - 82 + abs(dx) // 3, cx + dx, cy + 38],
               fill=(200, 200, 190), width=2)
    # lantern + flag
    d.rectangle([cx - 10, cy - 112, cx + 10, cy - 84], fill=(240, 240, 235))
    d.ellipse([cx - 14, cy - 120, cx + 14, cy - 104], fill=GOLD)
    d.line([cx, cy - 120, cx, cy - 146], fill=GOLD, width=3)
    d.polygon([(cx, cy - 146), (cx + 30, cy - 139), (cx, cy - 132)],
              fill=(178, 34, 34))
    # drum + columns
    d.rectangle([cx - 92, cy + 40, cx + 92, cy + 52], fill=(220, 220, 210))
    for i in range(7):
        x0 = cx - 84 + i * 26
        d.rectangle([x0, cy + 52, x0 + 12, cy + 96], fill=(240, 240, 235))
    d.rectangle([cx - 96, cy + 96, cx + 96, cy + 106], fill=(220, 220, 210))
    # stars: 258 seats as a scatter of gold dots below the dome
    import math
    for i in range(24):
        ang = math.pi * (0.15 + 0.7 * (i % 8) / 7)
        rr = 118 + (i // 8) * 12
        sx = cx + rr * math.cos(ang) * 0.9
        sy = cy + 128 + rr * math.sin(ang) * 0.28
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=GOLD)


def panel(d, x, y, w, h, bg, kicker, headline, sub, art):
    d.rectangle([x, y, x + w, y + h], fill=bg)
    pad = 18
    tx = x + pad
    ty = y + 14
    kf = font(FONT_BOLD, 19)
    sf = font(FONT_REG, 20)
    art_w = 108
    text_w = w - pad * 2 - art_w
    d.text((tx, ty), kicker, font=kf, fill=GOLD)
    ty += 28
    # shrink the headline until it fits on two lines
    size = 33
    while size > 24:
        hf = font(FONT_BOLD, size)
        if len(wrap(d, headline, hf, text_w)) <= 2:
            break
        size -= 2
    lines = wrap(d, headline, hf, text_w)
    ty = text_block(d, tx, ty, lines, hf, (255, 255, 255), leading=1.08)
    ty += 4
    slines = wrap(d, sub, sf, text_w)[:2]
    text_block(d, tx, ty, slines, sf, LIGHT, leading=1.15)
    art(d, x + w - art_w - 8, y + 18, art_w, h - 36)


def art_ship(d, x, y, w, h):
    # a warship listing in the harbour, smoke rising
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(38, 84, 96))
    d.polygon([(x + 6, y + h - 34), (x + 98, y + h - 52),
               (x + 98, y + h - 34)], fill=(90, 100, 110))
    d.rectangle([x + 30, y + h - 66, x + 52, y + h - 48], fill=(120, 128, 136))
    d.line([x + 40, y + h - 84, x + 40, y + h - 66], fill=(120, 128, 136), width=4)
    for i, (sx, sy, sr) in enumerate([(x + 42, y + 22, 12), (x + 58, y + 8, 16),
                                      (x + 74, y + 26, 10)]):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 120, 115))
    d.polygon([(x + 52, y + h - 60), (x + 58, y + h - 76), (x + 64, y + h - 60)],
              fill=(255, 120, 40))
    d.ellipse([x + 70, y + h - 46, x + 78, y + h - 38], fill=(255, 220, 120))


def art_flame(d, x, y, w, h):
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(38, 84, 96))
    for bx, bw, bh in [(x + 2, 22, 62), (x + 28, 18, 84), (x + 50, 24, 54),
                        (x + 78, 20, 74)]:
        d.rectangle([bx, y + h - 12 - bh, bx + bw, y + h - 12],
                    fill=(70, 70, 70))
    d.polygon([(x + 52, y + 6), (x + 66, y + 34), (x + 76, y + 22),
               (x + 72, y + 52), (x + 52, y + 62), (x + 38, y + 44),
               (x + 46, y + 28)], fill=(255, 120, 40))
    d.polygon([(x + 54, y + 30), (x + 62, y + 42), (x + 66, y + 34),
               (x + 62, y + 52), (x + 52, y + 54), (x + 50, y + 42)],
              fill=(255, 220, 120))


def art_skyline(d, x, y, w, h):
    base = y + h - 12
    for bx, bw, bh in [(x + 2, 22, 62), (x + 28, 18, 84), (x + 50, 24, 54),
                        (x + 78, 20, 74)]:
        d.rectangle([bx, base - bh, bx + bw, base], fill=(148, 163, 184))
        for wy in range(base - bh + 8, base - 6, 14):
            d.rectangle([bx + 4, wy, bx + bw - 4, wy + 6], fill=(255, 220, 120))
    d.ellipse([x + 58, y + 2, x + 82, y + 26], fill=(203, 213, 225))
    d.ellipse([x + 70, y - 6, x + 96, y + 18], fill=(226, 232, 240))
    d.polygon([(x + 30, y + 34), (x + 38, y + 18), (x + 46, y + 34)],
              fill=(255, 120, 40))


def art_tanker(d, x, y, w, h):
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(38, 84, 96))
    d.rectangle([x + 4, y + h - 44, x + 100, y + h - 28], fill=(120, 60, 40))
    d.rectangle([x + 60, y + h - 62, x + 84, y + h - 44], fill=(200, 200, 195))
    d.line([x + 72, y + h - 80, x + 72, y + h - 62], fill=(200, 200, 195), width=4)
    for i, (sx, sy) in enumerate([(x + 12, y + 56), (x + 34, y + 44)]):
        ex, ey = sx + 30, sy - 34
        d.arc([sx - 8, ey - 8, ex + 22, sy + 18], start=200, end=330,
              fill=(255, 170, 60), width=5)
        d.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=(255, 220, 120))
    d.text((x + 4, y + h - 22), "x2", font=font(FONT_BOLD, 18), fill=(255, 170, 60))


def render(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    centered(d, W // 2, 26, "THE WORLD IN ONE IMAGE",
             font(FONT_BOLD, 58), INK)
    d.rectangle([24, 104, W - 24, 108], fill=RED)
    centered(d, W // 2, 120, "MONDAY, 23 NOVEMBER 2026",
             font(FONT_BOLD, 30), RED)

    # ---- lead story: Democrats' House majority ----
    d.rectangle([24, 168, W - 24, 500], fill=NAVY)
    draw_capitol(d, 196, 300, 108)
    tx = 348
    d.text((tx, 196), "US MIDTERMS  •  WASHINGTON",
           font=font(FONT_BOLD, 21), fill=GOLD)
    d.text((tx, 226), "DEMOCRATS WIN", font=font(FONT_BOLD, 66),
           fill=(255, 255, 255))
    d.text((tx, 296), "258 SEATS", font=font(FONT_BOLD, 66),
           fill=(255, 255, 255))
    sub = ("Biggest House majority since 1992 — a sweep unseen "
           "in three decades; the Senate flips blue too.")
    lines = wrap(d, sub, font(FONT_REG, 25), W - 24 - tx - 28)
    text_block(d, tx, 392, lines, font(FONT_REG, 25), LIGHT, leading=1.22)

    # ---- four panels ----
    pw, ph, gap = 476, 160, 12
    panel(d, 24, 512, pw, ph, (122, 31, 31), "LIBYA  •  BENGHAZI",
          "RUSSIAN WARSHIP HIT",
          "Corvette Merkury struck by suspected sea drones.",
          art_ship)
    panel(d, 24 + pw + gap, 512, pw, ph, (20, 83, 45), "INDONESIA  •  CIKANDE",
          "FACTORY FIRE: 24 BODY BAGS",
          "Candy factory blaze; dozens missing, search resumes.",
          art_flame)
    panel(d, 24, 512 + ph + gap, pw, ph, (51, 65, 85), "UKRAINE  •  KYIV REGION",
          "DRONE HITS KYIV BUILDING",
          "At least 14 missing after Russian drone strike.",
          art_skyline)
    panel(d, 24 + pw + gap, 512 + ph + gap, pw, ph, (124, 45, 18),
          "STRAIT OF HORMUZ",
          "TWO TANKERS HIT",
          "Projectiles strike tankers as the war spreads.",
          art_tanker)

    # ---- bottom strip: two more stories ----
    d.line([24, 858, W - 24, 858], fill=INK, width=2)
    d.line([W // 2, 872, W // 2, 958], fill=(180, 175, 165), width=2)
    bf = font(FONT_BOLD, 22)
    kf = font(FONT_BOLD, 18)
    sf = font(FONT_REG, 19)
    d.text((24, 868), "CYBERCRIME", font=kf, fill=RED)
    y = text_block(d, 24, 890, wrap(d, "FBI PROBES BREACH OF ITS DATABASE",
                                    bf, 452), bf, INK, leading=1.08)
    text_block(d, 24, y + 2, wrap(d, "Apparent hack of criminal records under inquiry.",
                                  sf, 452), sf, (70, 70, 65))
    d.text((W // 2 + 18, 868), "BALTIC SEA", font=kf, fill=RED)
    y = text_block(d, W // 2 + 18, 890, wrap(d, "RUSSIAN SHIP STILL BURNING OFF FINLAND",
                                             bf, 452), bf, INK, leading=1.08)
    text_block(d, W // 2 + 18, y + 2, wrap(d, "Cargo ship ablaze after attack, drifting in the Gulf.",
                                           sf, 452), sf, (70, 70, 65))

    # ---- footer ----
    centered(d, W // 2, 994, "23 NOVEMBER 2026  —  THE WORLD'S NEWS IN ONE IMAGE",
             font(FONT_BOLD, 17), GREY)

    img.save(path, format="PNG")
    return path


if __name__ == "__main__":
    render("entry.png")
