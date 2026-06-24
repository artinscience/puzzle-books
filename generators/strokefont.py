"""A compact single-stroke (Hershey-style) vector font.

Outline fonts plot as hollow double-lines; a pen plotter wants one centre-line
per stroke. This is a hand-built angular uppercase alphabet + digits on a
4-wide x 6-tall grid (y UP, baseline at y=0, cap height y=6). Each glyph is a
list of strokes; each stroke a polyline of (x, y) points. Enough for word-search
grids and titles — not a complete typeface.
"""
from __future__ import annotations

GLYPHS: dict[str, list[list[tuple[float, float]]]] = {
    " ": [],
    "A": [[(0, 0), (2, 6), (4, 0)], [(1, 2), (3, 2)]],
    "B": [[(0, 0), (0, 6), (3, 6), (3.6, 5.4), (3.6, 3.6), (3, 3), (0, 3)],
          [(3, 3), (3.8, 2.4), (3.8, 0.6), (3, 0), (0, 0)]],
    "C": [[(4, 5), (3, 6), (1, 6), (0, 5), (0, 1), (1, 0), (3, 0), (4, 1)]],
    "D": [[(0, 0), (0, 6), (2, 6), (3.6, 5), (3.6, 1), (2, 0), (0, 0)]],
    "E": [[(4, 6), (0, 6), (0, 0), (4, 0)], [(0, 3), (3, 3)]],
    "F": [[(4, 6), (0, 6), (0, 0)], [(0, 3), (3, 3)]],
    "G": [[(4, 5), (3, 6), (1, 6), (0, 5), (0, 1), (1, 0), (3, 0), (4, 1),
           (4, 3), (2, 3)]],
    "H": [[(0, 0), (0, 6)], [(4, 0), (4, 6)], [(0, 3), (4, 3)]],
    "I": [[(1, 6), (3, 6)], [(2, 6), (2, 0)], [(1, 0), (3, 0)]],
    "J": [[(3, 6), (3, 1), (2, 0), (1, 0), (0, 1)]],
    "K": [[(0, 0), (0, 6)], [(4, 6), (0, 3), (4, 0)]],
    "L": [[(0, 6), (0, 0), (4, 0)]],
    "M": [[(0, 0), (0, 6), (2, 3), (4, 6), (4, 0)]],
    "N": [[(0, 0), (0, 6), (4, 0), (4, 6)]],
    "O": [[(1, 0), (0, 1), (0, 5), (1, 6), (3, 6), (4, 5), (4, 1), (3, 0),
           (1, 0)]],
    "P": [[(0, 0), (0, 6), (3, 6), (3.8, 5.4), (3.8, 3.6), (3, 3), (0, 3)]],
    "Q": [[(1, 0), (0, 1), (0, 5), (1, 6), (3, 6), (4, 5), (4, 1), (3, 0),
           (1, 0)], [(2.5, 1.5), (4, 0)]],
    "R": [[(0, 0), (0, 6), (3, 6), (3.8, 5.4), (3.8, 3.6), (3, 3), (0, 3)],
          [(2, 3), (4, 0)]],
    "S": [[(4, 5), (3, 6), (1, 6), (0, 5), (0, 4), (1, 3), (3, 3), (4, 2),
           (4, 1), (3, 0), (1, 0), (0, 1)]],
    "T": [[(0, 6), (4, 6)], [(2, 6), (2, 0)]],
    "U": [[(0, 6), (0, 1), (1, 0), (3, 0), (4, 1), (4, 6)]],
    "V": [[(0, 6), (2, 0), (4, 6)]],
    "W": [[(0, 6), (1, 0), (2, 3), (3, 0), (4, 6)]],
    "X": [[(0, 0), (4, 6)], [(0, 6), (4, 0)]],
    "Y": [[(0, 6), (2, 3), (4, 6)], [(2, 3), (2, 0)]],
    "Z": [[(0, 6), (4, 6), (0, 0), (4, 0)]],
    "0": [[(1, 0), (0, 1), (0, 5), (1, 6), (3, 6), (4, 5), (4, 1), (3, 0),
           (1, 0)], [(1, 1), (3, 5)]],
    "1": [[(1, 5), (2, 6), (2, 0)], [(1, 0), (3, 0)]],
    "2": [[(0, 5), (1, 6), (3, 6), (4, 5), (4, 4), (0, 0), (4, 0)]],
    "3": [[(0, 5), (1, 6), (3, 6), (4, 5), (3, 3.4), (4, 2), (4, 1), (3, 0),
           (1, 0), (0, 1)], [(2, 3.4), (3, 3.4)]],
    "4": [[(3, 0), (3, 6), (0, 2), (4, 2)]],
    "5": [[(4, 6), (0, 6), (0, 3.4), (3, 3.4), (4, 2.4), (4, 1), (3, 0),
           (1, 0), (0, 1)]],
    "6": [[(4, 5), (3, 6), (1, 6), (0, 4), (0, 1), (1, 0), (3, 0), (4, 1),
           (4, 2), (3, 3), (0, 3)]],
    "7": [[(0, 6), (4, 6), (1, 0)]],
    "8": [[(1, 3), (0, 4), (0, 5), (1, 6), (3, 6), (4, 5), (4, 4), (3, 3),
           (1, 3), (0, 2), (0, 1), (1, 0), (3, 0), (4, 1), (4, 2), (3, 3)]],
    "9": [[(0, 1), (1, 0), (3, 0), (4, 1), (4, 5), (3, 6), (1, 6), (0, 5),
           (0, 4), (1, 3), (4, 3)]],
}

GLYPH_W = 4.0  # design width of a glyph cell (units)


def text_strokes(s: str, x: float, y: float, h: float = 6.0,
                 advance: float | None = None) -> list[list[tuple[float, float]]]:
    """Strokes (in mm) for ``s`` with its LEFT BASELINE at (x, y).

    ``h`` is cap height in mm; SVG y grows downward, so a stroke at design-y=6
    sits ``h`` mm above the baseline. Default advance is 5/6*h (1 unit gap)."""
    scale = h / 6.0
    adv = advance if advance is not None else 5.0 * scale
    out: list[list[tuple[float, float]]] = []
    cx = x
    for ch in s.upper():
        for stroke in GLYPHS.get(ch, []):
            out.append([(cx + px * scale, y - py * scale) for px, py in stroke])
        cx += adv
    return out


def text_width(s: str, h: float = 6.0, advance: float | None = None) -> float:
    adv = advance if advance is not None else 5.0 * (h / 6.0)
    return len(s) * adv


def glyph_centered(ch: str, cx: float, cy: float,
                   h: float = 6.0) -> list[list[tuple[float, float]]]:
    """Strokes for a single character centred on (cx, cy) — for grid cells."""
    scale = h / 6.0
    x = cx - (GLYPH_W * scale) / 2
    y = cy + h / 2  # baseline sits h/2 below the centre
    return [[(x + px * scale, y - py * scale) for px, py in stroke]
            for stroke in GLYPHS.get(ch.upper(), [])]