#!/usr/bin/env python3
"""Perfect maze (recursive backtracker) as plottable line art.

    python generators/maze.py --seed 7 --cells 20 -o output/maze-01.svg

A single carved spanning tree → one solution path, entrance top-left, exit
bottom-right. Walls are single strokes; the whole thing plots without the pen
crossing itself.
"""
from __future__ import annotations

import argparse
import random

from _lib import centered_box, page_mm, save, svg
from strokefont import text_strokes, text_width


def carve(n: int, rng: random.Random) -> dict:
    """Recursive backtracker → dict of cell -> set of connected neighbours."""
    conn: dict[tuple[int, int], set] = {}
    visited = {(0, 0)}
    stack = [(0, 0)]
    while stack:
        r, c = stack[-1]
        nbrs = [(r + dr, c + dc) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
                if 0 <= r + dr < n and 0 <= c + dc < n and (r + dr, c + dc) not in visited]
        if not nbrs:
            stack.pop()
            continue
        nr, nc = rng.choice(nbrs)
        conn.setdefault((r, c), set()).add((nr, nc))
        conn.setdefault((nr, nc), set()).add((r, c))
        visited.add((nr, nc))
        stack.append((nr, nc))
    return conn


def maze_walls(n: int, x0: float, y0: float, size: float, rng: random.Random) -> list[str]:
    cell = size / n
    conn = carve(n, rng)

    def P(i: int, j: int) -> tuple[float, float]:  # i=col(x), j=row(y)
        return x0 + i * cell, y0 + j * cell

    segs: list[tuple] = []
    for r in range(n):
        for c in range(n):
            if c + 1 < n and (r, c + 1) not in conn.get((r, c), ()):
                segs.append((P(c + 1, r), P(c + 1, r + 1)))      # east wall
            if r + 1 < n and (r + 1, c) not in conn.get((r, c), ()):
                segs.append((P(c, r + 1), P(c + 1, r + 1)))      # south wall
    for c in range(n):                                            # top / bottom borders
        if c != 0:
            segs.append((P(c, 0), P(c + 1, 0)))                  # entrance gap at col 0
        if c != n - 1:
            segs.append((P(c, n), P(c + 1, n)))                  # exit gap at last col
    for r in range(n):                                            # left / right borders
        segs.append((P(0, r), P(0, r + 1)))
        segs.append((P(n, r), P(n, r + 1)))
    return [svg.line(a[0], a[1], b[0], b[1], width=0.5) for a, b in segs]


def build(page: str, cells: int, size: float, seed: int, title: str) -> tuple:
    w, h = page_mm(page)
    x0, y0 = centered_box(w, h, size)
    rng = random.Random(seed)
    elems = maze_walls(cells, x0, y0, size, rng)
    layers = [svg.layer("maze", elems)]
    if title:
        cap = 6.0
        tx = (w - text_width(title, cap)) / 2
        strokes = text_strokes(title, tx, y0 - 8, cap)
        layers.append(svg.layer("title", [svg.polyline(s, width=0.5) for s in strokes]))
    return w, h, "\n".join(layers)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--cells", type=int, default=20, help="cells per side")
    ap.add_argument("--page", default="letter")
    ap.add_argument("--size", type=float, default=150.0, help="content box (mm)")
    ap.add_argument("--title", default="MAZE")
    ap.add_argument("-o", "--out", default="output/maze.svg")
    a = ap.parse_args(argv)
    w, h, body = build(a.page, a.cells, a.size, a.seed, a.title)
    save(a.out, w, h, body)


if __name__ == "__main__":
    main()