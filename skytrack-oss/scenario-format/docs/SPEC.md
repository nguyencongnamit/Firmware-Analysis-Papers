# Scenario format specification (v0.1.0)

A scenario is a single JSON document that fully describes a reproducible
drone/robot test: the world, the agents and their missions, injected faults, and
the criteria that decide pass/fail. Everything needed to replay is in the file.

## Top-level fields

| Field | Required | Description |
|-------|----------|-------------|
| `scenario_version` | yes | Schema version this file targets (`0.1.x`). |
| `name` | yes | Human-readable name. |
| `description` | no | Free text. |
| `seed` | no | Deterministic RNG seed; same seed + same file → same run. |
| `world` | yes | Origin (lat/lon/alt) + `environment`. |
| `agents` | yes | One or more agents with a `body`, `start`, and `mission`. |
| `faults` | no | Injected faults with a `trigger.at_s` and optional `duration_s`. |
| `success_criteria` | yes | Conditions evaluated to decide pass/fail. |

## Coordinate frame

Agent `start.position`, `mission[].target`, and criterion `target` are
`[x, y, z]` in **meters, local ENU** relative to `world.origin` (x=East,
y=North, z=Up).

## Bodies

`multirotor`, `fixed_wing`, `ground_robot`. The body selects which actuator/HAL
the runtime binds (see `robot-brain`).

## Mission actions

`takeoff`, `goto`, `hover`, `land`, `follow`, `return_home`. `goto`/`follow` use
`speed_mps`; `hover` uses `duration_s`.

## Faults

`sensor_dropout` (targets a sensor name, e.g. `imu`), `gps_denied`, `wind_gust`,
`motor_loss`, `comms_loss` (the latter four target an agent `id`).

## Success criteria

`reach_waypoint`, `stay_within_geofence`, `land_within_radius`, `no_crash`,
`max_mission_time`. Omit `agent` on `no_crash`/`max_mission_time` to apply to all
agents.

## Validation

```bash
pip install -r ../validator/requirements.txt
python ../validator/validate.py ../examples/
```

The validator runs the JSON Schema plus cross-field lint checks (e.g. faults and
criteria referencing unknown agents).

## Versioning

The schema is semantically versioned. Within `0.1.x`, only backward-compatible
additions land. Breaking changes bump the minor (pre-1.0) and require scenarios
to update their `scenario_version`.

## Scale this up

The format is free and portable. Running thousands of scenarios at high fidelity
with analytics → **sn360**.
