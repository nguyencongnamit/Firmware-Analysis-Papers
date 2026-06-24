# CLAUDE.md — robot-brain session memory

> Read this first when starting or resuming work on `robot-brain`. It is the
> fast refresh on what this project is, what works today, and where to pick up.

## One-paragraph summary

`robot-brain` is an open, **body-agnostic autonomy interface**: write the brain
once as `perceive → plan → act`, and run it unchanged on a drone, a ground
robot, or in pure simulation by swapping a **hardware-abstraction layer (HAL)**.
It rides the embodied-AI / VLA wave by defining a tiny, stable contract instead
of yet another one-off LLM-on-a-robot bolt-on. It is part of
[`skytrack-oss`](../): the interface and a small local tier are open; the hosted
large-model brain, fleet orchestration, and managed evals live in **sn360**. The
**SkyTrack drone** is the product focus; the ground robot is a cheap, safe
indoor **testbed/demo**, not a parallel product.

## Current status

- **Works today (verified):**
  - The contract: `Brain` ABC + `HAL` ABC + body-agnostic `run()` loop (`core/brain.py`).
  - `ReferenceBrain` (`core/reference_brain.py`): dead-reckoning `perceive` +
    proportional waypoint `plan`, pass-through `act`. Dependency-free.
  - Three HALs: `SimHAL` (kinematic), `DroneHAL`, `GroundRobotHAL` (`adapters/`).
  - `examples/one_brain_two_bodies.py` runs the **same** `ReferenceBrain` on a
    drone body and a rover body — **smoke-tested, exits 0**.
- **TODO / not built yet:**
  - **`DroneHAL` still falls back to the kinematic `SimHAL`.** It carries an
    `endpoint` field but does NOT yet speak real MAVLink/ROS 2 — the
    `sn360-bridge` transport is not wired. This is the #1 milestone (M1).
  - No real VLM perceiver / LLM planner reference path yet (M2).
  - No real Vector/ground-robot adapter (SDK / wire-pod) yet (M3).
  - No scenario-format runner (M4) and no evals (M5).
  - The top-level `README.md` Status/Roadmap section still says "scaffold /
    interfaces only" — the code has since moved ahead of it (the contract,
    reference brain, HALs, and example all run).

## Key files map

| Path | What it is |
|------|------------|
| `core/types.py` | Data types: `Observation`, `WorldState`, `Goal`, `Plan`, `Command`, `CommandKind`, `Vec3` |
| `core/brain.py` | `Brain` ABC, `HAL` ABC, and the `run(brain, hal, goals)` loop |
| `core/reference_brain.py` | `ReferenceBrain` — trivial P-controller reference implementation |
| `core/__init__.py` | Public exports |
| `adapters/sim_hal.py` | `SimHAL` — pure-Python kinematic body, the shared math |
| `adapters/drone_hal.py` | `DroneHAL` — multirotor body; falls back to `SimHAL` until sn360-bridge wired |
| `adapters/ground_robot_hal.py` | `GroundRobotHAL` — z-locked, slow envelope testbed body |
| `adapters/__init__.py` | HAL exports |
| `examples/one_brain_two_bodies.py` | Same brain on drone + rover; the canonical demo |
| `docs/CONTRACT.md` | The two-abstraction contract, rationale, adapter table |
| `docs/` | This and the other design docs (IDEA, ARCHITECTURE, FLOW, JOURNEY, STRATEGY, BACKLOG) |

## How to run

```bash
cd skytrack-oss/robot-brain
python examples/one_brain_two_bodies.py
```

Expected: two lines reporting `reached goals=True` for `[drone]` and `[rover]`,
process exits 0. No engine, hardware, or third-party deps required.

## Conventions

- **Architecture:** `perceive → plan → act` in the brain; `read_sensors` /
  `send_commands` / `goal_reached` in the HAL. The brain never names a body; the
  HAL never contains autonomy logic.
- **Frame & units:** ENU, meters, m/s, radians; time in seconds since scenario start.
- **Types are frozen dataclasses**, deliberately small and serializable.
- **License:** Apache-2.0 (per-folder `LICENSE`).
- **Funnel:** everything points at **sn360** for the hosted big-model brain +
  fleet. Open the rim, keep the hub.
- **Bodies:** the **drone is the product**; the **ground robot is the testbed**.
  Rule of thumb: improve the shared brain/sim/firmware → do it; improve only a
  side body → skip it.

## Where to resume

→ **[`docs/BACKLOG.md`](./docs/BACKLOG.md)** — prioritized milestones (M1–M5).
The next concrete work is **M1: wire `DroneHAL` to real sn360-bridge MAVLink/ROS 2
transport** so the drone body stops falling back to the kinematic sim.

## Other docs

- [`docs/IDEA.md`](./docs/IDEA.md) — vision, painpoint, value, funnel.
- [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md) — contracts, run loop, type system, where AI plugs in.
- [`docs/FLOW.md`](./docs/FLOW.md) — the control loop and the goto/GPS-denied flow.
- [`docs/JOURNEY.md`](./docs/JOURNEY.md) — developer journey from free sim to sn360.
- [`docs/STRATEGY.md`](./docs/STRATEGY.md) — positioning, open-vs-sn360 split, go-to-market.
- [`docs/BACKLOG.md`](./docs/BACKLOG.md) — milestones and current scaffold state.
- [`docs/CONTRACT.md`](./docs/CONTRACT.md) — the canonical contract reference.
- [`README.md`](./README.md) — public-facing overview.

## Refresh checklist before starting or clearing a session

- [ ] Re-read this `CLAUDE.md`, the project [`README.md`](./README.md), and [`docs/BACKLOG.md`](./docs/BACKLOG.md).
- [ ] Confirm the git branch is `claude/skytrack-oss-ideas-0ivndv`.
- [ ] Run the smoke test: `python examples/one_brain_two_bodies.py` (expect exit 0, both bodies reach goals).
- [ ] Remember the standing TODO: `DroneHAL` still falls back to kinematic sim — M1 wires the real transport.
- [ ] Docs only here — do not modify code unless the task explicitly asks.
