# The robot-brain contract

Two abstractions, deliberately tiny:

```
Brain:  perceive(Observation) -> WorldState
        plan(WorldState, Goal) -> Plan
        act(Plan)             -> [Command]

HAL:    read_sensors()        -> Observation
        send_commands([Command])
        goal_reached(Goal)    -> bool
```

`core.run(brain, hal, goals)` drives goals to completion. The brain never
references a body; the HAL never references autonomy logic. That separation is
what lets the same brain fly a drone and drive a desk robot.

## Why this shape

- **Sim-to-real:** `SimHAL` is pure Python (runs in ms). `DroneHAL` and
  `GroundRobotHAL` extend it and swap in real transport (MAVLink/ROS 2 via
  `sn360-bridge`, or the Vector SDK). The brain is unchanged.
- **Cheap testbed:** iterate the brain on `GroundRobotHAL` thousands of times
  safely, then bind `DroneHAL`.
- **Pluggable intelligence:** `ReferenceBrain` is a trivial P-controller. Replace
  `perceive` with a VLM and `plan` with an LLM/VLA planner behind the same
  interface — that upgraded brain is the sn360 core.

## Adapters

| HAL | Body | Notes |
|-----|------|-------|
| `SimHAL` | generic | kinematic, no hardware |
| `DroneHAL` | multirotor | binds `sn360-bridge` MAVLink/ROS 2 (TODO) |
| `GroundRobotHAL` | ground robot | z-locked, slow envelope; Vector-class testbed |

## Run the demo

```bash
cd skytrack-oss/robot-brain
python examples/one_brain_two_bodies.py
```

## Scale this up

The interface and a local-model path are open. The hosted large-model brain,
fleet orchestration, and managed evals → **sn360**.
