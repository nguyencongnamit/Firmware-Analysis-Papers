# BACKLOG

Prioritized milestones for `robot-brain`. Honest about current state: the
**contract, reference brain, three HALs, and the two-bodies example all work and
are smoke-tested** — but the parts that make it real (live drone transport, a
genuine model-driven brain, a real rover adapter, scenario integration, evals)
are **not built yet**. Everything below marked unchecked is planned/TODO.

## Done (current scaffold)

- [x] Core contract: `Brain` ABC + `HAL` ABC + body-agnostic `run()` loop (`core/brain.py`).
- [x] Type system: frozen dataclasses in `core/types.py` (ENU/meters/seconds).
- [x] `ReferenceBrain`: dead-reckoning `perceive` + proportional `plan` + pass-through `act`.
- [x] `SimHAL` kinematic body (shared integration math).
- [x] `DroneHAL` and `GroundRobotHAL` (extend `SimHAL`; body-specific limits).
- [x] `examples/one_brain_two_bodies.py` — same brain on drone + rover, **verified (exit 0)**.

## M1 — Real `DroneHAL` transport (highest priority)

> Today `DroneHAL` carries an `endpoint` field but **falls back to the kinematic
> `SimHAL`**. This milestone makes the drone body actually fly through hardware/SITL.

- [ ] Wire `DroneHAL` to a real **`sn360-bridge`** client (MAVLink / ROS 2).
- [ ] Sensing: read `LOCAL_POSITION_NED` / `ATTITUDE` → populate `Observation`
      (convert NED ↔ ENU; set `gps_ok` / `imu_ok` from link/health).
- [ ] Actuation: send `SET_POSITION_TARGET_LOCAL_NED` velocity setpoints from
      `VELOCITY` commands; map `TAKEOFF` / `LAND` / `HOLD`.
- [ ] Lifecycle: heartbeat, OFFBOARD/OFFBOARD-equivalent mode, arm/disarm, failsafe.
- [ ] Keep the kinematic fallback when `endpoint` is unset (so examples still run anywhere).
- [ ] Validate against PX4 SITL via `sn360-bridge` (e.g. `udp:127.0.0.1:14540`).

## M2 — Local small-model reference path

> The open "free tier" intelligence: a real (if small) model-driven brain behind
> the same interface, distinct from sn360's hosted large-model brain.

- [ ] Small-**VLM** perceiver: consume `Observation.extras` (camera/depth) → richer `WorldState`.
- [ ] Small-**LLM** planner: reason over `WorldState` + `Goal` → higher-level intents.
- [ ] Implement a non-trivial `act()` that lowers abstract intents into `Command`s.
- [ ] Reference example running the model brain on `SimHAL` / `GroundRobotHAL`.
- [ ] Document the local-vs-hosted (sn360) split and the upgrade seam.

## M3 — Real ground-robot adapter

> Turn the testbed body from kinematic-only into a real desk robot.

- [ ] `GroundRobotHAL` real transport: Vector SDK / **wire-pod** (or ROS 2 via `sn360-bridge`).
- [ ] Map `VELOCITY` → wheel/drive commands; read pose/odometry → `Observation`.
- [ ] Honor the slow, z-locked safety envelope on real hardware.
- [ ] Demo: iterate a brain on the rover, then bind the same brain to `DroneHAL`.

## M4 — `scenario-format` runner

> Let brains run standard, reproducible scenarios; ties into the sibling
> `scenario-format` project.

- [ ] Loader: parse a `scenario-format` mission into `Goal`s (and fault injections).
- [ ] Drive `Goal.kind` from scenario actions (goto / hover / takeoff / land / follow).
- [ ] Use `SimHAL` fault hooks (`gps_ok` / `imu_ok`) for GPS-denied / degraded scenarios.
- [ ] CLI: run a brain over a scenario file and report goal completion.

## M5 — Evals

> Measure brains objectively; managed/scaled evals are an sn360 hook, but a local
> baseline is open.

- [ ] Metrics: goal success rate, path efficiency, time-to-goal, safety violations.
- [ ] Run a brain across a scenario suite and produce a scorecard.
- [ ] Regression baseline so brain changes can be compared.
- [ ] Document the local-eval → **sn360 managed-evals** funnel.

## Housekeeping

- [ ] Update the project `README.md` Status/Roadmap (it still says "scaffold /
      interfaces only"; the contract, reference brain, HALs, and example now run).
- [ ] Add tests around `run()`, `ReferenceBrain`, and each HAL.
- [ ] Keep `CLAUDE.md` in sync as milestones land.
