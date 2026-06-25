# CLAUDE.md — skytrack-oss session memory

> **Read this first** at the start of any session, and **refresh it** before
> clearing/compacting. Single source of truth for *what this is, where it stands,
> and where to resume.*

## What this is

`skytrack-oss` is an **open-source ecosystem** around the **SkyTrack** drone
simulation platform. Strategy: **open rim, closed hub** — open the
connectors/formats/tools/standards the community touches daily; keep the
proprietary value (Unity/Unreal engine, cloud "robot brain," hi-fidelity models,
fleet) in the commercial product **sn360**. Every project funnels adoption to sn360.

- **Product focus:** SkyTrack **drone** (Unity/Unreal, AirSim-style sim).
- **Second body:** a ground robot (an **Anki Vector** rebuild) is a *testbed /
  demo / second firmware target* — NOT a parallel product.
- **Ecosystem goal:** any audience (student, drone/robot researcher, startup) can
  **build their own product without permission** via small extension seams.
  Apache-2.0 lets them ship and sell what they build.

## The four pillars

| Folder | One-liner | Status |
|--------|-----------|--------|
| `sn360-bridge/` | Unity/Unreal ↔ PX4·MAVLink·ROS 2 (the AirSim successor) | runnable scaffold; real transport TODO |
| `robot-brain/` | `perceive→plan→act` + HAL; one brain, many bodies | working demos; DroneHAL falls back to sim |
| `drone-rehost/` | firmware rehosting harness + MAVLink fuzzer | self-test + fuzzer run; QEMU hook TODO |
| `scenario-format/` | open scenario interchange standard + validator | schema+examples+validator pass; player TODO |

Each folder is a **self-contained mini-repo** (own README, LICENSE, `CLAUDE.md`,
`docs/`) splittable via `git subtree split` (recipe in `README.md`).

## Ecosystem layers (beyond the 4 pillars)

Community (docs site, examples gallery, tutorials, papers hub) · Pillars ·
Interchange standards (scenario spec, telemetry, model API, brain↔HAL,
report schema) · **`skytrack-core`** (shared ENU frame/types/transport — the
KEYSTONE, not yet built) · Assets/data (datasets, benchmarks, model zoo, body
packs). See [`ECOSYSTEM.md`](./ECOSYSTEM.md) and [`docs/DIAGRAMS.md`](./docs/DIAGRAMS.md).

## Extension seams (how outsiders build)

`Brain`, `HAL` (`robot-brain/core/brain.py`), `Peripheral`
(`drone-rehost/peripherals/base.py`), `IBridgeTransport`
(`sn360-bridge/unity/MotorSubscriber.cs`), the scenario JSON Schema. Guide:
[`docs/EXTENDING.md`](./docs/EXTENDING.md). Proof: `robot-brain/examples/
custom_brain_obstacle_avoid.py` (a custom Brain in ~15 lines, verified).

## Smoke tests (verify the world still works)

```bash
cd skytrack-oss
python robot-brain/examples/one_brain_two_bodies.py
python robot-brain/examples/custom_brain_obstacle_avoid.py
python drone-rehost/harness/rehost.py
python drone-rehost/fuzzer/mavlink_fuzzer.py -n 5000
pip install -r scenario-format/validator/requirements.txt
python scenario-format/validator/validate.py scenario-format/examples/
python sn360-bridge/common/mavlink_bridge.py --dry-run --seconds 3
```

## Conventions

- **Frame:** ENU meters; convert at edges (MAVLink NED, Unity Y-up, Unreal Z-up/cm).
- **Diagrams:** three formats available — ASCII (`docs/DIAGRAMS.md`, preferred for
  in-repo), rendered Graphviz SVG/PNG (`docs/diagrams/`, for decks/site), and
  Mermaid (per-project `docs/`, not yet converted — see backlog). Regenerate
  images: `cd docs/diagrams && for f in *.dot; do dot -Tsvg $f -o ${f%.dot}.svg; done`.
- **Funnel:** every README/doc ends with a "scale this up → sn360" CTA.
- **Branch:** develop on `claude/skytrack-oss-ideas-0ivndv`. Don't push elsewhere.
- **License:** Apache-2.0 throughout.

## Doc map

- Start/memory: `CLAUDE.md` (this) · [`CONTEXT.md`](./CONTEXT.md) ·
  [`BACKLOG.md`](./BACKLOG.md) · [`OSS-STRATEGY.md`](./OSS-STRATEGY.md) ·
  [`ECOSYSTEM.md`](./ECOSYSTEM.md)
- Platform docs: [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md) ·
  [`docs/FLOW.md`](./docs/FLOW.md) · [`docs/JOURNEY.md`](./docs/JOURNEY.md) ·
  [`docs/DIAGRAMS.md`](./docs/DIAGRAMS.md) ·
  [`docs/IDEAS-OVERVIEW.md`](./docs/IDEAS-OVERVIEW.md) ·
  [`docs/EXTENDING.md`](./docs/EXTENDING.md)
- Per project: each folder's `CLAUDE.md` + `docs/{IDEA,ARCHITECTURE,FLOW,JOURNEY,
  STRATEGY,BACKLOG}.md`

## Where to resume

**Current top priority:** extract **`skytrack-core`** (the keystone), then wire
real MAVLink transport into `sn360-bridge` and bind it in `robot-brain`'s
`DroneHAL` so a brain actually flies PX4 SITL. See [`BACKLOG.md`](./BACKLOG.md).

## Refresh checklist (before starting OR clearing/compacting a session)

1. Re-read this file, `README.md`, `CONTEXT.md`, `BACKLOG.md`, `ECOSYSTEM.md`.
2. `git status` and confirm branch `claude/skytrack-oss-ideas-0ivndv`.
3. Run the smoke tests above; fix or note any regressions here.
4. Update **Status**, **Where to resume**, and `BACKLOG.md` with what changed
   this session, then commit — so the next session starts current.
