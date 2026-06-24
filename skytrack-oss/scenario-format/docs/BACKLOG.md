# BACKLOG

Prioritized milestones for `scenario-format`. Honest about what exists today.

## Current state (done)

- [x] Schema `schema/scenario.schema.json` — JSON Schema draft 2020-12, v0.1.0
  (top-level `scenario_version`/`name`/`world`/`agents`/`faults`/`success_criteria`;
  ENU-meters local frame; bodies, actions, faults, criteria enumerated).
- [x] Validator `validator/validate.py` — `Draft202012Validator` + cross-field
  lint (unknown agent refs in faults/criteria). Exit `0`/`1`.
- [x] 4 reference examples, all validate: `gps_denied_approach.json`,
  `wind_gust.json`, `sensor_dropout.json`, `swarm_formation.json`.
- [x] Spec (`docs/SPEC.md`) covering v0.1.0.

**Not built yet:** reference player, result/report schema, scenario gallery, CI.

## M1 — Schema additions (backward-compatible `0.1.x`)

- [ ] Richer fault parameters (e.g. partial sensor degradation, `gps_denied`
      drift model params, `wind_gust` direction/profile, `motor_loss` which motor).
- [ ] Swarm formation blocks — first-class formation/relative-position primitives
      so `follow`/formation intent isn't encoded only as raw waypoints.
- [ ] Per-action conveniences (e.g. `goto` arrival tolerance, `loiter`).
- [ ] Keep every addition optional so existing examples still validate.

## M2 — Reference player

- [ ] CLI player that loads a validated scenario and **drives `sn360-bridge`**
      (MAVLink · PX4 · ROS 2) to execute it.
- [ ] Schedule fault injection at `trigger.at_s` for `duration_s`.
- [ ] Bind body → HAL via `robot-brain` (multirotor / fixed_wing / ground_robot).
- [ ] Honor `seed` for deterministic playback where the runtime allows.

## M3 — Result / report schema (pass/fail)

- [ ] An open JSON-Schema for run results: per-criterion pass/fail, measured
      values, timestamps, scenario hash + version.
- [ ] Player emits a report conforming to it.
- [ ] Validator (or a sibling tool) can validate reports too.
- [ ] Make reports diffable so regressions are reviewable in git.

## M4 — More examples + scenario gallery

- [ ] Expand beyond the 4 examples (fixed-wing, ground_robot, multi-fault,
      geofence-heavy, longer swarms).
- [ ] A browsable gallery (`docs/` index) describing each scenario + expected
      outcome.
- [ ] Contribution guide for adding gallery scenarios.

## M5 — Versioning / governance + CI

- [ ] Documented schema-change process + extension (`x-`) namespace convention.
- [ ] Deprecation policy ahead of 1.0.
- [ ] **CI that validates every example on each commit** (the guardrail that
      keeps the format trustworthy).
- [ ] Publish versioned schemas resolvable by `$id`.

## Resume here

Pick up at **M1** (schema additions) or **M2** (reference player) — M2 is the
highest-leverage step toward proving the format end-to-end and wiring the funnel
into `sn360-bridge`. Run the validator smoke test first:

```bash
pip install -r validator/requirements.txt
python validator/validate.py examples/
```
