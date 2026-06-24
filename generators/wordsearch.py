#!/usr/bin/env python3
"""Word-search puzzle with single-stroke letters.

    python generators/wordsearch.py --seed 2 -o output/wordsearch-01.svg

Places a themed word list into an N x N grid in all 8 directions, fills the rest
with random letters, and lists the words below. Letters are drawn with the
single-stroke font (strokefont.py) so they plot as centre-lines, not outlines.
"""
from __future__ import annotations

import argparse
import random
import string

from _lib import centered_box, page_mm, save, svg
from strokefont import glyph_centered, text_strokes, text_width

# Pen-plotter / art-and-science themed default list (all <= grid size).
DEFAULT_WORDS = ["PLOTTER", "VECTOR", "SERVO", "PEN", "INK", "PAPER", "LINE",
                 "CURVE", "AXIS", "MOTOR", "DRAW", "GRBL", "ART", "SCIENCE",
                 "STROKE", "GANTRY"]

DIRS = [(0, 1), (1, 0), (1, 1), (1, -1), (0, -1), (-1, 0), (-1, -1), (-1, 1)]


def place(words: list[str], n: int, rng: random.Random) -> tuple[list[list[str]], list[str]]:
    grid = [["" for _ in range(n)] for _ in range(n)]
    placed = []
    for word in sorted(words, key=len, reverse=True):
        if len(word) > n:
            continue
        for _ in range(200):
            dr, dc = rng.choice(DIRS)
            r0 = rng.randrange(n)
            c0 = rng.randrange(n)
            r1, c1 = r0 + dr * (len(word) - 1), c0 + dc * (len(word) - 1)
            if not (0 <= r1 < n and 0 <= c1 < n):
                continue
            cells = [(r0 + dr * i, c0 + dc * i) for i in range(len(word))]
            if all(grid[r][c] in ("", word[i]) for i, (r, c) in enumerate(cells)):
                for i, (r, c) in enumerate(cells):
                    grid[r][c] = word[i]
                placed.append(word)
                break
    for r in range(n):
        for c in range(n):
            if not grid[r][c]:
                grid[r][c] = rng.choice(string.ascii_uppercase)
    return grid, placed


def build(page: str, n: int, size: float, seed: int, words: list[str], title: str) -> tuple:
    w, h = page_mm(page)
    rng = random.Random(seed)
    grid, placed = place(words, n, rng)
    x0, y0 = centered_box(w, h, size)
    cell = size / n
    cap = cell * 0.55

    cells = []
    cells.append(svg.rect(x0, y0, size, size, width=0.5))   # frame
    for r in range(n):
        for c in range(n):
            cx, cy = x0 + (c + 0.5) * cell, y0 + (r + 0.5) * cell
            for stroke in glyph_centered(grid[r][c], cx, cy, cap):
                cells.append(svg.polyline(stroke, width=0.4))
    layers = [svg.layer("grid", cells)]

    # title above
    if title:
        th = 6.0
        tx = (w - text_width(title, th)) / 2
        layers.append(svg.layer("title",
            [svg.polyline(s, width=0.5) for s in text_strokes(title, tx, y0 - 8, th)]))

    # word list below, in columns
    wl = []
    lh = 6.5
    wcap = 3.2
    per_col = (len(placed) + 2) // 3
    colw = size / 3
    for i, word in enumerate(sorted(placed)):
        col, row = divmod(i, per_col)
        wx = x0 + col * colw
        wy = y0 + size + 12 + row * lh
        wl += [svg.polyline(s, width=0.4) for s in text_strokes(word, wx, wy, wcap)]
    layers.append(svg.layer("words", wl))

    print(f"  grid {n}x{n}  placed {len(placed)}/{len(words)}: {', '.join(placed)}")
    return w, h, "\n".join(layers)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--grid", type=int, default=13, help="cells per side")
    ap.add_argument("--page", default="letter")
    ap.add_argument("--size", type=float, default=150.0)
    ap.add_argument("--title", default="WORD SEARCH")
    ap.add_argument("--words", nargs="*", default=None, help="override word list")
    ap.add_argument("-o", "--out", default="output/wordsearch.svg")
    a = ap.parse_args(argv)
    words = [x.upper() for x in (a.words or DEFAULT_WORDS)]
    w, h, body = build(a.page, a.grid, a.size, a.seed, words, a.title)
    save(a.out, w, h, body)


if __name__ == "__main__":
    main()