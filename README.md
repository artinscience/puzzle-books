# artinscience · puzzle-books

Algorithmic **mazes, word & logic puzzles, kids' activity & coloring books, and
print-and-play games** — generated as plottable line art.

**What fits (all natively plottable line art):**
- **Mazes** — procedural (recursive backtracker / Prim), incl. *shaped* mazes in
  an animal, letter, or map outline.
- **Word & logic puzzles** — word search, crosswords, nonograms.
- **Coloring pages / books** — geometric, mandalas, or themed.
- **Dot-to-dot, spirograph, hidden-picture, print-and-play games.**

---

## Generators

Self-contained scripts in [`generators/`](generators/) emit plot-ready SVG in
millimetre page space, reusing the engine's dependency-free SVG toolkit from the
sibling `../core` checkout. **Generation needs only `python3`** — no venv, no Nix
shell. Each takes `--seed` (deterministic), `--page` (default `letter`, the
stock on hand), and `--size` (content box, default 150 mm).

```sh
make new TYPE=maze       DIFF=intermediate     # -> output/maze-intermediate-NN.svg (auto-numbered)
make new TYPE=mandala    DIFF=ultra            # -> output/mandala-ultra-NN.svg
make new TYPE=spiro      DIFF=beginner         # -> output/spiro-beginner-NN.svg
make new TYPE=wordsearch DIFF=hard             # -> output/wordsearch-hard-NN.svg
make batch SEED=7                              # one (untiered) of each, quick test
```

- `strokefont.py` — a compact single-stroke uppercase + digit font, so word-search
  letters and titles plot as centre-lines (outline fonts plot hollow).
- Content is centred and capped at 150 mm so it fits the iDraw 2.0's travel
  envelope when exported with `--origin corner --margin 33` (see *To paper*).

### Naming convention & difficulty tiers

Output files follow **`<type>-<difficulty>-<NN>`**, e.g. `maze-beginner-01.svg`.
`NN` is an auto-incrementing variation number — many distinct puzzles can share a
type+difficulty (`maze-beginner-01`, `-02`, `-03`, …). The plate's title prints
the tier. Every type uses the same five tiers (`beginner` → `ultra`) but on its
own complexity axis — *solve-difficulty* for the puzzles, *visual intricacy /
passes* for the decorative ones:

| Tier | maze `--cells` | wordsearch `--grid` | mandala `--fold`/`--bands` | spiro `--petals` |
|---|---|---|---|---|
| `beginner` | 10 | 9 | 6 / 2 | 5 |
| `intermediate` | 20 | 12 | 10 / 3 | 11 |
| `hard` | 30 | 15 | 14 / 4 | 17 |
| `advanced` | 40 | 18 | 18 / 5 | 23 |
| `ultra` | 50 | 21 | 22 / 6 | 31 |

Generate the next variation of any tier (auto-numbered; `seed = NN`; title set
automatically):

```sh
make new TYPE=maze    DIFF=beginner    # -> maze-beginner-NN.svg at the next free NN
make new TYPE=spiro   DIFF=ultra       # -> spiro-ultra-NN.svg
```

`TYPE` ∈ `maze | wordsearch | mandala | spiro`. The seed varies the *shape* while
the tier fixes the complexity (e.g. all `spiro-ultra` variations have 31 petals
but different curves). Maze `advanced`/`ultra` corridors (≤3.75 mm) plot fine
with a 0.5 mm pen but are tight — nudge the export `--margin` down to enlarge them
if needed.

### To paper

Export + plot live in `core` (export needs `vpype`). Homing is automatic — each
plot re-homes to the repeatable origin, then plots:

```sh
artinscience-export output/maze-hard-01.svg output/maze-hard-01.gcode \
    --origin corner --margin 33 --frame output/maze-hard-01-frame.gcode
artinscience-plot   stream output/maze-hard-01.gcode
```

If a plot is aborted, errors, or loses power partway, recover with
`artinscience-plot stream <gcode> --resume` (auto-checkpointed every 50 lines for
jobs ≥ 200 lines; re-load the same sheet first). See `core`'s README → *Plot* for
the full recovery + setup workflow.

---

Part of the artinscience project — generative pen-plotter art.
