# SkyTrack OSS Ecosystem

How the open projects form **one ecosystem** for every audience in the SkyTrack
world — and how each piece relates to, feeds, and reinforces the others. The goal:
anyone (student, drone/robot researcher, startup) can **build their own product
without permission**, and every open path has a natural ceiling that **sn360**
lifts.

> Diagrams here are ASCII on purpose (portable, render-free). Per-project
> `docs/ARCHITECTURE.md` files carry the detailed views.

## Layers, not just projects

```
  ┌──────────────────────────────────────────────────────────────────────┐
  │  COMMUNITY LAYER   docs site · examples gallery · tutorials · RFCs ·   │
  │                    Discord/forum · firmware-papers awareness hub       │
  ├──────────────────────────────────────────────────────────────────────┤
  │  PILLARS (the 4)   sn360-bridge   robot-brain   drone-rehost  scenario │
  │                    (connect)      (intelligence)(security)    -format  │
  │                                                               (tests)  │
  ├──────────────────────────────────────────────────────────────────────┤
  │  INTERCHANGE       scenario spec · telemetry/log format · model API ·  │
  │  STANDARDS         brain↔HAL contract · result/report schema           │
  ├──────────────────────────────────────────────────────────────────────┤
  │  SHARED CORE       skytrack-core: ENU frame, message types, units,     │
  │                    MAVLink/ROS2 helpers   (used by ALL pillars)        │
  ├──────────────────────────────────────────────────────────────────────┤
  │  ASSETS / DATA     datasets · benchmarks+leaderboard · model zoo ·     │
  │                    scenario library · drone/ground-robot body packs    │
  └──────────────────────────────────────────────────────────────────────┘
                    every layer ─────────────▶  sn360 (paid hub)
```

**Keystone:** `skytrack-core` (not yet built) is what turns *four loose repos*
into *one ecosystem* — the shared ENU frame, message types, units, and
MAVLink/ROS 2 helpers currently duplicated across the pillars. **Build it first.**

## How the pieces relate (who builds on / feeds whom)

```
                          ┌───────────────────────────┐
                          │       skytrack-core       │ ◀── everything builds on this
                          │  ENU frame · message types │
                          └─────┬─────┬─────┬─────┬─────┘
              ┌─────────────────┘     │     │     └─────────────────┐
              ▼                       ▼     ▼                       ▼
     ┌─────────────────┐   ┌──────────────────┐   ┌──────────────┐   ┌──────────────┐
     │ scenario-format │   │   robot-brain    │   │ sn360-bridge │   │ drone-rehost │
     └────────┬────────┘   └─────────┬────────┘   └──────┬───────┘   └──────┬───────┘
              │ feeds missions/faults │ sends commands    │ MAVLink         │ SITL
              └──────────────────────▶  ◀────binds HAL────┘ ◀───────────────┘
                       robot-brain drives bridge; rehost can stand in
                       for real firmware behind the bridge
```

## The flywheel (each turn raises the others)

```
   scenario-format ─more tests─▶ datasets/benchmarks ─train─▶ model zoo
        ▲                              │ leaderboard ranks        │
        │                              ▼                          │ better brains
        └────────── harder tests ◀──── robot-brain ◀──────────────┘
   drone-rehost ─bugs─▶ crash corpus ─hardens─▶ the whole stack
```

## Every audience has a door

| Audience | Enters through | Glue that keeps them | → sn360 when… |
|----------|---------------|----------------------|----------------|
| Drone-sim / RL / CV researchers | sn360-bridge | examples gallery, datasets, leaderboard | need photoreal + cloud scale |
| AI / autonomy / embodied-AI | robot-brain | model zoo, brain↔HAL contract | need hosted big brain + fleet |
| Security / firmware / defense | drone-rehost + papers hub | SBOM/compliance, crash corpus | need scaled fuzzing + findings |
| Test / QA / CI engineers | scenario-format | scenario library, report schema, CI action | need 1000s of runs + analytics |
| Students / educators / newcomers | tutorials + papers hub | guided examples, EXTENDING guide | grow into power users |
| Hardware makers / Vector fans | body packs | shared core + bridge | want polished sim/brain |
| ML / data scientists | datasets + leaderboard | benchmarks, model zoo | need data generation at scale |
| Enterprise / regulated buyers | SBOM / compliance CLI | security track, papers-hub credibility | procurement (NDAA/Blue UAS, EU) |

## Build-your-own (the abstraction promise)

Outsiders extend the ecosystem through small, documented seams — see
[`docs/EXTENDING.md`](./docs/EXTENDING.md):

```
        YOUR PRODUCT / RESEARCH
   ┌───────────────────────────────┐
   │ your Brain  │ your HAL/body    │   ← you write only these
   │ your sensor │ your scenario    │
   └──────┬──────┴────────┬─────────┘
          │ plugs into     │
   ┌──────▼────────────────▼─────────┐
   │  skytrack-oss interfaces +       │   ← given, free, Apache-2.0
   │  skytrack-core (frame/transport) │
   └──────────────────────────────────┘
```

Apache-2.0 means third parties may build **and commercialize** their own products
on top. That "build without permission" property is the ecosystem's core value.

## Governance & the open/paid line

- **One brand, shared conventions:** ENU frame, Apache-2.0, a "scale → sn360" CTA
  in every README.
- **Open standards, RFC-governed:** the scenario format, telemetry format, and
  brain↔HAL contract evolve in the open (a `SkyEP` proposal process).
- **Hard open/paid boundary:** never open the engine, hosted brain, hi-fi models,
  or fleet. If the ceiling isn't real, the funnel breaks.

## Rollout (don't build it all at once)

1. **Now:** extract `skytrack-core`; stand up examples gallery + a docs landing page.
2. **Next:** scenario library + benchmark/leaderboard; one `CONTRIBUTING` + RFC process.
3. **Later:** body packs, model zoo, SBOM/compliance, education tracks.

See [`BACKLOG.md`](./BACKLOG.md) for the tracked tasks.
