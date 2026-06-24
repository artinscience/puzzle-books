#!/usr/bin/env python3
"""Radial mandala / coloring page.

    python generators/mandala.py --seed 5 -o output/mandala-01.svg

Concentric bands of k-fold symmetric motifs (rings, scallops, petals, spokes),
chosen deterministically from the seed. More pen-down time than the line
puzzles — a good ink-flow / endurance test for the plotter.
"""
from __future__ import annotations

import argparse
import math
import random

from _lib import arc_pts, centered_box, circle_pts, page_mm, save, svg
from strokefont import text_strokes, text_width


def scallops(cx: float, cy: float, r: float, k: float) -> list[str]:
    """k outward bumps around radius r."""
    out = []
    bump = (2 * math.pi * r / k) * 0.5
    for i in range(int(k)):
        a = 2 * math.pi * i / k
        mx, my = cx + (r + bump) * math.cos(a), cy + (r + bump) * math.sin(a)
        a0, a1 = a - math.pi / k, a + math.pi / k
        p0 = (cx + r * math.cos(a0), cy + r * math.sin(a0))
        p1 = (cx + r * math.cos(a1), cy + r * math.sin(a1))
        out.append(svg.polyline([p0, (mx, my), p1], width=0.4))
    return out


def petals(cx: float, cy: float, r0: float, r1: float, k: float) -> list[str]:
    """k pointed petals spanning radii r0..r1."""
    out = []
    for i in range(int(k)):
        a = 2 * math.pi * i / k
        tip = (cx + r1 * math.cos(a), cy + r1 * math.sin(a))
        for s in (-1, 1):
            aw = a + s * math.pi / k * 0.7
            base = (cx + r0 * math.cos(aw), cy + r0 * math.sin(aw))
            mid = (cx + (r0 + r1) / 2 * math.cos(a + s * math.pi / k * 0.35),
                   cy + (r0 + r1) / 2 * math.sin(a + s * math.pi / k * 0.35))
            out.append(svg.polyline([base, mid, tip], width=0.4))
    return out


def dot_ring(cx: float, cy: float, r: float, k: float, dot: float) -> list[str]:
    out = []
    for i in range(int(k)):
        a = 2 * math.pi * i / k
        out.append(svg.polyline(circle_pts(cx + r * math.cos(a),
                                            cy + r * math.sin(a), dot, 20), width=0.4))
    return out


def build(page: str, size: float, seed: int, fold: int, bands: int, title: str) -> tuple:
    w, h = page_mm(page)
    cx, cy = w / 2, h / 2
    rng = random.Random(seed)
    k = fold if fold > 0 else rng.choice([10, 12, 14, 16, 18])   # k-fold symmetry (intricacy)
    bands = max(1, bands)                                        # concentric motif bands
    R = size / 2
    elems: list[str] = []

    # bounding rings
    elems.append(svg.polyline(circle_pts(cx, cy, R), width=0.5))
    elems.append(svg.polyline(circle_pts(cx, cy, R * 0.97), width=0.3))

    # spokes
    for i in range(int(k)):
        a = 2 * math.pi * i / k
        elems.append(svg.line(cx + R * 0.18 * math.cos(a), cy + R * 0.18 * math.sin(a),
                              cx + R * 0.97 * math.cos(a), cy + R * 0.97 * math.sin(a),
                              width=0.3))

    # `bands` concentric motif rings (outside in), spaced evenly over 0.85R..0.32R
    fracs = [0.85] if bands == 1 else \
            [0.85 - (0.85 - 0.32) * i / (bands - 1) for i in range(bands)]
    motifs = ["scallop", "petal", "dot", "ring"]
    rng.shuffle(motifs)
    for i, f in enumerate(fracs):
        r, m = R * f, motifs[i % len(motifs)]
        if m == "scallop":
            elems += scallops(cx, cy, r, k)
        elif m == "petal":
            elems += petals(cx, cy, r * 0.78, r, k)
        elif m == "dot":
            elems += dot_ring(cx, cy, r, k, R * 0.03)
        else:
            elems.append(svg.polyline(circle_pts(cx, cy, r), width=0.4))

    # centre rosette
    elems.append(svg.polyline(circle_pts(cx, cy, R * 0.14), width=0.4))
    elems += petals(cx, cy, R * 0.05, R * 0.16, k)

    layers = [svg.layer("mandala", elems)]
    if title:
        cap = 6.0
        tx = (w - text_width(title, cap)) / 2
        layers.append(svg.layer("title",
            [svg.polyline(s, width=0.5) for s in text_strokes(title, tx, cy + R + 14, cap)]))
    print(f"  symmetry k={k}  bands={bands}")
    return w, h, "\n".join(layers)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--fold", type=int, default=0, help="k-fold symmetry (0 = auto from seed)")
    ap.add_argument("--bands", type=int, default=4, help="concentric motif bands (intricacy)")
    ap.add_argument("--page", default="letter")
    ap.add_argument("--size", type=float, default=150.0)
    ap.add_argument("--title", default="")
    ap.add_argument("-o", "--out", default="output/mandala.svg")
    a = ap.parse_args(argv)
    w, h, body = build(a.page, a.size, a.seed, a.fold, a.bands, a.title)
    save(a.out, w, h, body)


if __name__ == "__main__":
    main()