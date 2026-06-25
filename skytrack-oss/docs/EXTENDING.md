# Extending SkyTrack OSS — build your own in ~20 lines

The ecosystem is built on small **abstraction seams**. To add your own piece, you
implement one interface and plug in — nothing else changes. Apache-2.0 means you
may ship and even sell what you build.

| You want to add… | Implement | Where | Difficulty |
|------------------|-----------|-------|------------|
| A new **robot body** (drone, rover, Vector) | `HAL` | `robot-brain/core/brain.py` | 🟢 easy |
| A smarter **AI brain** (VLM/LLM/RL) | `Brain` | `robot-brain/core/brain.py` | 🟡 medium |
| A new **sensor/chip** to emulate | `Peripheral` | `drone-rehost/peripherals/base.py` | 🟡 medium |
| A new **transport/protocol** | `IBridgeTransport` | `sn360-bridge/unity/MotorSubscriber.cs` | 🟢 easy |
| A new **test type** (mission/fault/metric) | extend the JSON Schema | `scenario-format/schema/scenario.schema.json` | 🟢 easy |

```
        YOUR PRODUCT / RESEARCH
   ┌───────────────────────────────┐
   │ your Brain  │ your HAL/body    │  ← you write only these
   │ your sensor │ your scenario    │
   └──────┬──────┴────────┬─────────┘
          ▼ plugs into     ▼
   ┌─────────────────────────────────┐
   │ skytrack-oss interfaces + core   │  ← given, free, Apache-2.0
   └─────────────────────────────────┘
```

---

## 1. Your own AI brain — implement `Brain`

Override `perceive / plan / act`. Runnable example:
[`robot-brain/examples/custom_brain_obstacle_avoid.py`](../robot-brain/examples/custom_brain_obstacle_avoid.py).

```python
from core.brain import Brain
from core.reference_brain import ReferenceBrain
from core.types import Command, CommandKind, Plan

class MyBrain(ReferenceBrain):           # reuse the waypoint planner, add behavior
    def plan(self, state, goal):
        base = super().plan(state, goal)
        front = state.notes.get("front_range", 999)
        if front < 3.0:                  # obstacle ahead → dodge sideways
            return Plan([Command(CommandKind.VELOCITY, value=(0, 2.0, 0))], "avoid")
        return base
```

Run it on any body with `core.run(MyBrain(), hal, goals)`.

## 2. Your own robot body — implement `HAL`

Three methods bind the brain to *your* hardware/sim.

```python
from core.brain import HAL
from core.types import Observation

class MyRobotHAL(HAL):
    def read_sensors(self) -> Observation: ...      # your sensors -> Observation
    def send_commands(self, commands): ...          # Command[] -> your actuators
    def goal_reached(self, goal) -> bool: ...        # arrival test
```

The same brain that flies a drone now drives your robot. (See `adapters/` for
`SimHAL`, `DroneHAL`, `GroundRobotHAL` as references.)

## 3. Your own sensor/chip — implement `Peripheral`

For firmware rehosting: answer the MMIO reads/writes your device would.

```python
from peripherals.base import Peripheral

class Lidar(Peripheral):
    def __init__(self): super().__init__("lidar", base=0x4000_7000, size=0x100)
    def read(self, offset, width): ...    # return what firmware should see
    def write(self, offset, value, width): ...
```

Add it to `default_peripherals()` and the `MmioBus` routes to it automatically.

## 4. Your own transport — implement `IBridgeTransport` (C#)

Swap how the engine talks to the bridge (UDP, ROS 2, your middleware).

```csharp
public class MyTransport : IBridgeTransport {
    public void Connect(string endpoint) { ... }
    public void PublishSensors(SensorFrame f) { ... }
    public bool TryGetCommand(out CommandFrame cmd) { ... }
    public void Dispose() { }
}
```

## 5. Your own test type — extend the scenario schema

Add an action, fault, or success criterion to
`scenario-format/schema/scenario.schema.json` (e.g. a new `enum` value), then
`python validator/validate.py examples/` to check it. Bump `scenario_version`
for breaking changes.

---

## Who this is for

- **Students:** pick one 🟢 seam, learn by doing. Start from the obstacle-avoid
  example or `one_brain_two_bodies.py`.
- **Drone/robot researchers:** write your algorithm as a `Brain`, test it across
  many `scenario-format` files, run through `sn360-bridge`. Focus on your
  contribution; the plumbing is given.
- **Product builders:** prototype today; for production, finish the in-code TODOs
  (real MAVLink transport, QEMU MMIO hook, scenario player) — tracked in each
  `docs/BACKLOG.md`.

## Honest status

These are **runnable scaffolds**, not a finished SDK. Ready for student projects,
research prototypes, and paper experiments today; a shipping commercial product
also needs the wiring TODOs and `skytrack-core` done.
