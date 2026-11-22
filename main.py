#!/usr/bin/env python3
"""The World in One Day - Sunday 22 November 2026.

A pure-stdlib Python program that draws one 1024x1024 front page
summing up the day's real world news and writes it to
/output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png).

Stories researched from Sunday 22 November 2026 reporting:
  lead   Middle East - Iran strikes US assets in Bahrain, tankers
         hit off Oman as Gulf tensions spiral.
  1      Ukraine - Russian missiles hit Lviv, two killed, in a
         400-drone / 110-missile barrage; debris falls in Poland.
  2      Trade - EU and Indonesia sign a landmark trade deal after
         ten years of talks; 98.5% of tariffs to go.
  3      Climate - COP31 talks deadlock and run into overtime over
         fossil fuels and finance.
  4      Israel - President Herzog taps Eisenkot to form the next
         government, bypassing Netanyahu.
  strip  France protests a 4th weekend, Hong Kong votes, Democrats
         retake Congress, 6.7 quake shakes Peru, Bolsonaro in ICU,
         Lagarde quits the ECB.

No Pillow, no numpy, no network, no clock, no randomness.
Two runs write byte-identical output.
"""

import binascii
import math
import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER = (247, 243, 234)
INK = (22, 22, 28)
NAVY = (20, 33, 61)
NAVY2 = (28, 48, 88)
GOLD = (201, 162, 39)
GOLD_L = (232, 196, 90)
RED = (178, 34, 34)
RED_L = (214, 69, 65)
TEAL = (38, 120, 110)
TEAL_D = (24, 84, 78)
SKY = (70, 110, 150)
SKY_D = (44, 74, 110)
GREY = (120, 124, 132)
GREY_L = (200, 200, 196)
WHITE = (255, 255, 255)
CREAM = (250, 246, 236)
ORANGE = (224, 122, 42)
GREEN = (46, 125, 60)
BLUE_EU = (0, 51, 153)

# ---------------------------------------------------------------- 5x7 font
# Each glyph is 7 rows of 5 bits, '#' = on, '.' = off.
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '+': ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '*': ("00000", "00100", "10101", "01110", "10101", "00100", "00000"),
}

# ---------------------------------------------------------------- raster
img = bytearray(W * H * 3)


def px(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        img[i], img[i + 1], img[i + 2] = c


def rect(x, y, w, h, c):
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(W, x + w), min(H, y + h)
    for yy in range(y0, y1):
        base = (yy * W + x0) * 3
        for xx in range(x0, x1):
            i = base + (xx - x0) * 3
            img[i], img[i + 1], img[i + 2] = c


def border(x, y, w, h, c, t=2):
    rect(x, y, w, t, c)
    rect(x, y + h - t, w, t, c)
    rect(x, y, t, h, c)
    rect(x + w - t, y, t, h, c)


def circle(cx, cy, r, c):
    for yy in range(cy - r, cy + r + 1):
        dx = int(math.sqrt(max(0, r * r - (yy - cy) * (yy - cy))))
        for xx in range(cx - dx, cx + dx + 1):
            px(xx, yy, c)


def ring(cx, cy, r, c, t=2):
    for yy in range(cy - r - t, cy + r + t + 1):
        for xx in range(cx - r - t, cx + r + t + 1):
            d = math.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
            if r - t <= d <= r:
                px(xx, yy, c)


def line(x0, y0, x1, y1, c):
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        px(x0, y0, c)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def thick_line(x0, y0, x1, y1, c, t=2):
    line(x0, y0, x1, y1, c)
    if t > 1:
        line(x0, y0 + 1, x1, y1 + 1, c)
        line(x0 + 1, y0, x1 + 1, y1, c)


def arc_points(cx, cy, rx, ry, a0, a1, n=24):
    pts = []
    for k in range(n + 1):
        a = a0 + (a1 - a0) * k / n
        pts.append((int(cx + rx * math.cos(a)), int(cy + ry * math.sin(a))))
    return pts


def polyline(pts, c):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        line(x0, y0, x1, y1, c)


# ---------------------------------------------------------------- text
def text_w(s, scale):
    return len(s) * 6 * scale - scale


def draw_text(s, x, y, scale, c):
    # The bitmap font holds capitals only; fold everything to upper
    # case so no letter silently vanishes.
    s = s.upper()
    cx = x
    for ch in s:
        glyph = FONT.get(ch, FONT[' '])
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits[col] == '1':
                    rect(cx + col * scale, y + row * scale, scale, scale, c)
        cx += 6 * scale


def text_center(s, cx, y, scale, c):
    draw_text(s, cx - text_w(s, scale) // 2, y, scale, c)


# ---------------------------------------------------------------- PNG out
def chunk(typ, data):
    out = struct.pack(">I", len(data)) + typ + data
    out += struct.pack(">I", binascii.crc32(typ + data) & 0xFFFFFFFF)
    return out


def write_png(path):
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw += img[y * W * 3:(y + 1) * W * 3]
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)

# ---------------------------------------------------------------- scenes
def scene_lead(x0, y0, x1, y1):
    """Gulf at night: tanker on dark water, missile arcs, burst."""
    rect(x0, y0, x1 - x0, y1 - y0, NAVY2)
    # stars
    for sx, sy in [(18, 14), (52, 30), (96, 10), (140, 26), (180, 12),
                   (220, 34), (260, 16), (300, 28), (36, 52), (150, 48)]:
        px(x0 + sx, y0 + sy, GOLD_L)
        px(x0 + sx + 1, y0 + sy, GOLD_L)
    # moon
    circle(x0 + 40, y0 + 42, 20, GOLD_L)
    circle(x0 + 34, y0 + 36, 16, NAVY2)
    # sea
    rect(x0, y0 + 150, x1 - x0, y1 - y0 - 150, TEAL_D)
    for wy in (y0 + 168, y0 + 196, y0 + 222):
        for wx in range(x0 + 6, x1 - 10, 26):
            line(wx, wy, wx + 14, wy, TEAL)
    # tanker hull + superstructure + funnel
    rect(x0 + 30, y0 + 128, 190, 22, INK)
    rect(x0 + 170, y0 + 108, 50, 20, WHITE)
    rect(x0 + 44, y0 + 112, 26, 16, RED_L)
    for wx in range(x0 + 176, x0 + 214, 12):
        px(wx, y0 + 114, GOLD)
        px(wx, y0 + 120, GOLD)
    # missile arcs from the right, bursting over the water
    polyline(arc_points(x0 + 295, y0 + 210, 85, 85, math.pi, math.pi * 1.55),
             ORANGE)
    polyline(arc_points(x0 + 295, y0 + 210, 62, 62, math.pi, math.pi * 1.55),
             GOLD_L)
    polyline(arc_points(x0 + 295, y0 + 210, 100, 100, math.pi, math.pi * 1.55),
             RED_L)
    # burst star over the tanker
    bx, by = x0 + 236, y0 + 84
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        line(bx, by, int(bx + 26 * math.cos(a)), int(by + 26 * math.sin(a)),
             GOLD_L)
    circle(bx, by, 10, ORANGE)
    circle(bx, by, 5, GOLD_L)
    # radar dish on the far right
    line(x0 + 300, y0 + 140, x0 + 300, y0 + 108, WHITE)
    polyline(arc_points(x0 + 300, y0 + 104, 14, 14, math.pi * 1.15,
                        math.pi * 1.85), WHITE)
    draw_text("BAHRAIN", x0 + 238, y1 - 26, 2, WHITE)


def scene_lviv(x0, y0, x1, y1):
    """Night skyline under a missile barrage."""
    rect(x0, y0, x1 - x0, y1 - y0, SKY_D)
    # skyline
    base = y1 - 8
    for bx, bw, bh in [(6, 52, 30), (64, 40, 42), (110, 60, 26), (176, 44, 38),
                       (226, 52, 30), (284, 46, 44), (336, 58, 28),
                       (400, 44, 36)]:
        rect(x0 + bx, base - bh, bw, bh, INK)
        for wy in range(base - bh + 6, base - 6, 10):
            for wx in range(x0 + bx + 7, x0 + bx + bw - 6, 12):
                px(wx, wy, GOLD_L)
    # missile streaks
    for (sx, sy, ex, ey) in [(40, 4, 90, 40), (150, 2, 210, 44),
                             (260, 6, 320, 42), (360, 2, 410, 38)]:
        thick_line(x0 + sx, y0 + sy, x0 + ex, y0 + ey, ORANGE, 2)
        circle(x0 + ex, y0 + ey, 4, GOLD_L)
    # smoke puffs
    for cx, cy, r in [(96, 42, 8), (214, 44, 9), (322, 42, 8)]:
        circle(x0 + cx, y0 + cy, r, GREY)
        circle(x0 + cx, y0 + cy, r - 4, GREY_L)


def scene_trade(x0, y0, x1, y1):
    """EU flag, Indonesian flag, and the 98.5% figure."""
    rect(x0, y0, x1 - x0, y1 - y0, CREAM)
    # EU flag
    fx, fy = x0 + 14, y0 + 10
    rect(fx, fy, 92, 36, BLUE_EU)
    for k in range(12):
        a = math.radians(k * 30 - 90)
        circle(int(fx + 46 + 13 * math.cos(a)), int(fy + 18 + 12 * math.sin(a)),
               2, GOLD_L)
    # Indonesian flag
    ix = x0 + 120
    rect(ix, fy, 92, 18, RED)
    rect(ix, fy + 18, 92, 18, WHITE)
    border(ix, fy, 92, 36, GREY, 1)
    # the number
    draw_text("98.5%", x0 + 236, y0 + 10, 3, NAVY)
    draw_text("TARIFFS TO GO", x0 + 236, y0 + 34, 2, INK)


def scene_cop(x0, y0, x1, y1):
    """Warming globe beside a rising thermometer."""
    rect(x0, y0, x1 - x0, y1 - y0, (232, 240, 236))
    # globe
    gx, gy = x0 + 60, y0 + 28
    circle(gx, gy, 22, SKY)
    circle(gx - 7, gy - 6, 6, GREEN)
    circle(gx + 8, gy + 5, 7, GREEN)
    circle(gx + 2, gy - 12, 4, GREEN)
    ring(gx, gy, 22, NAVY, 2)
    # crack across the globe
    polyline([(gx - 18, gy - 14), (gx - 6, gy - 2), (gx + 4, gy - 10),
              (gx + 14, gy + 2), (gx + 20, gy + 12)], RED)
    # thermometer
    tx = x0 + 150
    rect(tx, y0 + 8, 12, 34, WHITE)
    border(tx, y0 + 8, 12, 34, INK, 1)
    rect(tx + 2, y0 + 20, 8, 20, RED)
    circle(tx + 6, y0 + 46, 9, RED)
    circle(tx + 6, y0 + 46, 5, RED_L)
    # rising heat lines
    for hx in (x0 + 200, x0 + 216, x0 + 232):
        polyline([(hx, y0 + 44), (hx + 4, y0 + 34), (hx, y0 + 24),
                  (hx + 4, y0 + 14)], ORANGE)
    draw_text("OVERTIME", x0 + 262, y0 + 20, 2, RED)


def scene_israel(x0, y0, x1, y1):
    """Knesset-style building with dome, columns and flag."""
    rect(x0, y0, x1 - x0, y1 - y0, (228, 232, 240))
    bx = x0 + 30
    # dome
    circle(bx + 60, y0 + 34, 20, NAVY2)
    rect(bx + 40, y0 + 34, 40, 6, NAVY2)
    # columns and base
    for cx in range(bx + 8, bx + 112, 22):
        rect(cx, y0 + 40, 8, 14, WHITE)
        border(cx, y0 + 40, 8, 14, NAVY, 1)
    rect(bx, y0 + 40, 120, 4, NAVY)
    rect(bx - 6, y0 + 52, 132, 3, NAVY)
    # flag on a pole
    fx = x0 + 220
    line(fx, y0 + 6, fx, y0 + 52, INK)
    rect(fx + 2, y0 + 8, 64, 22, WHITE)
    rect(fx + 2, y0 + 8, 64, 4, BLUE_EU)
    rect(fx + 2, y0 + 26, 64, 4, BLUE_EU)
    # star of david: two triangles
    sx, sy = fx + 34, y0 + 19
    polyline([(sx, sy - 6), (sx - 6, sy + 5), (sx + 6, sy + 5), (sx, sy - 6)],
             BLUE_EU)
    polyline([(sx, sy + 6), (sx - 6, sy - 5), (sx + 6, sy - 5), (sx, sy + 6)],
             BLUE_EU)
    draw_text("NEW GOVERNMENT", x0 + 292, y0 + 20, 2, NAVY)


# ---------------------------------------------------------------- page
def panel(x, y, w, h, accent, kicker, head, sub, scene):
    rect(x, y, w, h, WHITE)
    border(x, y, w, h, INK, 2)
    rect(x, y, w, 8, accent)
    draw_text(kicker, x + 16, y + 16, 2, accent)
    hy = y + 38
    for ln in head:
        draw_text(ln, x + 16, hy, 3, INK)
        hy += 26
    sy = y + 94
    for ln in sub:
        draw_text(ln, x + 16, sy, 2, (74, 74, 82))
        sy += 16
    scene(x + 8, y + 146, x + w - 8, y + h - 8)


def build():
    rect(0, 0, W, H, PAPER)

    # masthead
    rect(0, 0, W, 118, NAVY)
    rect(0, 118, W, 6, GOLD)
    circle(64, 59, 34, TEAL)
    ring(64, 59, 34, GOLD_L, 2)
    circle(56, 50, 8, GREEN)
    circle(74, 68, 10, GREEN)
    circle(70, 44, 5, GREEN)
    line(64, 27, 64, 91, GOLD_L)
    line(32, 59, 96, 59, GOLD_L)
    draw_text("THE WORLD IN ONE DAY", 120, 28, 5, WHITE)
    draw_text("SUNDAY 22 NOVEMBER 2026", 120, 76, 3, GOLD_L)
    draw_text("No. 22", 900, 76, 3, WHITE)

    # lead story
    lx, ly, lw, lh = 24, 140, 976, 250
    rect(lx, ly, lw, lh, WHITE)
    border(lx, ly, lw, lh, INK, 2)
    rect(lx, ly, 14, lh, RED)
    draw_text("MIDDLE EAST ON EDGE", lx + 32, ly + 18, 2, RED)
    draw_text("IRAN STRIKES U.S. BASES", lx + 32, ly + 46, 4, INK)
    draw_text("IN BAHRAIN", lx + 32, ly + 82, 4, INK)
    sub = ["IRGC missiles and drones hit Patriot",
           "radars; tankers struck off Oman as",
           "Gulf tensions spiral toward war."]
    sy = ly + 128
    for ln in sub:
        draw_text(ln, lx + 32, sy, 2, (74, 74, 82))
        sy += 18
    draw_text("TANKERS HIT OFF OMAN", lx + 32, ly + 196, 2, RED)
    scene_lead(lx + 640, ly + 10, lx + lw - 10, ly + lh - 10)

    # grid of four
    gy = 410
    panel(24, gy, 478, 210, ORANGE, "UKRAINE UNDER FIRE",
          ["MISSILES RAIN", "ON LVIV"],
          ["Two killed as Russia fires 400",
           "drones and 110 missiles;",
           "debris falls in Poland."],
          scene_lviv)
    panel(522, gy, 478, 210, TEAL, "TRADE - TEN YEARS ON",
          ["EU SEALS TRADE", "DEAL WITH INDONESIA"],
          ["Ten years of talks end;",
           "98.5% of tariffs to go.",
           "Southeast Asia's biggest economy."],
          scene_trade)
    panel(24, gy + 230, 478, 210, RED, "CLIMATE - COP31",
          ["COP31 TALKS", "DEADLOCK"],
          ["Climate summit runs into",
           "overtime as the fossil-fuel",
           "and finance rift deepens."],
          scene_cop)
    panel(522, gy + 230, 478, 210, NAVY2, "ISRAEL - NEW TURN",
          ["EISENKOT TAPPED", "TO LEAD ISRAEL"],
          ["President Herzog bypasses",
           "Netanyahu; coalition talks",
           "open with Likud invited."],
          scene_israel)

    # also-today strip
    ty = 874
    rect(24, ty, 976, 72, NAVY)
    draw_text("ALSO TODAY:", 40, ty + 8, 2, GOLD_L)
    draw_text("FRANCE PROTESTS FOR A 4TH WEEKEND  *  HONG KONG VOTES",
              184, ty + 8, 2, WHITE)
    draw_text("DEMOCRATS RETAKE CONGRESS  *  6.7 QUAKE SHAKES PERU",
              40, ty + 30, 2, WHITE)
    draw_text("BOLSONARO IN ICU  *  LAGARDE QUITS ECB  *  NORWAY VOIDS OIL LICENCES",
              40, ty + 52, 2, WHITE)

    # footer
    text_center("DRAWN FROM THE DAY'S REPORTING - SUNDAY 22 NOVEMBER 2026",
                W // 2, 972, 2, (110, 110, 116))


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    if not os.path.isdir(outdir):
        os.makedirs(outdir, exist_ok=True)
    else:
        # Clear only the contents of the grader-owned directory,
        # never the directory itself.
        for name in os.listdir(outdir):
            path = os.path.join(outdir, name)
            if os.path.isfile(path):
                os.remove(path)
    build()
    size = write_png(os.path.join(outdir, "entry.png"))
    print("wrote %s (%d bytes)" % (os.path.join(outdir, "entry.png"), size))


if __name__ == "__main__":
    main()
