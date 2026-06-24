# Adoption journey — from open tools to sn360

How a developer travels from "I found one of these on GitHub" to an sn360
customer. The funnel is intentional: each open project solves a real problem
standalone, and each has a natural ceiling that sn360 lifts.

## The funnel

```mermaid
journey
    title Developer journey into the sn360 funnel
    section Discover
      Hits an open project (AirSim is dead / needs a robot brain): 4: Dev
      Runs the smoke test in minutes: 5: Dev
    section Adopt (open)
      Builds something real for free: 5: Dev
      Tells colleagues / cites it: 4: Dev
    section Hit the ceiling
      Needs photoreal worlds / scale / fleet / hi-fi models: 2: Dev
    section Convert
      Adopts sn360 for the hard part: 5: Dev, Company
```

## Entry points → ceiling → sn360

```mermaid
flowchart TD
    A1["AirSim died — need a sim bridge"] --> BR[sn360-bridge]
    A2["Bolting LLMs onto robots ad-hoc"] --> RB[robot-brain]
    A3["Can't fuzz firmware without a rig"] --> DR[drone-rehost]
    A4["No portable, reproducible scenarios"] --> SF[scenario-format]

    BR --> C1{"Need photoreal<br/>worlds + swarm scale?"}
    RB --> C2{"Need hosted big-model<br/>brain + fleet?"}
    DR --> C3{"Need scaled fuzzing<br/>+ hi-fi oracle?"}
    SF --> C4{"Need thousands of runs<br/>at fidelity + analytics?"}

    C1 -->|yes| SN[(sn360)]
    C2 -->|yes| SN
    C3 -->|yes| SN
    C4 -->|yes| SN
    C1 -->|no| BR
    C2 -->|no| RB
    C3 -->|no| DR
    C4 -->|no| SF
```

## Why each ceiling is real (not artificial)

| Project | Free is genuinely useful for… | The wall you eventually hit |
|---------|------------------------------|------------------------------|
| `sn360-bridge` | connecting PX4/ROS 2 to a game engine | photoreal assets, swarm/cloud scale |
| `robot-brain` | portable autonomy, sim-to-real, local models | hosted large-model brain, fleet, evals |
| `drone-rehost` | rehosting + fuzzing on a laptop | continuous scaled fuzzing, hi-fi oracle, curated findings |
| `scenario-format` | authoring/sharing/validating scenarios | running thousands at fidelity + analytics |

## Cross-sell path

A developer who enters through one project meets the others (shared frame,
shared docs, the "same brain, two bodies" demo), widening the surface that leads
to sn360.
