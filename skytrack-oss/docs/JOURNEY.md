# Adoption journey — from open tools to sn360

How a developer travels from "I found one of these on GitHub" to an sn360
customer. Each open project solves a real problem standalone and has a natural
ceiling sn360 lifts. ASCII (no renderer).

## The funnel

```
   DISCOVER            ADOPT (open)         HIT THE CEILING         CONVERT
   ─────────           ────────────         ───────────────         ───────
   finds a project ─▶  runs smoke test ─▶   builds something ─▶  needs photoreal /
   (AirSim is dead /   in minutes           real for free        scale / fleet /
    needs a brain /                         tells colleagues     hi-fi / analytics
    can't fuzz fw)                          cites it                   │
                                                                       ▼
                                                                  adopts sn360
```

## Entry points → ceiling → sn360

```
   "AirSim died"               ─▶ sn360-bridge ─┐ need photoreal + swarm scale ─┐
   "LLM on a robot, ad-hoc"    ─▶ robot-brain  ─┤ need hosted big brain + fleet ─┤
   "can't fuzz firmware"       ─▶ drone-rehost ─┤ need scaled fuzzing + oracle  ─┼─▶ [ sn360 ]
   "no reproducible tests"     ─▶ scenario-fmt ─┤ need 1000s runs + analytics   ─┤
   "need training data"        ─▶ datasets     ─┤ need data gen at scale        ─┤
   "procurement/compliance"    ─▶ SBOM CLI     ─┘ need certified reports        ─┘
```

## Why each ceiling is real (not artificial)

| Project | Free is genuinely useful for… | The wall you eventually hit |
|---------|------------------------------|------------------------------|
| sn360-bridge | connecting PX4/ROS 2 to a game engine | photoreal assets, swarm/cloud scale |
| robot-brain | portable autonomy, sim-to-real, local models | hosted large-model brain, fleet, evals |
| drone-rehost | rehosting + fuzzing on a laptop | continuous scaled fuzzing, hi-fi oracle, curated findings |
| scenario-format | authoring/sharing/validating scenarios | thousands of runs at fidelity + analytics |

## The student / researcher path (build-without-permission)

```
   learn one seam ──▶ extend a corner ──▶ prototype a product ──▶ publish / ship
   (Brain/HAL/        (obstacle-avoid     (Apache-2.0 lets       (some grow into
    Peripheral/        example, custom     you commercialize)     sn360 customers)
    scenario)          sensor, new test)
```

## Cross-sell path

A developer who enters through one project meets the others — shared `skytrack-core`
conventions, the examples gallery, the "same brain, two bodies" demo — widening
the surface that eventually leads to sn360.
