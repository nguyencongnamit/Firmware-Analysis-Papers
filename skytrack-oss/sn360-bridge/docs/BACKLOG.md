# BACKLOG — `sn360-bridge`

Prioritized, milestone-grouped task list. **Honest current state: runnable
scaffold.** The MAVLink core works in dry-run and (with `pymavlink`) speaks to a
real endpoint, but it does not yet ingest engine sensor frames. The engine side
is `LogTransport` stubs. The real transport, the SITL round-trip, ROS 2 parity,
the migration guide, and CI are **not built**.

Legend: `[x]` done · `[ ]` todo · `[~]` partial/scaffolded.

## Current state (scaffold)

- [x] `common/mavlink_bridge.py` — pymavlink core, dry-run safe (HEARTBEAT + velocity setpoint)
- [x] `common/ros2_bridge.py` — ROS 2 node skeleton, degrades without `rclpy`
- [x] `common/requirements.txt` — `pymavlink>=2.4`
- [x] `unity/` — `DroneSensorPublisher`, `MotorSubscriber`, `IBridgeTransport`, `LogTransport` (frame math correct)
- [x] `unreal/` — `USn360BridgeComponent` scaffold with cm→m + ENU conversion
- [x] Docs: README, PROTOCOL, IDEA, ARCHITECTURE, FLOW, JOURNEY, STRATEGY, CLAUDE
- [~] Frame conversions present at each edge; not yet exercised end-to-end over the wire

## M1 — Real transport wiring (highest priority)

Goal: replace stubs so the engine and `common/` actually exchange frames.

- [ ] Define the on-the-wire ENU frame format (sensor + command) shared by all transports
- [ ] `common/`: add a transport server/client that ingests engine `SensorFrame`s
      (today `mavlink_bridge.py` only sends a fixed forward setpoint)
- [ ] `common/`: implement explicit ENU↔NED conversion helpers (currently implicit)
- [ ] Unity: implement `UdpTransport : IBridgeTransport` (replace `LogTransport` default)
- [ ] Unreal: define `ISn360Transport` + `UdpTransport`; wire the `// TODO` hooks
      in `PublishSensors()` / `ApplyPendingCommand()`
- [ ] Fill `FSn360SensorFrame.T` and Unity `t` from real world/sim time (clock sync)
- [ ] Smoke test: engine publishes → `common/` receives → logs (no autopilot)

## M2 — PX4 SITL round-trip demo

Goal: the proof demo — arm, takeoff, fly a square inside Unity/UE5.

- [ ] DroneHAL-style sensor ingestion → MAVLink (feed engine pose to PX4)
- [ ] Command path: PX4 setpoints → `common/` → engine body
- [ ] Demo script: connect SITL, arm, takeoff, fly a square, land
- [ ] Minimal Unity scene + minimal UE5 level with the components attached
- [ ] Document the demo in `docs/` with expected output

## M3 — ROS 2 parity

Goal: the ROS 2 path matches the MAVLink path.

- [ ] Implement publishers in `ros2_bridge.py` (`/sn360/imu`, `/sn360/odom`) fed by engine frames
- [ ] Verify `/sn360/cmd_vel` drives the body end-to-end
- [ ] Unity/Unreal `Ros2Transport` (or bridge via `common/`) implementing the seam
- [ ] Confirm REP-103 ENU frames throughout; document QoS choices
- [ ] micro-ROS / DDS notes

## M4 — "Migrating from AirSim" guide

Goal: convert stranded AirSim users in one sitting (top GTM asset).

- [ ] Porting table: `getMultirotorState` → sensor frame, `moveByVelocity` → velocity setpoint, etc.
- [ ] Side-by-side AirSim → sn360-bridge code examples
- [ ] Note feature gaps and the sn360 upgrade path
- [ ] Link prominently from README and PROTOCOL

## M5 — CI

Goal: keep it green and trustworthy.

- [ ] Lint + run `mavlink_bridge.py --dry-run` in CI
- [ ] Build Unity package headless
- [ ] Build UE5 plugin headless
- [ ] (Optional) PX4 SITL integration job for the M2 demo
- [ ] Status badge in README

## Resume pointer

Start at **M1**. See [CLAUDE.md](../CLAUDE.md) for the refresh checklist and
[ARCHITECTURE](ARCHITECTURE.md) / [FLOW](FLOW.md) for the transport-seam and
frame model.
