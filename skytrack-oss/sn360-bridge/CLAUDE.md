# CLAUDE.md — session memory for `sn360-bridge`

> Read this first. It exists so a fresh AI/dev session can resume in minutes
> without re-deriving context. If something here is stale, fix it.

## Project summary (one paragraph)

`sn360-bridge` is the maintained, modern successor to Microsoft AirSim: a clean
bridge that connects a **Unity** or **Unreal Engine 5** scene to real drone
flight stacks — **PX4 / ArduPilot SITL, MAVLink, and ROS 2 / micro-ROS (DDS)** —
so real autopilot code can fly inside a game-engine world. It is the open
adoption on-ramp for the proprietary **sn360** product (photoreal environments,
cloud "robot brain", hi-fidelity models, swarm/fleet scale). The canonical
internal frame is **ENU meters**; all frame/unit conversions happen at the edges
(MAVLink NED, Unity Y-up, Unreal Z-up cm). License: **Apache-2.0**.

## Current status — honest

**Runnable scaffold, not a finished bridge.** What actually works today:

- `common/mavlink_bridge.py` runs end-to-end in **dry-run** (no autopilot
  needed). With a real endpoint it uses `pymavlink` to send HEARTBEAT and
  `SET_POSITION_TARGET_LOCAL_NED` velocity setpoints.
- `common/ros2_bridge.py` is a ROS 2 node **skeleton**; it degrades gracefully
  and prints its topic shape when `rclpy` is absent.
- Unity (`DroneSensorPublisher.cs`, `MotorSubscriber.cs`) and Unreal
  (`Sn360Bridge.h/.cpp`) compile-time scaffolds with the correct frame math.

**Key TODOs (not yet wired):**

- No `DroneHAL` / sensor-side abstraction yet; the MAVLink core only sends a
  fixed forward-velocity demo and does not yet ingest engine sensor frames or
  expose a transport server for the engine to connect to.
- Engine transport is a **`LogTransport` stub** only — it prints frames. The
  real UDP/ROS 2 transport implementing `IBridgeTransport` (Unity) /
  `ISn360Transport` (Unreal) is **not built**. Unreal's
  `PublishSensors`/`ApplyPendingCommand` have explicit `// TODO` transport hooks.
- No PX4 SITL round-trip demo, no CI, no AirSim migration table yet.

## Key files map

| Path | What it does |
|------|--------------|
| `README.md` | Public pitch, open-vs-sn360 split, roadmap |
| `docs/PROTOCOL.md` | Data flow, frames/units table, quick start |
| `docs/IDEA.md` | Vision, painpoint, funnel to sn360 |
| `docs/ARCHITECTURE.md` | Components, frame design, transport seam |
| `docs/FLOW.md` | Runtime/data flow, tick loop, conversion paths |
| `docs/JOURNEY.md` | Developer adoption journey → sn360 |
| `docs/STRATEGY.md` | Positioning, open-core split, GTM, metrics |
| `docs/BACKLOG.md` | Prioritized milestone task list (resume here) |
| `common/mavlink_bridge.py` | pymavlink core; HEARTBEAT + velocity setpoint; dry-run safe |
| `common/ros2_bridge.py` | ROS 2 node skeleton (pub imu/odom, sub cmd_vel) |
| `common/requirements.txt` | `pymavlink>=2.4` (rclpy comes from a ROS 2 distro) |
| `unity/DroneSensorPublisher.cs` | Samples Rigidbody pose/vel each FixedUpdate, ENU-converts, publishes |
| `unity/MotorSubscriber.cs` | `SensorFrame`/`CommandFrame`/`IBridgeTransport` + `LogTransport`; applies velocity setpoints |
| `unreal/Sn360Bridge.h` | `USn360BridgeComponent` + `FSn360SensorFrame` |
| `unreal/Sn360Bridge.cpp` | UE5 tick loop; cm→m + ENU conversion; transport TODOs |

## How to run / try it

Dry-run smoke test (no autopilot, no ROS 2 — always works):

```bash
python common/mavlink_bridge.py --dry-run --seconds 3
```

With PX4/ArduPilot SITL running:

```bash
pip install -r common/requirements.txt
python common/mavlink_bridge.py --endpoint udp:127.0.0.1:14540
```

ROS 2 path (prints topic shape if `rclpy` missing):

```bash
python common/ros2_bridge.py
```

## Conventions

- **Canonical frame: ENU meters** (x=East, y=North, z=Up), m/s, rad. Everything
  in `common/` is ENU. Convert **only at the edges**:
  - MAVLink ↔ NED (in `common/`)
  - Unity ↔ Y-up left-handed (in C#: `py=p.z, pz=p.y`)
  - Unreal ↔ Z-up left-handed cm (in C++: divide by 100, map axes)
- **Transport seam:** `IBridgeTransport` (Unity) / `ISn360Transport` (Unreal)
  isolate the wire protocol so UDP/ROS 2 swap in without touching gameplay code.
- **License:** Apache-2.0 across the repo.
- **Funnel:** every doc keeps an honest "scale this up → sn360" CTA. Keep
  proprietary value (engine, cloud brain, hi-fi models) out of this repo.

## Where to resume / next actions

Open **`docs/BACKLOG.md`** and start at **M1** (wire real MAVLink transport in
`common/` + UDP transport for Unity/Unreal). That is the single highest-leverage
gap between "scaffold" and "real bridge".

## Refresh checklist before starting or clearing a session

- [ ] Re-read this `CLAUDE.md`, then `README.md`, then `docs/BACKLOG.md`.
- [ ] Check git: `git status` and confirm branch `claude/skytrack-oss-ideas-0ivndv`.
- [ ] Run the dry-run smoke test: `python common/mavlink_bridge.py --dry-run --seconds 3`
      (expect HEARTBEAT + SET_POSITION_TARGET_LOCAL_NED lines).
- [ ] Skim `docs/ARCHITECTURE.md` and `docs/FLOW.md` for the frame/transport model.

## Related docs

- [IDEA](docs/IDEA.md) · [ARCHITECTURE](docs/ARCHITECTURE.md) ·
  [FLOW](docs/FLOW.md) · [JOURNEY](docs/JOURNEY.md) ·
  [STRATEGY](docs/STRATEGY.md) · [BACKLOG](docs/BACKLOG.md) ·
  [PROTOCOL](docs/PROTOCOL.md)
- Monorepo framing: [`../README.md`](../README.md), [`../OSS-STRATEGY.md`](../OSS-STRATEGY.md)
