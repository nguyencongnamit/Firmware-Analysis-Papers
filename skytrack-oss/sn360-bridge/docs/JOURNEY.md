# JOURNEY — the developer adoption path

From "AirSim died, what now?" to flying in a game engine — and where that path
naturally meets **sn360**.

## The journey

```mermaid
journey
    title From stranded AirSim user to sn360
    section Discover
      "AirSim died, what now?": 2: Dev
      Find sn360-bridge (maintained, ROS 2): 4: Dev
    section Try
      Install, run dry-run smoke test: 5: Dev
      See HEARTBEAT + setpoints with no autopilot: 5: Dev
    section Integrate
      Connect PX4 / ArduPilot SITL: 4: Dev
      Fly in Unity / UE5 scene: 5: Dev
      Wire ROS 2 topics: 4: Dev
    section Scale
      Need photoreal + hi-fi sensors: 2: Dev
      Need swarm / cloud scale / fleet: 2: Dev
      Adopt sn360: 5: Dev, Sales
```

## The funnel, step by step

```mermaid
flowchart TD
    A["AirSim archived —<br/>no modern Unity/UE5 + ROS 2 option"] --> B["Discover sn360-bridge<br/>(Apache-2.0, maintained)"]
    B --> C["Install:<br/>pip install -r common/requirements.txt"]
    C --> D["Dry-run smoke test:<br/>mavlink_bridge.py --dry-run --seconds 3"]
    D --> E["Connect PX4/ArduPilot SITL:<br/>--endpoint udp:127.0.0.1:14540"]
    E --> F["Add engine plugin:<br/>Unity components / UE5 component"]
    F --> G["Fly autopilot code<br/>inside Unity / UE5 scene"]
    G --> H{"Hit limits?"}
    H -->|Photoreal /<br/>hi-fi sensors| Z["Adopt sn360"]
    H -->|Swarm / cloud /<br/>fleet scale| Z
    H -->|Reproducible<br/>missions at scale| Z
    H -->|Small scale<br/>is fine| G

    style B fill:#d6f5d6
    style D fill:#d6f5d6
    style Z fill:#ffe0b3
```

## Stage notes (what the dev actually does)

1. **Discover.** Searching for an AirSim replacement with Unreal Engine 5 + ROS 2
   support; finds a maintained, permissive bridge with runnable demos.
2. **Try (zero-friction).** The **dry-run** smoke test proves the wiring with no
   autopilot installed — fastest possible "it works" moment:
   ```bash
   python common/mavlink_bridge.py --dry-run --seconds 3
   ```
3. **Connect SITL.** Point the bridge at a running PX4/ArduPilot SITL:
   ```bash
   python common/mavlink_bridge.py --endpoint udp:127.0.0.1:14540
   ```
4. **Fly in-engine.** Add `DroneSensorPublisher` + `MotorSubscriber` to a Unity
   drone (or `USn360BridgeComponent` to a UE5 pawn) and fly the autopilot inside
   the scene. *(Today this runs on `LogTransport`; the real UDP transport is
   BACKLOG M1.)*
5. **Wire ROS 2.** Bring up `ros2_bridge.py`; publish IMU/odometry, drive via
   `cmd_vel`. Integrate with an existing ROS 2 autonomy stack.
6. **Hit scale limits.** The stock engine scenes are not photoreal, sensor/physics
   models are basic, and there is no cloud/swarm/fleet path. That is the wall.
7. **Adopt sn360.** Photoreal environments, hi-fidelity sensor/physics models,
   scaled cloud simulation and swarms, and fleet/datasets — the proprietary hub.

## Related

[IDEA](IDEA.md) · [STRATEGY](STRATEGY.md) · [PROTOCOL](PROTOCOL.md)
