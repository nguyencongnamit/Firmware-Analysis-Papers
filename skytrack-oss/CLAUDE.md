# CLAUDE.md — skytrack-oss session memory

> **Read this first** at the start of any session, and **refresh it** before
> clearing/compacting a session. It is the single source of truth for *what this
> is, where it stands, and where to resume.*

## What this is

`skytrack-oss` is a **monorepo of four open-source projects** that orbit the
**SkyTrack** drone simulation platform. Strategy: **open rim, closed hub** — open
the connectors/formats/tools the community touches daily; keep the proprietary
value (Unity/Unreal engine, cloud "robot brain," hi-fidelity models, fleet) in
the commercial product **sn360**. Every project funnels adoption back to sn360.

- **Product focus:** SkyTrack **drone** (Unity/Unreal, AirSim-style sim).
- **Second body:** a ground robot (an **Anki Vector** rebuild) is a *testbed /
  demo / second firmware target* — NOT a parallel product.
- **License:** Apache-2.0 across all projects.

## The four projects

| Folder | One-liner | Status |
|--------|-----------|--------|
| `sn360-bridge/` | Unity/Unreal ↔ PX4·MAVLink·ROS 2 (the AirSim successor) | runnable scaffold; real transport TODO |
| `robot-brain/` | `perceive→plan→act` + HAL; one brain, many bodies | working demo; DroneHAL falls back to sim |
| `drone-rehost/` | firmware rehosting harness + MAVLink fuzzer | self-test + fuzzer run; QEMU hook TODO |
| `scenario-format/` | open scenario interchange standard + validator | schema+examples+validator all pass; player TODO |

Each folder is a **self-contained mini-repo** (own README, LICENSE, `CLAUDE.md`,
`docs/`) ready to split out via `git subtree split` (recipe in `README.md`).

## Smoke tests (verify the world still works)

```bash
cd skytrack-oss
python robot-brain/examples/one_brain_two_bodies.py            # one brain, two bodies
python drone-rehost/harness/rehost.py                          # MMIO bus self-test
python drone-rehost/fuzzer/mavlink_fuzzer.py -n 5000           # MAVLink fuzzer
pip install -r scenario-format/validator/requirements.txt
python scenario-format/validator/validate.py scenario-format/examples/
python sn360-bridge/common/mavlink_bridge.py --dry-run --seconds 3
```

## Conventions

- **Frame:** ENU meters (x=East, y=North, z=Up). Convert at the edges
  (MAVLink NED, Unity Y-up, Unreal Z-up/cm).
- **Funnel:** every README/doc ends with a "scale this up → sn360" CTA.
- **Branch:** develop on `claude/skytrack-oss-ideas-0ivndv`. Don't push elsewhere.
- **Docs per project:** `CLAUDE.md` (this kind of file), `docs/IDEA.md`,
  `docs/ARCHITECTURE.md`, `docs/FLOW.md`, `docs/JOURNEY.md`, `docs/STRATEGY.md`,
  `docs/BACKLOG.md`.

## Where to resume

- Cross-project plan & priorities: [`BACKLOG.md`](./BACKLOG.md)
- Why decisions were made (the conversation history): [`CONTEXT.md`](./CONTEXT.md)
- Strategy detail: [`OSS-STRATEGY.md`](./OSS-STRATEGY.md)
- Platform-level diagrams: [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md),
  [`docs/JOURNEY.md`](./docs/JOURNEY.md)
- Per-project next steps: each `*/docs/BACKLOG.md`

**Current top priority:** wire `sn360-bridge` real MAVLink transport and bind it
into `robot-brain`'s `DroneHAL` so a brain actually flies PX4 SITL. See
`sn360-bridge/docs/BACKLOG.md` M1–M2 and `robot-brain/docs/BACKLOG.md` M1.

## Refresh checklist (before starting OR clearing/compacting a session)

1. Re-read this file, `README.md`, `CONTEXT.md`, and `BACKLOG.md`.
2. `git status` and confirm branch `claude/skytrack-oss-ideas-0ivndv`.
3. Run the smoke tests above; fix or note any regressions here.
4. Update **Status**, **Where to resume**, and `BACKLOG.md` with anything done
   or learned this session, then commit — so the next session starts current.
