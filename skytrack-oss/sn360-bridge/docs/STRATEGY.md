# STRATEGY — `sn360-bridge`

## Positioning

> **The maintained AirSim successor** — a modern Unity / Unreal Engine 5 + ROS 2
> bridge to real drone flight stacks.

AirSim is archived and has no modern Unity/UE5 + ROS 2 path. `sn360-bridge` owns
the gap with one sharp claim: *the bridge AirSim users should migrate to.* It is
deliberately a **connector, not a simulator** — small, permissive, easy to adopt,
and the on-ramp to the proprietary **sn360** product.

This is the lead project in [skytrack-oss](../../README.md): biggest painpoint,
biggest audience, highest chance of broad interest — everyone walks through this
funnel first.

## Open-core split: open rim, closed hub

| Open — `sn360-bridge` (Apache-2.0) | Closed — **sn360** (proprietary) |
|------------------------------------|----------------------------------|
| Engine ↔ MAVLink / ROS 2 / PX4–ArduPilot SITL bridge | Photoreal, high-fidelity environments |
| Reference Unity + UE5 sample components/scenes | Scaled cloud simulation & swarms |
| Sensor/clock sync, transport seam, message mapping | Hi-fidelity sensor & physics models |
| ENU↔NED / engine-frame conversions | Cloud "robot brain" |
| Docs, examples, migration guide, CI | Fleet management & curated datasets |

**Principle:** the open bridge is genuinely useful standalone; its *easy mode /
scale mode* lives in sn360. Keep engine core, cloud brain, and hi-fi models out
of this repo entirely.

## Licensing

- **Apache-2.0** across the project (permissive + explicit patent grant →
  maximizes adoption and enterprise comfort).
- Folder carries its own `LICENSE` so it stays correct when split into a
  standalone public repo (`git subtree split`, see the monorepo README).

## Go-to-market

1. **Migration guide from AirSim** — a concrete porting table
   (`getMultirotorState` → sensor frame, `moveByVelocity` → velocity setpoint).
   This is the single highest-leverage adoption asset; it converts a stranded
   user in one sitting. *(planned — BACKLOG M4.)*
2. **ROS 2 community** — meet developers where they are: standard topics
   (`sensor_msgs/Imu`, `nav_msgs/Odometry`, `geometry_msgs/Twist`), REP-103
   frames, micro-ROS/DDS friendliness. Post in ROS Discourse / PX4 / ArduPilot
   forums.
3. **Runnable examples** — the **dry-run** smoke test (works with zero setup) and
   a **PX4 SITL round-trip demo** (arm, takeoff, fly a square) are the proof.
4. **Consistent CTA** — every README/doc ends with an honest "need photoreal /
   scale / fleet? → sn360".

## Success metrics

- **Adoption:** GitHub stars/forks, `pip`/package installs, sample-scene clones.
- **Migration:** number of AirSim projects ported (issues/PRs referencing the
  migration guide).
- **Engagement:** ROS Discourse / PX4 / ArduPilot mentions, community PRs,
  third-party transports/sensors contributed.
- **Funnel:** click-throughs from repo → sn360, and sn360 trials/conversions
  attributable to bridge users (the metric that actually matters).
- **Health:** CI green on Unity package + UE5 plugin headless builds; issue
  response time.

## Related

[IDEA](IDEA.md) · [JOURNEY](JOURNEY.md) · [BACKLOG](BACKLOG.md) ·
[OSS strategy](../../OSS-STRATEGY.md)
