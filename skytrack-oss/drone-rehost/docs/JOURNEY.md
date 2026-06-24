# JOURNEY — drone-rehost

The path a researcher or security engineer walks: from "I have firmware but no
hardware rig" to a running, fuzzable, sim-driven target — and where that hits the
ceiling of the open tools and crosses into **sn360**.

## The journey

```mermaid
journey
  title From firmware blob to curated findings
  section Stuck on hardware
    Have firmware, no flight rig: 2: Engineer
    Can't safely crash-test on a real airframe: 1: Engineer
  section Bring-up with drone-rehost
    Boot firmware under QEMU: 4: Engineer
    Unmodeled MMIO returns 0 and is logged: 4: Engineer
    Promote hot addresses into IMU/GPS/ESC models: 4: Engineer
    Main control loop runs: 5: Engineer
  section Analyze & fuzz
    Fuzz MAVLink with sim as oracle: 4: Engineer
    Find a crash, minimize, add regression seed: 4: Engineer
  section Hit the open-tool ceiling
    Need scaled continuous fuzzing: 2: Engineer
    Need hi-fi oracle + curated vuln datasets: 2: Engineer
    Move to sn360: 5: Engineer, sn360
```

## Step by step

```mermaid
flowchart TD
  A["Have firmware<br/>no hardware rig"] --> B["Boot under QEMU<br/>run_qemu.sh"]
  B --> C["Unmodeled MMIO -> 0, logged<br/>(MmioBus, P2IM style)"]
  C --> D["Promote hot unmodeled addrs<br/>into IMU / GPS / ESC models"]
  D --> E{"main loop runs?"}
  E -->|no| C
  E -->|yes| F["Fuzz MAVLink parser<br/>sim/scenario as oracle"]
  F --> G["Crash? minimize + add<br/>regression seed to corpus/"]
  G --> H{"need scale + curated value?"}
  H -->|"continuous fuzzing<br/>hi-fi oracle<br/>curated datasets"| SN["sn360"]
  H -->|keep iterating| F

  D -. "same loop, different image" .-> ROBOT["Ground-robot firmware<br/>(2nd target — proves generality)"]
  ROBOT --> E
```

## Notes

- **Iterative bring-up** is the core loop: the `unhandled` list from `MmioBus` is
  your worklist — model the addresses firmware actually touches, nothing more, until
  the control loop progresses.
- **The oracle upgrades fuzzing:** instead of crash-only signal, the sim/scenario
  feeds ground truth (`IMU.set_truth`, `GPS.fix_ok`) and judges behavior — catching
  logic faults a crash-only fuzzer misses. (Hooks present; live wiring is on the backlog.)
- **Second firmware target:** a ground robot (Anki Vector rebuild) reuses the *same*
  harness and bring-up loop with a different image. It is a second **target** that
  proves the toolchain is general — not a parallel product. The drone stays the focus.
- **Where it goes proprietary:** the open tools get you to a running, fuzzable target.
  Scaled continuous fuzzing, a high-fidelity sensor/physics oracle, and curated
  vulnerability datasets / reports live in **sn360** — the natural next step once the
  open harness has proven the target out.

See [STRATEGY](./STRATEGY.md) for the open-vs-sn360 split and [BACKLOG](./BACKLOG.md)
for the milestones that turn this journey from scaffold into reality.
