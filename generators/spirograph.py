#!/usr/bin/env python3
"""Hypotrochoid (spirograph) — one continuous line.

    python generators/spirograph.py --seed 3 -o output/spiro-01.svg

A pen rolling inside a fixed circle traces a closed curve that repeats after
``r/gcd(R, r)`` turns. Drawn as a single polyline → the plotter never lifts the
pen until it's done.
"""
from __future__ import annotations

import argparse
import math
import random
from math import gcd

from _lib import centered_box, page_mm, save, svg
from strokefont import text_strokes, text_width


def hypotrochoid(R: int, r: int, d: float, cx: float, cy: float,
                 scale: float, steps_per_turn: int = 240) -> list[tuple[float, float]]:
    turns = r // gcd(R, r)
    n = turns * steps_per_turn
    k = (R - r) / r
    pts = []
    for i in range(n + 1):
        t = 2 * math.pi * turns * i / n
        x = (R - r) * math.cos(t) + d * math.cos(k * t)
        y = (R - r) * math.sin(t) - d * math.sin(k * t)
        pts.append((cx + x * scale, cy + y * scale))
    return pts


def build(page: str, size: float, seed: int, title: str, petals: int = 0) -> tuple:
    w, h = page_mm(page)
    cx, cy = w / 2, h / 2
    rng = random.Random(seed)
    if petals > 0:
        # `petals` is the intricacy knob: with coprime R,r the rosette has exactly
        # R outer petals (R/gcd = R). r ~0.45R keeps petals prominent; the seed
        # varies the shape (via d) so variations of one tier differ but keep the
        # same petal count.
        R = petals
        r = max(2, round(0.45 * petals))
        while gcd(R, r) != 1:
            r += 1
        d = rng.uniform(0.55, 0.92) * r
    else:
        R = rng.choice([90, 96, 100, 105, 120])
        r = rng.choice([29, 33, 37, 41, 47, 53])     # coprime-ish with R → long path
        d = rng.uniform(0.55, 0.95) * r
    pts = hypotrochoid(R, r, d, cx, cy, 1.0)
    reach = max(max(abs(x - cx), abs(y - cy)) for x, y in pts)
    scale = (size / 2) / reach                    # fit the curve into the box
    pts = [(cx + (x - cx) * scale, cy + (y - cy) * scale) for x, y in pts]

    layers = [svg.layer("spiro", [svg.polyline(pts, width=0.4)])]
    if title:
        cap = 6.0
        tx = (w - text_width(title, cap)) / 2
        ty = cy + size / 2 + 14
        strokes = text_strokes(title, tx, ty, cap)
        layers.append(svg.layer("title", [svg.polyline(s, width=0.5) for s in strokes]))
    print(f"  R={R} r={r} d={d:.1f}  turns={r // gcd(R, r)}  points={len(pts)}")
    return w, h, "\n".join(layers)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--page", default="letter")
    ap.add_argument("--size", type=float, default=150.0)
    ap.add_argument("--title", default="")
    ap.add_argument("--petals", type=int, default=0,
                    help="rosette petal count (intricacy; 0 = random from seed)")
    ap.add_argument("-o", "--out", default="output/spiro.svg")
    a = ap.parse_args(argv)
    w, h, body = build(a.page, a.size, a.seed, a.title, a.petals)
    save(a.out, w, h, body)


if __name__ == "__main__":
    main()