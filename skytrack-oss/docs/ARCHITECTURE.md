# Platform & ecosystem architecture

How the open projects fit together and where the proprietary **sn360** hub takes
over. ASCII (no renderer). Per-project `docs/ARCHITECTURE.md` files have detail;
[`DIAGRAMS.md`](./DIAGRAMS.md) collects every diagram in one place.

## Ecosystem layers

```
  ┌──────────────────────────────────────────────────────────────────────┐
  │  COMMUNITY    docs site · examples gallery · tutorials · RFCs ·        │
  │               Discord/forum · firmware-papers awareness hub            │
  ├──────────────────────────────────────────────────────────────────────┤
  │  PILLARS      sn360-bridge   robot-brain   drone-rehost   scenario-fmt │
  │               (connect)      (intelligence)(security)     (tests)      │
  ├──────────────────────────────────────────────────────────────────────┤
  │  STANDARDS    scenario spec · telemetry/log · model API ·              │
  │               brain↔HAL contract · result/report schema               │
  ├──────────────────────────────────────────────────────────────────────┤
  │  CORE         skytrack-core: ENU frame · message types · units · utils │
  ├──────────────────────────────────────────────────────────────────────┤
  │  ASSETS/DATA  datasets · benchmarks+leaderboard · model zoo ·          │
  │               scenario library · body packs                           │
  └──────────────────────────────────────────────────────────────────────┘
                    every layer ─────────────▶  sn360 (paid hub)
```

**Keystone:** `skytrack-core` (planned) is the stable foundation every pillar and
every third-party product sits on. It's what makes the four pillars *one
ecosystem* instead of four loose repos. Build it first.

## Open rim, closed hub

```
            OPEN RIM  (Apache-2.0 · skytrack-oss)
  ┌─────────────────────────────────────────────────────────────┐
  │  scenario-format ─▶ robot-brain ─▶ sn360-bridge ─▶ engine I/O │
  │        drone-rehost ····· SITL firmware target ····▶         │
  └───────┬──────────────┬───────────────┬───────────────┬───────┘
          ▼              ▼               ▼               ▼
  ┌─────────────────────────────────────────────────────────────┐
  │              CLOSED HUB — sn360 (proprietary)                 │
  │  photoreal worlds · hosted big-model brain · hi-fi models ·   │
  │  scaled cloud simulation · fleet · analytics                  │
  └─────────────────────────────────────────────────────────────┘
```

## Dependency map

```
                          ┌───────────────────────────┐
                          │       skytrack-core       │ ◀── everything builds on this
                          └─────┬─────┬─────┬─────┬─────┘
              ┌─────────────────┘     │     │     └─────────────────┐
              ▼                       ▼     ▼                       ▼
       scenario-format          robot-brain   sn360-bridge     drone-rehost
              │ feeds tests          │ commands    │ MAVLink         │ SITL target
              └─────────────────────▶ ◀──binds HAL─┘ ◀───────────────┘
```

## Shared conventions (the contract every piece honors)

| Concern | Convention |
|---------|-----------|
| Frame | ENU meters (x=East, y=North, z=Up); convert at edges (MAVLink NED, Unity Y-up, Unreal Z-up/cm) |
| Transport | MAVLink (pymavlink) + ROS 2 / DDS, centralized in `sn360-bridge/common` (→ `skytrack-core`) |
| Interfaces | `Brain`, `HAL`, `Peripheral`, `IBridgeTransport`, scenario JSON Schema |
| License | Apache-2.0 everywhere |
| Funnel | each project useful alone; scale/fidelity/fleet → sn360 |

## One platform, two bodies

```
   robot-brain (one brain)
        ├─ DroneHAL ──────▶ SkyTrack drone   (product focus)
        └─ GroundRobotHAL ─▶ ground robot     (Vector testbed / demo / 2nd fw target)
                 both share core + sim + firmware toolchain → both funnel to sn360
```

## Extension points (third-party products plug in here)

See [`EXTENDING.md`](./EXTENDING.md). Implement one seam, plug in, nothing else
changes — students extend a corner, researchers build whole products.
