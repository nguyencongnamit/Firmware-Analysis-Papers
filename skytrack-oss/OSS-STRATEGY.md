# SkyTrack OSS Strategy

## Thesis

SkyTrack sits at a rare intersection: **drone autonomy/simulation × embedded
firmware security × robot AI**. Almost no one owns that intersection in open
source. The strategy is **open-core with an "open rim, closed hub" funnel**:

- **Open (the rim):** the connectors, formats, and tools developers reach for
  daily. These earn trust, citations, and adoption.
- **Closed (the hub / sn360):** the Unity/Unreal engine, the cloud "robot
  brain," high-fidelity sensor/physics models, fleet management, and scaled
  simulation.

Every open project is useful standalone, but its *easy mode / scale mode* lives
in sn360.

## Goals (in priority order)

1. **Show strength & usefulness** — ship things the community genuinely needs.
2. **Drive adoption back to sn360** — each project has an explicit "scale this
   up → sn360" path.
3. **Build credibility** — especially in firmware/embedded security, where the
   research depth is real and differentiated.

## Market painpoint ranking

| Idea | Painpoint severity | Chance of big interest | Why |
|------|-------------------|----------------------|-----|
| sn360-bridge (AirSim successor) | 🔴 Very high | 🟢 High | AirSim archived; large stranded user base; no modern Unity/Unreal + ROS 2 option |
| robot-brain | 🔴 High | 🟢 High | Everyone is bolting LLMs/VLAs onto robots ad-hoc; trend-driven |
| scenario-format | 🟡 Medium | 🟡 Medium | Real reproducibility pain; slow-burn standard |
| drone-rehost | 🟡 Medium | 🟡 Med (loud, niche) | Deep pain, small security audience; uniquely ours |
| sim-in-CI | 🟡 Medium | 🟡 Medium | Genuine HIL/SITL-in-CI gap; narrower audience |
| sensor/physics lib | 🟡 Medium | 🟡 Medium | On-ramp to premium models |
| SBOM/firmware CLI | 🟡 Medium (enterprise) | 🟠 Low-Med | Procurement trust (NDAA/Blue UAS, EU) |
| curated hub | 🟢 Low (magnet) | 🟠 Low-Med | SEO/credibility, not a painpoint |

**Biggest pain + biggest interest = sn360-bridge.** Start there.

## Stack reality

SkyTrack's simulation is **Unity/Unreal-based** (game-engine, AirSim-style).
This argues *against* open-sourcing the engine core and *for* open bridges,
formats, and tools that orbit it.

## One platform, multiple bodies

A drone and a ground robot (e.g. an Anki Vector rebuild) are the same problem in
two bodies: embedded firmware + sensors + an AI brain + a cloud backend. The
shared assets:

- **One sim** (your Unity/Unreal engine) → train/test brains in simulation,
  then sim-to-real.
- **One brain** (`perceive → plan → act` + HAL) → swap the body, keep the brain.
- **One firmware toolchain** (`drone-rehost`) → a drone autopilot *and* a ground
  robot are two targets that prove the toolchain is general.

A cheap, safe ground robot is the ideal **indoor testbed and demo** for the
shared brain — you cannot crash-test drone autonomy 50×/day in the office, but
you can with a small robot. It is a *tool that strengthens the drone roadmap*,
not a second product.

## Recommended sequence

1. **sn360-bridge** — the funnel everyone walks through; built generic so other
   bodies plug into the same bridge later for ~free.
2. **robot-brain** — drone is the primary body; ground robot is the cheap test
   body.
3. **drone-rehost** — drone firmware first; second body as the second target.
4. **scenario-format** — lock the ecosystem to your interchange standard.

## Licensing & branding

- **Apache-2.0** across the board (permissive + patent grant → max adoption).
- Each README carries sn360 branding and a clear "scale this up → sn360" CTA.
- Keep proprietary value (engine, cloud brain, hi-fi models) out of every repo.

## From projects to an ecosystem

The four pillars are one **ecosystem** in layers — community / pillars /
interchange standards / **`skytrack-core`** / assets-data — so every audience has
a door and a path to sn360. Full design in [`ECOSYSTEM.md`](./ECOSYSTEM.md);
diagrams in [`docs/DIAGRAMS.md`](./docs/DIAGRAMS.md).

Three principles make it an ecosystem, not just repos:

1. **`skytrack-core` is the keystone.** Shared ENU frame, message types, and
   transport unify the pillars and give third parties one stable foundation.
   Build it first.
2. **Build-without-permission.** Small seams (`Brain`, `HAL`, `Peripheral`,
   `IBridgeTransport`, scenario schema) let students extend a corner and
   researchers build whole products. Apache-2.0 permits commercial third-party
   products. This openness *is* the growth engine. Guide: `docs/EXTENDING.md`.
3. **A real, not artificial, ceiling.** Every open path is genuinely useful but
   tops out where sn360 begins (photoreal, hosted big brain, scaled fuzzing,
   analytics). If the ceiling isn't real, the funnel breaks.

The flywheel: more scenarios → more data → better brains → harder scenarios;
rehost crashes harden the whole stack. Each turn raises the others — and every
arrow eventually points at sn360.
