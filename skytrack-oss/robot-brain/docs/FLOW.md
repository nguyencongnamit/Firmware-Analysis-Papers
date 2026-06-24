# FLOW — the perceive → plan → act control loop

The `run()` loop (`core/brain.py`) drives a list of goals to completion. For
each goal it spins a tight `perceive → plan → act` cycle until the HAL reports
the goal reached (or `max_steps` is hit).

## Control loop (one step)

```mermaid
sequenceDiagram
    participant App as run(brain, hal, goals)
    participant HAL
    participant Brain

    Note over App: for each goal in goals
    loop until hal.goal_reached(goal) or max_steps
        App->>HAL: goal_reached(goal)?
        HAL-->>App: False (not yet)
        App->>HAL: read_sensors()
        HAL-->>App: Observation (t, position, velocity,<br/>attitude, gps_ok, imu_ok)
        App->>Brain: perceive(Observation)
        Brain-->>App: WorldState (+ localization_ok)
        App->>Brain: plan(WorldState, goal)
        Brain-->>App: Plan (intents + rationale)
        App->>Brain: act(Plan)
        Brain-->>App: list[Command]
        App->>HAL: send_commands(commands)
        Note over HAL: integrate / actuate, advance time
    end
    App->>HAL: goal_reached(goal)?
    HAL-->>App: True → next goal
```

When every goal reports reached within `max_steps`, `run()` returns `True`;
otherwise it returns `False`.

## How a `goto` goal resolves (with the degraded-localization branch)

`ReferenceBrain.plan` steers a proportional velocity toward the target, eased in
as it approaches. `perceive` sets `localization_ok = gps_ok and imu_ok`; when
GPS (or IMU) drops, the brain keeps flying on inertial/dead-reckoning and
annotates the plan rationale as **localization degraded** rather than stopping.
`SimHAL.goal_reached` declares arrival within 0.5 m of the target.

```mermaid
flowchart TD
    START(["Goal: goto target @ speed"]) --> READ["hal.read_sensors() → Observation"]
    READ --> PERCEIVE["brain.perceive()"]
    PERCEIVE --> LOC{"gps_ok AND imu_ok?"}

    LOC -->|yes| OKSTATE["WorldState.localization_ok = True"]
    LOC -->|no| DEGRADED["WorldState.localization_ok = False<br/>notes: gps_ok / imu_ok<br/>(keep flying on inertial /<br/>dead-reckoning)"]

    OKSTATE --> PLAN
    DEGRADED --> PLAN["brain.plan(state, goal)<br/>dx = target − position<br/>speed = min(goal.speed, dist)<br/>vel = unit(dx) · speed"]
    DEGRADED -. "rationale: '(localization degraded)'" .-> PLAN

    PLAN --> ACT["brain.act() → [VELOCITY command]"]
    ACT --> SEND["hal.send_commands()<br/>clamp to body max_speed,<br/>integrate, advance t"]
    SEND --> REACHED{"dist(position, target) ≤ 0.5 m?"}
    REACHED -->|no| READ
    REACHED -->|yes| DONE(["goal reached → next goal"])

    style DEGRADED fill:#fff3e0,stroke:#e65100
    style DONE fill:#e8f5e9,stroke:#2e7d32
```

### Notes on the body-specific behavior in this flow

- **`SimHAL`** clamps the velocity vector to its `max_speed`, integrates with a
  fixed `dt`, and keeps `z ≥ 0`.
- **`DroneHAL`** uses a tighter envelope (`max_speed = 12.0`) and *today*
  inherits the kinematic integration — real MAVLink/ROS 2 transport via
  `sn360-bridge` is TODO (see [BACKLOG M1](./BACKLOG.md)).
- **`GroundRobotHAL`** flattens any `z` intent (no takeoff/altitude), pins
  `z = 0`, and uses a slow envelope (`max_speed = 1.5`) so the same brain can be
  iterated safely indoors.
- For a **`hover`** goal with a `deadline`, `goal_reached` returns true once
  `t ≥ deadline` rather than on a position test.
