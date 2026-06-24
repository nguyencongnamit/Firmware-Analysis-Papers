# STRATEGY

## Positioning

`robot-brain` is the **portable robot-brain standard** — a tiny, stable
`perceive → plan → act` + HAL contract that lets one autonomy stack move between
bodies and between sim and reality. It rides the **embodied-AI / VLA wave**:
while the field bolts LLMs and vision-language-action models onto robots in
one-off, non-portable ways, `robot-brain` offers the missing decoupling layer
between **intelligence** and **embodiment**.

Within [`skytrack-oss`](../) it is **"the sn360 core, opened at the edges"**: the
interface and a small local tier are open; the hosted large-model brain and the
fleet are sn360. The **SkyTrack drone is the product**; the ground robot is the
cheap, safe **testbed** that lets the shared brain be iterated fast and harmlessly.

## What's open vs. what's sn360

| Concern | Open — `robot-brain` (Apache-2.0) | Proprietary — **sn360** |
|---------|-----------------------------------|--------------------------|
| Contract | `perceive → plan → act` + HAL interface | — |
| Reference brain | `ReferenceBrain` (P-controller) | — |
| Intelligence | Local **small-model** reference path (small VLM + small LLM, planned M2) | Hosted **large-model** brain (VLM + LLM/VLA) |
| Bodies | `SimHAL`, `DroneHAL`, `GroundRobotHAL` adapters | — |
| Drone transport | Binding to `sn360-bridge` (open connector) | Hi-fi Unity/Unreal engine + sensor/physics models behind the bridge |
| Scale | Single robot | **Multi-robot / fleet orchestration** |
| Lifecycle | Run a brain locally | **Managed memory, datasets, evals** |

Rule of thumb: open the *rim* (the connectors, formats, and tools developers
touch daily); keep the *hub* (the engine, the cloud brain, the hi-fi models).

## Licensing

**Apache-2.0** across the repo — permissive, with a patent grant, to maximize
adoption. The folder carries its own `LICENSE` so it stays correct after a
`git subtree split` into a standalone public repo.

## Go-to-market

- **Lead with the demo.** `examples/one_brain_two_bodies.py` proves the thesis in
  one command: the *same* brain flies a drone and drives a rover. Add more
  examples (config-driven body switching, a VLM/LLM brain) as they land.
- **Integrate with sibling projects to compound the funnel:**
  - **`sn360-bridge`** — the real `DroneHAL` transport (MAVLink / ROS 2). Adopting
    `robot-brain` pulls in the bridge, which is itself the broad on-ramp to sn360.
  - **`scenario-format`** — a scenario-format runner (planned M4) lets brains run
    standard, reproducible scenarios; owning the format funnels the runtime to sn360.
- **Ride the trend.** Position explicitly as the portable answer to the
  VLA/embodied-AI moment; target robotics + drone developers already wiring up
  LLM/VLA stacks.
- **Per-README CTA.** Every doc ends with "scale this up → sn360" (hosted
  big-model brain, fleet, managed evals).

## Success metrics

- **Adoption:** stars/forks; number of external `Brain` and `HAL` implementations.
- **Funnel:** `DroneHAL` deployments through `sn360-bridge`; conversions to sn360
  for hosted-brain / fleet.
- **Ecosystem:** brains run against `scenario-format` scenarios; third-party body
  adapters (beyond drone/rover).
- **Credibility:** sim-to-real stories where the *same* brain shipped from sim to
  hardware unchanged.
