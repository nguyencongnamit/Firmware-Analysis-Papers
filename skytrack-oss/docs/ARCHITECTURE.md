# Platform architecture — skytrack-oss × sn360

How the four open projects fit together and where the proprietary **sn360** hub
takes over. This is the bird's-eye view; each project's own
`docs/ARCHITECTURE.md` has the detail.

## The open rim and the closed hub

```mermaid
flowchart TB
    subgraph OPEN["Open rim (Apache-2.0, this monorepo)"]
        SF["scenario-format<br/>portable test scenarios"]
        RB["robot-brain<br/>perceive → plan → act + HAL"]
        BR["sn360-bridge<br/>engine ↔ MAVLink/ROS 2"]
        DR["drone-rehost<br/>firmware emulation + fuzzer"]
    end
    subgraph HUB["Closed hub — sn360 (proprietary)"]
        ENG["Unity/Unreal engine<br/>photoreal worlds"]
        BRAIN["hosted large-model brain<br/>fleet + evals"]
        MODELS["hi-fidelity sensor/physics models"]
        CLOUD["scaled cloud simulation"]
    end

    SF --> RB --> BR --> ENG
    DR -. SITL firmware target .-> BR
    BR --> CLOUD
    RB --> BRAIN
    SF --> CLOUD
    DR --> MODELS
    ENG --> MODELS

    classDef open fill:#e6f4ff,stroke:#0366d6;
    classDef hub fill:#fff0e6,stroke:#d9480f;
    class SF,RB,BR,DR open;
    class ENG,BRAIN,MODELS,CLOUD hub;
```

## End-to-end data flow (a scenario run)

```mermaid
sequenceDiagram
    participant SF as scenario-format
    participant RB as robot-brain
    participant BR as sn360-bridge
    participant ENG as Engine (Unity/Unreal)
    participant FW as drone-rehost (optional SITL firmware)

    SF->>RB: load scenario (mission, faults, criteria)
    loop control loop
        ENG->>BR: sensor frame (ENU)
        BR->>RB: Observation
        RB->>RB: perceive → plan → act
        RB->>BR: Command (velocity/goto)
        BR->>ENG: actuator setpoint (engine frame)
        opt firmware-in-the-loop
            BR->>FW: MAVLink
            FW->>BR: parsed control output
        end
    end
    RB->>SF: evaluate success_criteria → pass/fail
```

## One platform, two bodies

```mermaid
flowchart LR
    BRAIN["robot-brain<br/>(one brain)"]
    BRAIN --> DH["DroneHAL"] --> DRONE["SkyTrack drone<br/>(product focus)"]
    BRAIN --> GH["GroundRobotHAL"] --> ROVER["ground robot<br/>(Vector testbed/demo)"]
    DRONE --> SN[(sn360)]
    ROVER --> SN
```

The same brain, sim, and firmware toolchain serve both bodies. The drone is the
product; the ground robot is the cheap, safe testbed and the "look, it
generalizes" demo.

## Shared conventions

- **Canonical frame:** ENU meters; edges convert (MAVLink NED, Unity Y-up,
  Unreal Z-up/cm).
- **Transport:** MAVLink (pymavlink) and ROS 2 / DDS, centralized in
  `sn360-bridge/common`.
- **Funnel:** each project is useful alone; scale/fidelity/fleet → sn360.
