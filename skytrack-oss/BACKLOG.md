# BACKLOG — skytrack-oss (cross-project)

Cross-cutting roadmap. Per-project detail lives in each `*/docs/BACKLOG.md`.
Status legend: ✅ done · 🟡 in progress · ⬜ todo.

## Now (top priority)

- ⬜ **Extract `skytrack-core`** (the keystone): shared ENU frame, message types,
  units, MAVLink/ROS 2 helpers. Refactor the four pillars onto it. (Turns 4 repos
  into 1 ecosystem.)
- ⬜ **Make a brain fly PX4 SITL.** Wire real MAVLink transport into
  `sn360-bridge/common`, then bind it in `robot-brain`'s `DroneHAL`.
  (→ `sn360-bridge` M1–M2, `robot-brain` M1)
- ⬜ **CI smoke tests** on every push (run all self-tests/demos + validate examples).

## Next

- ⬜ **Examples gallery + docs landing page** — the "show me it works" surface.
- ⬜ `sn360-bridge`: UDP transport for Unity/Unreal plugins; PX4 SITL round-trip
  demo (arm → takeoff → fly a square).
- ⬜ `scenario-format`: reference player driving `sn360-bridge`; result/report schema.
- ⬜ `robot-brain`: local small-VLM perceiver + small-LLM planner reference (free tier).
- ⬜ `drone-rehost`: gdb/Unicorn MMIO hook wiring `rehost.py` into QEMU; bring a
  real flight image to its main loop.
- ⬜ **Governance:** one `CONTRIBUTING.md` + an RFC/`SkyEP` process for the
  interchange standards; code of conduct; community channel.

## Later

- ⬜ "Migrating from AirSim" guide (`sn360-bridge`) — key for adoption.
- ⬜ Ground-robot (Vector) adapter in `robot-brain` + second firmware target in
  `drone-rehost` → the "same platform, two bodies" demo.
- ⬜ Assets/data layer: datasets · benchmarks + leaderboard · model zoo · body packs.
- ⬜ Enterprise door: SBOM / compliance CLI (NDAA/Blue UAS, EU).
- ⬜ Education track: tutorials + the firmware-papers awareness hub.
- ⬜ End-to-end integration: `scenario-format` → `robot-brain` → `sn360-bridge` →
  engine, with `drone-rehost` as optional SITL firmware target.
- ⬜ Convert per-project `docs/` Mermaid diagrams to ASCII (consistency w/ preference).

## Done

- ✅ Scaffolded four splittable OSS projects with the open-rim/closed-hub funnel.
- ✅ Built runnable code + self-tests for all four (verified).
- ✅ Per-project doc sets (IDEA/ARCHITECTURE/FLOW/JOURNEY/STRATEGY/BACKLOG) + each
  project `CLAUDE.md`.
- ✅ Session-refresh docs: `CLAUDE.md`, `CONTEXT.md`, `BACKLOG.md`.
- ✅ Ecosystem layer: `ECOSYSTEM.md`, `docs/EXTENDING.md`, `docs/DIAGRAMS.md`,
  `docs/IDEAS-OVERVIEW.md`, top-level `docs/FLOW.md`; ASCII `docs/ARCHITECTURE.md`
  + `docs/JOURNEY.md`.
- ✅ Extension proof: `robot-brain/examples/custom_brain_obstacle_avoid.py` (verified).
- ✅ Rendered (non-Mermaid/non-ASCII) diagrams: Graphviz DOT → SVG+PNG in
  `docs/diagrams/` (ecosystem, layers, bridge, robot-brain, rehost, scenario).

## Cross-project dependency

```
   scenario-format ─▶ robot-brain ─▶ sn360-bridge ─▶ engine
        │                 │              ▲              │
        └── all build on ─┴─ skytrack-core ─┘           ▼
   drone-rehost ···· SITL firmware target ····▶  (all funnel to) sn360
```
