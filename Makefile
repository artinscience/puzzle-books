.PHONY: all maze new spiro mandala wordsearch batch clean
# Procedural puzzle generators -> plot-ready SVG in output/.
# Pure stdlib + the engine's artinscience.svg (sibling ../core checkout); no
# venv/nix shell needed to GENERATE. Export (vpype) + plot run from core.
PY    ?= python3
SEED  ?= 1
OUT   ?= output

all: batch

maze:
	$(PY) generators/maze.py --seed $(SEED) -o $(OUT)/maze-$(SEED).svg

# New puzzle in the <type>-<difficulty>-<NN> convention, auto-numbered.
#   make new TYPE=maze DIFF=beginner       (TYPE: maze|wordsearch|mandala|spiro)
#                                          (DIFF: beginner|intermediate|hard|advanced|ultra)
# Each type ramps its own complexity knob across the 5 tiers; NN = next free
# number; seed = NN; the plate title is set automatically.
new:
	@t='$(TYPE)'; d='$(DIFF)'; \
	i=$$(case "$$d" in beginner) echo 1;; intermediate) echo 2;; hard) echo 3;; advanced) echo 4;; ultra) echo 5;; *) echo 0;; esac); \
	if [ "$$i" = 0 ]; then echo "DIFF must be beginner|intermediate|hard|advanced|ultra"; exit 1; fi; \
	pick() { echo "$$1" | cut -d' ' -f$$i; }; \
	case "$$t" in \
	  maze)       arg="--cells $$(pick '10 20 30 40 50')"; script=maze;; \
	  wordsearch) arg="--grid $$(pick '9 12 15 18 21')"; script=wordsearch;; \
	  mandala)    arg="--fold $$(pick '6 10 14 18 22') --bands $$(pick '2 3 4 5 6')"; script=mandala;; \
	  spiro)      arg="--petals $$(pick '5 11 17 23 31')"; script=spirograph;; \
	  *) echo "TYPE must be maze|wordsearch|mandala|spiro"; exit 1;; esac; \
	n=1; while [ -f "$(OUT)/$$t-$$d-$$(printf '%02d' $$n).svg" ]; do n=$$((n+1)); done; \
	nn=$$(printf '%02d' $$n); T=$$(echo "$$d" | tr a-z A-Z); \
	echo "generating $$t-$$d-$$nn ($$arg, seed=$$n)"; \
	$(PY) generators/$$script.py --seed $$n $$arg --title "$$T $$nn" -o "$(OUT)/$$t-$$d-$$nn.svg"

spiro:
	$(PY) generators/spirograph.py --seed $(SEED) --title SPIROGRAPH -o $(OUT)/spiro-$(SEED).svg

mandala:
	$(PY) generators/mandala.py --seed $(SEED) -o $(OUT)/mandala-$(SEED).svg

wordsearch:
	$(PY) generators/wordsearch.py --seed $(SEED) -o $(OUT)/wordsearch-$(SEED).svg

# One of each, for a quick plot session.
batch: maze spiro mandala wordsearch

clean:
	rm -f $(OUT)/*.svg $(OUT)/*.png && find . -name __pycache__ -type d -prune -exec rm -rf {} +