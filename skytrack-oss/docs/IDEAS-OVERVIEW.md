# Ideas overview — meaning, value, audience

Plain-language summary of every project, and who it's for. Detail lives in each
project's `docs/IDEA.md`.

| Project | What it means (plain) | Value | Audience |
|---------|----------------------|-------|----------|
| **sn360-bridge** | A connector that lets a game engine (Unity/Unreal) talk to real drone flight software (PX4/ArduPilot, MAVLink, ROS 2) — "fly real autopilot code inside a 3D world." | Fills the hole left by **AirSim** (dead/unmaintained). Visual drone sim with no special tooling. The on-ramp everyone installs first. | Drone-AI/robotics researchers, RL & CV teams, drone startups, hobbyists, ex-AirSim users |
| **robot-brain** | A standard robot "brain" — *perceive → plan → act* — written once and run on any body (drone, ground robot, sim) via a swappable hardware layer (HAL). | One brain, many bodies. Iterate AI safely on a cheap robot, then deploy the same brain to the drone (sim-to-real). Rides the LLM/VLA wave. | AI/autonomy engineers, robotics startups, embodied-AI/VLA researchers, makers putting LLMs on robots |
| **drone-rehost** | Run flight-controller **firmware on a normal PC** (in QEMU) with fake sensors, instead of on the real chip — to test, debug, and fuzz it without a flight rig. | Find security bugs and test firmware at PC speed, in parallel, zero crash risk. Makes the firmware-analysis research executable. Credibility flagship. | Security researchers, firmware/embedded engineers, drone red-teams, academics, defense/regulated buyers |
| **scenario-format** | An open file format (+ validator) describing a drone test — mission, wind, sensor failures, GPS-denied zones, swarms, pass/fail rules — portable and replayable. | Reproducible, shareable, version-controlled tests instead of hand-coded one-offs. "Own the format, monetize the runtime." Ecosystem standard. | Sim/QA & test engineers, drone dev teams, CI/CD users, researchers needing reproducible benchmarks |

## Reading the audience spread

- **Widest reach** → `sn360-bridge` (every drone-sim user) and `robot-brain` (the AI crowd).
- **Deepest credibility** → `drone-rehost` (security/firmware experts — smaller but influential).
- **Most strategic lock-in** → `scenario-format` (whoever owns the format shapes the ecosystem).

## Abstract enough to build your own?

Yes. Each project exposes a small seam (`Brain`, `HAL`, `Peripheral`,
`IBridgeTransport`, the scenario schema). A student extends one corner; a
researcher builds a whole product. Apache-2.0 lets third parties ship and sell
what they build. See [`EXTENDING.md`](./EXTENDING.md).

- ✅ Student project / research prototype / paper experiment → **ready today**.
- ⚠️ Commercial product → ready once the in-code TODOs + `skytrack-core` are done.

## Common thread

Each is genuinely useful free and standalone, but has a natural ceiling —
photoreal worlds, a hosted big-model brain, scaled fuzzing, thousands of runs
with analytics — that **sn360** lifts. That ceiling is the funnel.
