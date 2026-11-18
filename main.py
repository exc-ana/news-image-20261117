#!/usr/bin/env python3
"""Deterministic generator for the make.fun bounty entry:
"Sum up 17 November's world news in one image".

Python standard library ONLY (no Pillow, no network, no fonts from disk).
Output: output.png -- 1024x1024 PNG, < 1 MiB, byte-identical on every run.

How it works:
  * Text is drawn with a built-in 5x7 bitmap font (uppercase A-Z, 0-9,
    and common punctuation) scaled by integer factors.
  * The PNG is encoded by hand: signature + IHDR + IDAT (zlib, level 9)
    + IEND. No timestamps, no metadata chunks, no randomness, so the
    output bytes are fully deterministic.
  * All news copy is baked into EVENTS below, with sources listed in
    README.md. Nothing is fetched at runtime.

Usage:  python3 main.py            # writes output.png next to this file
"""
import hashlib
import struct
import sys
import zlib
from pathlib import Path

W = H = 1024

# ---------------------------------------------------------------- font ----
# 5x7 bitmap font. Each glyph is 7 rows of 5 characters ('#' = ink).
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "?": ("01110", "10001", "00001", "00010", "00100", "00000", "00100"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
}

# ------------------------------------------------------------- content ----
# Six specific, verified events from 17 November 2026, across regions
# and fields. Wording stays close to what the sources reported; no
# speculation, no hype, no forecasts. Sources in README.md.
EVENTS = [
    ("MIDDLE EAST", (180, 35, 24),
     "US STRIKES QESHM ISLAND, IRAN",
     "US WARPLANES HIT A MISSILE SITE ON QESHM AFTER IRAN TARGETED US "
     "PERSONNEL AND ASSETS, A US OFFICIAL TOLD REUTERS."),
    ("UKRAINE", (29, 78, 216),
     "CRIMEAN BRIDGE HIT FOR A SECOND DAY",
     "RUSSIA SUSPENDED ROAD AND RAIL TRAFFIC AFTER A SECOND UKRAINIAN "
     "STRIKE IN TWO DAYS, REUTERS REPORTED."),
    ("ASIA-PACIFIC", (14, 116, 144),
     "JAPAN SCRAMBLES JETS OVER AIRSPACE",
     "TWO SUSPECTED RUSSIAN AIRCRAFT ENTERED AIRSPACE NEAR OKINOSHIMA "
     "FOR ABOUT 3 MINUTES EACH, TOKYO SAID."),
    ("GAZA", (154, 52, 18),
     "WINTER RAINS DEEPEN GAZA SHELTER CRISIS",
     "THE UN WARNED RAINS WERE FLOODING MAKESHIFT SHELTERS AS MORE THAN "
     "1.7 MILLION PEOPLE REMAIN DISPLACED."),
    ("HEALTH", (21, 128, 61),
     "US LOSES MEASLES ELIMINATION STATUS",
     "PAHO SAID THE STATUS ENDED AFTER THE SAME MEASLES STRAIN "
     "CIRCULATED FOR AT LEAST 12 MONTHS."),
    ("MARKETS", (107, 33, 168),
     "WALL STREET FALLS AS AI STOCKS SLIDE",
     "MAJOR US INDEXES CLOSED LOWER ON TUESDAY, LED BY AI AND TECH "
     "STOCKS, THE AP REPORTED."),
]

NAVY = (16, 36, 62)
GOLD = (201, 162, 39)
WHITE = (255, 255, 255)
INK = (17, 24, 39)
GREY = (100, 116, 139)
CARD = (255, 255, 255)
CARD_BORDER = (203, 213, 225)
BG = (241, 245, 249)

# ------------------------------------------------------------- canvas -----
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, bg)

    def fill_rect(self, x, y, w, h, color):
        r, g, b = color
        for yy in range(max(0, y), min(self.h, y + h)):
            base = (yy * self.w + max(0, x)) * 3
            for xx in range(max(0, x), min(self.w, x + w)):
                i = (yy * self.w + xx) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = r, g, b

    def draw_text(self, x, y, text, scale, color):
        """Draw uppercase text with the 5x7 bitmap font."""
        cx = x
        for ch in text:
            glyph = FONT.get(ch)
            if glyph is None:
                raise ValueError(f"character not in font: {ch!r}")
            for row, bits in enumerate(glyph):
                for col, bit in enumerate(bits):
                    if bit == "1":
                        self.fill_rect(cx + col * scale, y + row * scale,
                                       scale, scale, color)
            cx += 6 * scale
        return cx

    def text_width(self, text, scale):
        return len(text) * 6 * scale - scale

    def wrap(self, text, scale, max_width):
        """Greedy word wrap; returns a list of lines."""
        words, lines, cur = text.split(" "), [], ""
        for word in words:
            trial = f"{cur} {word}".strip()
            if self.text_width(trial, scale) <= max_width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines


def draw_image():
    c = Canvas(W, H, BG)

    # Header ------------------------------------------------------------
    c.fill_rect(0, 0, W, 196, NAVY)
    c.fill_rect(0, 196, W, 6, GOLD)
    c.draw_text(48, 42, "17 NOVEMBER 2026", 7, WHITE)
    c.draw_text(48, 118, "THE DAY IN WORLD NEWS", 3, (201, 162, 39))
    c.draw_text(48, 156, "SIX STORIES FROM AROUND THE WORLD", 2, (203, 213, 225))

    # Event cards -------------------------------------------------------
    x0, y, bw, bh, gap = 48, 218, W - 96, 116, 10
    for tag, color, headline, detail in EVENTS:
        c.fill_rect(x0, y, bw, bh, CARD)
        # border
        c.fill_rect(x0, y, bw, 2, CARD_BORDER)
        c.fill_rect(x0, y + bh - 2, bw, 2, CARD_BORDER)
        c.fill_rect(x0, y, 2, bh, CARD_BORDER)
        c.fill_rect(x0 + bw - 2, y, 2, bh, CARD_BORDER)
        # accent bar
        c.fill_rect(x0, y, 14, bh, color)
        tx = x0 + 32
        c.draw_text(tx, y + 14, tag, 2, color)
        c.draw_text(tx, y + 38, headline, 3, INK)
        lines = c.wrap(detail, 2, bw - 32 - 16)
        ly = y + 68
        for line in lines[:2]:
            c.draw_text(tx, ly, line, 2, (51, 65, 85))
            ly += 20
        y += bh + gap

    # Footer ------------------------------------------------------------
    fy = y + 2
    c.draw_text(48, fy, "SOURCES: REUTERS, AP, PAHO, UN, JAPAN DEFENCE MINISTRY",
                2, GREY)
    c.draw_text(48, fy + 22,
                "SUMMARY OF EVENTS AS REPORTED ON 17 NOVEMBER 2026.",
                2, GREY)
    return c


# -------------------------------------------------------------- png -------
def chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def encode_png(canvas):
    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    raw = bytearray()
    for yy in range(canvas.h):
        raw.append(0)  # filter: none
        raw += canvas.px[yy * canvas.w * 3:(yy + 1) * canvas.w * 3]
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    return png


def main():
    out = Path(__file__).resolve().parent / "output.png"
    png = encode_png(draw_image())
    out.write_bytes(png)
    print(f"wrote {out} ({len(png)} bytes, "
          f"sha256={hashlib.sha256(png).hexdigest()})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
