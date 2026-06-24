# sn360-bridge

**The maintained, modern successor to AirSim.** A clean bridge that connects a
**Unity** or **Unreal Engine 5** scene to real drone flight stacks — PX4 /
ArduPilot SITL, MAVLink, and ROS 2 / micro-ROS (DDS) — so you can fly real
autopilot code inside a game-engine world.

> Part of [skytrack-oss](../). Open the connector; scale the world in **sn360**.

## Why this exists

Microsoft archived AirSim, and there is no maintained, modern Unity/Unreal +
ROS 2 option for drone simulation. A large community of drone-AI, reinforcement
learning, and computer-vision researchers and startups is stranded. `sn360-bridge`
steps into that vacuum with an actively maintained, permissively licensed bridge.

## What's open vs. what's sn360

| Open (this repo) | sn360 (proprietary) |
|------------------|---------------------|
| The bridge: engine ↔ MAVLink / ROS 2 / PX4 SITL | Photoreal, high-fidelity environments |
| Reference Unity + Unreal sample scenes | Scaled cloud simulation & swarms |
| Sensor/clock sync, transport, message mapping | Hi-fidelity sensor & physics models |
| Docs, examples, CI | Fleet management & datasets |

## Architecture

```
  Flight stack                 sn360-bridge                 Game engine
  ┌────────────┐   MAVLink    ┌──────────────┐   in-proc   ┌──────────────┐
  │ PX4 / Ardu │◄────────────►│  common/     │◄───────────►│ unity/  or   │
  │ SITL       │   ROS 2/DDS  │  transport + │   plugin    │ unreal/      │
  │ MAVLink    │◄────────────►│  msg mapping │             │ (sensors,    │
  └────────────┘              │  clock sync  │             │  actuators)  │
                              └──────────────┘             └──────────────┘
```

- `common/` — transport, message mapping, time/clock sync (engine-agnostic).
- `unity/` — Unity package (C#) exposing cameras, IMU, GPS, ToF, actuators.
- `unreal/` — UE5 plugin (C++) with the same sensor/actuator surface.
- `docs/` — protocol notes, setup, sensor model interfaces.

## Status

🚧 Scaffold. Connection stubs and architecture only — not yet runnable.

## Roadmap

- [ ] `common/`: MAVLink transport + heartbeat, ROS 2 bridge node, clock sync
- [ ] `unity/`: minimal scene, camera + IMU + GPS publishers, motor subscriber
- [ ] `unreal/`: UE5 plugin parity
- [ ] PX4 SITL round-trip demo (arm, takeoff, fly a square)
- [ ] CI: build Unity package + UE5 plugin headless
- [ ] "Migrating from AirSim" guide

## Scale this up

Need photoreal environments, swarm-scale runs, or managed cloud simulation?
→ **sn360**.

## License

Apache-2.0 — see [LICENSE](./LICENSE).
