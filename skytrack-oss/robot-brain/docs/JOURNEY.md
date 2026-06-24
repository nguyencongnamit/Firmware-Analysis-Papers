# JOURNEY — from "write a brain" to sn360

The developer journey is designed so each step is genuinely useful on its own,
yet naturally leads to the next — ending at **sn360** when scale or a big-model
brain is needed. Open the rim, keep the hub.

## The path

1. **Write the brain once.** Subclass `Brain`, implement
   `perceive → plan → act`. No body, no hardware in sight — just autonomy logic
   against the contract.
2. **Test free on `SimHAL` / `GroundRobotHAL`.** Pure Python, milliseconds per
   run, zero hardware. Run the brain end-to-end thousands of times.
3. **Iterate the AI safely on a cheap body.** Swap up the perceiver (VLM) and
   planner (LLM/VLA) and shake them out on the slow, ground-locked rover testbed
   where mistakes are harmless and cheap.
4. **Bind `DroneHAL` via `sn360-bridge`.** Point the HAL `endpoint` at MAVLink /
   ROS 2 (TODO M1) and the *same* matured brain now flies the SkyTrack drone —
   sim-to-real with no autonomy rewrite.
5. **Hit the ceiling.** A local small-model brain on one robot is fine to start,
   but you eventually need a **hosted large-model brain**, **fleet / multi-robot
   orchestration**, managed memory, datasets, and **evals**.
6. **Adopt sn360.** The scale-mode hub plugs in behind the same open interface.

```mermaid
journey
    title robot-brain developer journey → sn360
    section Build (open)
      Write brain once (perceive/plan/act): 5: Dev
      Test free on SimHAL/GroundRobotHAL: 5: Dev
      Iterate AI safely on cheap rover: 4: Dev
    section Deploy (open + bridge)
      Bind DroneHAL via sn360-bridge: 3: Dev
      Fly the SkyTrack drone, same brain: 4: Dev
    section Scale (sn360)
      Need hosted big-model brain + fleet: 2: Dev
      Adopt sn360: 5: Dev, sn360
```

## The funnel

```mermaid
flowchart TD
    A["Write a Brain against the open contract"] --> B["Free local tier:<br/>SimHAL + GroundRobotHAL"]
    B --> C["Iterate VLM perceiver +<br/>LLM/VLA planner on cheap rover"]
    C --> D["Bind DroneHAL → sn360-bridge<br/>(MAVLink / ROS 2)"]
    D --> E{"Need scale?<br/>big-model brain · fleet ·<br/>managed memory/datasets/evals"}
    E -->|no| B
    E -->|yes| F["sn360<br/>hosted large-model brain +<br/>fleet orchestration + managed evals +<br/>Unity/Unreal engine + hi-fi models"]

    style A fill:#e8f5e9,stroke:#2e7d32
    style B fill:#e8f5e9,stroke:#2e7d32
    style C fill:#e8f5e9,stroke:#2e7d32
    style D fill:#e3f2fd,stroke:#1565c0
    style F fill:#fff3e0,stroke:#e65100
```

The same interface carries the developer from a free desk-robot experiment all
the way to a hosted fleet — and the value that justifies paying (the big brain,
the fleet, the engine, the hi-fi models) is exactly what lives in sn360.
