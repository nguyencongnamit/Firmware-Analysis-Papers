# Rendered diagrams (Graphviz / DOT)

Non-Mermaid, non-ASCII diagrams: **diagrams-as-code** in Graphviz `DOT`, rendered
to `SVG` (scalable, for docs/web) and `PNG` (140 dpi, for slides/decks). The
`.dot` files are the git-friendly source of truth; the images are generated.

| Diagram | Source | SVG | PNG |
|---------|--------|-----|-----|
| Ecosystem dependency + funnel | `ecosystem.dot` | `ecosystem.svg` | `ecosystem.png` |
| Ecosystem layers (rim → hub) | `layers.dot` | `layers.svg` | `layers.png` |
| sn360-bridge architecture | `bridge.dot` | `bridge.svg` | `bridge.png` |
| robot-brain (one brain, many bodies) | `robot-brain.dot` | `robot-brain.svg` | `robot-brain.png` |
| drone-rehost (MMIO dispatch) | `rehost.dot` | `rehost.svg` | `rehost.png` |
| scenario-format (model + pipeline) | `scenario.dot` | `scenario.svg` | `scenario.png` |

## Regenerate

```bash
# needs graphviz:  apt-get install -y graphviz   (or: brew install graphviz)
cd skytrack-oss/docs/diagrams
for f in *.dot; do
  dot -Tsvg "$f" -o "${f%.dot}.svg"
  dot -Tpng -Gdpi=140 "$f" -o "${f%.dot}.png"
done
```

## Why Graphviz here

- **Diagrams-as-code** — diffable, reviewable in PRs, no GUI.
- **Renders to real images** — unlike Mermaid (needs a renderer) or ASCII (text
  only), these drop straight into a pitch deck, docs site, or paper.
- Colour legend: blue = pillars · yellow = `skytrack-core` keystone · green =
  engine/validator · purple = brain/oracle · pink = data/fuzz · orange/3-D =
  sn360 hub · dashed red = planned/TODO.

ASCII equivalents live in [`../DIAGRAMS.md`](../DIAGRAMS.md); Mermaid versions are
in the per-project `docs/ARCHITECTURE.md` / `FLOW.md` files.
