"""Shared helpers for the puzzle generators.

Each generator is a standalone script (``python generators/<name>.py``) that
emits a plot-ready SVG in millimetre page space. We reuse the engine's
dependency-free SVG toolkit from the sibling ``core`` checkout (same trick the
cities repo uses) so there's a single source of truth for page sizes and the
<g>-layer / document plumbing.

The physical target is the UUNA TEK iDraw 2.0. Its usable travel is only
~288 x 187 mm, so on a sheet-centred page the SHORT axis caps drawable width at
~150 mm — every generator defaults its content box to 150 mm and centres it, so
``artinscience-export --origin center`` lands it safely inside the envelope.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

_CORE = Path(__file__).resolve().parents[2] / "core" / "src"
if str(_CORE) not in sys.path:
    sys.path.insert(0, str(_CORE))

from artinscience import svg  # noqa: E402  (path set above)

# Letter is the stock on hand; A-sizes defer to the engine's table.
LETTER = (215.9, 279.4)
SAFE_CONTENT_MM = 150.0  # fits the iDraw's 187 mm short-axis travel, centred


def page_mm(name: str, orientation: str = "portrait") -> tuple[float, float]:
    if name.lower() == "letter":
        w, h = LETTER
        if orientation == "landscape":
            w, h = h, w
        return w, h
    return svg.size_mm(name, orientation)


def centered_box(w: float, h: float, size: float) -> tuple[float, float]:
    """Top-left corner of a ``size`` square centred on a ``w x h`` page."""
    return (w - size) / 2, (h - size) / 2


def circle_pts(cx: float, cy: float, r: float, seg: int = 96) -> list[tuple[float, float]]:
    return arc_pts(cx, cy, r, 0.0, 2 * math.pi, seg)


def arc_pts(cx: float, cy: float, r: float, a0: float, a1: float,
            seg: int = 64) -> list[tuple[float, float]]:
    return [(cx + r * math.cos(a0 + (a1 - a0) * i / seg),
             cy + r * math.sin(a0 + (a1 - a0) * i / seg)) for i in range(seg + 1)]


def save(path: str, w: float, h: float, body: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(svg.document(w, h, body))
    print(f"wrote {path}  ({w:.1f}x{h:.1f} mm)")