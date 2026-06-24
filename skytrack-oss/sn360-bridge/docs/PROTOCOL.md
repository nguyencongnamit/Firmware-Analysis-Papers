# sn360-bridge protocol & setup

## Data flow

```
flight stack  <--MAVLink/ROS2-->  common/  <--local socket-->  engine plugin
(PX4/ArduPilot)                  (transport,                   (Unity / UE5:
                                  msg mapping,                   sensors out,
                                  clock sync)                    motors in)
```

## Frames & units

| Layer | Frame | Units |
|-------|-------|-------|
| Bridge canonical | **ENU** (x=East, y=North, z=Up) | meters, m/s, rad |
| MAVLink | NED | converted in `common/` |
| Unity | Y-up left-handed | converted in the C# plugin |
| Unreal | Z-up left-handed, cm | converted in the C++ plugin |

All conversions happen at the edges; everything in `common/` is ENU meters.

## Quick start (PX4 SITL, dry-run safe)

```bash
cd common
pip install -r requirements.txt
# No autopilot yet? Prove the wiring with dry-run:
python mavlink_bridge.py --dry-run --seconds 3
# With PX4 SITL running:
python mavlink_bridge.py --endpoint udp:127.0.0.1:14540
```

## ROS 2 path

```bash
python common/ros2_bridge.py     # pub /sn360/imu,/sn360/odom  sub /sn360/cmd_vel
```

## Engine side

- **Unity:** add `DroneSensorPublisher` + `MotorSubscriber` to the drone
  GameObject. Default `LogTransport` prints frames; swap for a UDP/ROS 2
  transport implementing `IBridgeTransport`.
- **Unreal:** add `USn360BridgeComponent` to the pawn; set `Endpoint`.

## Migrating from AirSim

AirSim's `getMultirotorState` / `moveByVelocity` map to the bridge's sensor
frame / velocity setpoint. A porting table lives in this folder as the project
matures.

## Scale this up

Photoreal environments, swarm-scale runs, managed cloud sim → **sn360**.
