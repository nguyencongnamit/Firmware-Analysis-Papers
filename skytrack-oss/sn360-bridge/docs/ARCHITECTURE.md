# ARCHITECTURE — `sn360-bridge`

Three layers, one canonical frame, one swappable transport seam.

## Components

```mermaid
graph LR
    subgraph FS["Flight stack (external)"]
        PX4["PX4 / ArduPilot SITL"]
        ROS["ROS 2 graph / DDS"]
    end

    subgraph COMMON["common/ (engine-agnostic, Python)"]
        MAV["mavlink_bridge.py<br/>pymavlink: heartbeat,<br/>velocity setpoints"]
        R2["ros2_bridge.py<br/>pub imu/odom,<br/>sub cmd_vel"]
        CONV["frame + unit conversion<br/>(ENU ↔ NED, time/clock)"]
    end

    subgraph ENGINE["Engine plugin"]
        UNITY["unity/ (C#)<br/>DroneSensorPublisher<br/>MotorSubscriber"]
        UNREAL["unreal/ (C++)<br/>USn360BridgeComponent"]
        SEAM["IBridgeTransport /<br/>ISn360Transport seam<br/>(LogTransport today)"]
    end

    PX4 <-->|MAVLink UDP| MAV
    ROS <-->|DDS topics| R2
    MAV --- CONV
    R2 --- CONV
    CONV <-->|local socket / in-proc<br/>(planned UDP)| SEAM
    SEAM --- UNITY
    SEAM --- UNREAL

    style COMMON fill:#eef
    style ENGINE fill:#efe
```

## Responsibilities

### Flight stack (external, not in this repo)
PX4 or ArduPilot **SITL**, speaking MAVLink and/or a ROS 2 graph. The bridge is a
client of these; it does not host them.

### `common/` — engine-agnostic core (Python)
- `mavlink_bridge.py` — `MavlinkBridge` class: connect, send HEARTBEAT (1 Hz),
  send `SET_POSITION_TARGET_LOCAL_NED` velocity setpoints. `--dry-run` logs
  frames with no autopilot present (degrades when `pymavlink` is missing).
- `ros2_bridge.py` — `Sn360BridgeNode` skeleton: publishes
  `/sn360/imu` (`sensor_msgs/Imu`) and `/sn360/odom` (`nav_msgs/Odometry`),
  subscribes `/sn360/cmd_vel` (`geometry_msgs/Twist`). Degrades when `rclpy` is
  absent (prints shape only).
- **Owns all frame/unit conversion** between the canonical ENU representation and
  MAVLink NED, plus time/clock sync. Everything inside `common/` is ENU meters.

### Engine plugin — per-engine, matching surface
- **Unity (C#):** `DroneSensorPublisher` samples Rigidbody pose/velocity each
  `FixedUpdate`, converts Unity Y-up → ENU, and publishes a `SensorFrame`.
  `MotorSubscriber` polls for a `CommandFrame` and applies the ENU velocity
  setpoint back to the Rigidbody.
- **Unreal (C++):** `USn360BridgeComponent` does the same on `TickComponent`,
  converting UE5 cm / Z-up left-handed → ENU meters.

> **Status:** the engine side currently uses **`LogTransport`** (prints frames).
> The real UDP/ROS 2 transport is planned — see [BACKLOG](BACKLOG.md) M1.

## Frame-conversion design

**One canonical frame, conversions at the edges.** The core never reasons about
engine handedness or MAVLink NED — each edge owns its own conversion, so a new
engine or middleware only adds one adapter.

| Layer | Frame | Units | Conversion lives in |
|-------|-------|-------|---------------------|
| **Bridge canonical** | **ENU** (x=East, y=North, z=Up) | meters, m/s, rad | — (everything here) |
| MAVLink | NED (x=North, y=East, z=Down) | converted to/from ENU | `common/` |
| ROS 2 | ENU (REP-103 aligns) | meters, m/s, rad | `common/ros2_bridge.py` |
| Unity | Y-up, left-handed | meters | `unity/*.cs` (`py=p.z, pz=p.y`) |
| Unreal | Z-up, left-handed | **cm** | `unreal/*.cpp` (÷100, axis map) |

## The transport seam (`IBridgeTransport` / `ISn360Transport`)

The wire protocol is isolated behind an interface so gameplay/sim code never
changes when the transport does.

Unity interface (`unity/MotorSubscriber.cs`):

```csharp
public interface IBridgeTransport : IDisposable
{
    void Connect(string endpoint);
    void PublishSensors(SensorFrame frame);
    bool TryGetCommand(out CommandFrame cmd);
}
```

- `LogTransport` — default no-network implementation; prints frames for first
  bring-up. **(current state)**
- `UdpTransport` — planned: framed ENU messages to `common/`. **(M1)**
- `Ros2Transport` — planned: publish/subscribe directly on the ROS 2 graph.

Unreal mirrors this with `ISn360Transport`; `USn360BridgeComponent` has explicit
`// TODO` hooks in `PublishSensors()` / `ApplyPendingCommand()` where the
transport plugs in.

## Related

[FLOW](FLOW.md) · [PROTOCOL](PROTOCOL.md) · [BACKLOG](BACKLOG.md)
