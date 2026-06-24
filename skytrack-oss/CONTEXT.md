# CONTEXT — how we got here

A durable record of the decisions behind `skytrack-oss`, so a fresh session
understands *why*, not just *what*. Update when a material decision changes.

## Background

- The host repo (`Firmware-Analysis-Papers`) is a curated list of academic
  firmware-analysis papers (rehosting, fuzzing, IoT/embedded security).
- The company builds **SkyTrack**, a drone product with **simulation software**,
  and a commercial platform referred to as **sn360**.
- The owner has prior skill with the **Anki Vector** robot and is rebuilding it
  with AI — but **SkyTrack drone remains the main focus**.

## Decisions made

1. **OSS model = open-core, "open rim / closed hub."** Open the connectors,
   formats, and tools; keep the engine, cloud brain, hi-fi models, and fleet in
   sn360. Goal: show usefulness, give the community real value, and drive
   adoption back to sn360.
2. **Sim stack is Unity/Unreal (AirSim-style).** → favor open bridges/formats
   around the engine rather than open-sourcing the engine core.
3. **Four projects chosen** (see `OSS-STRATEGY.md` for the painpoint ranking):
   - `sn360-bridge` — biggest painpoint (AirSim archived); the adoption on-ramp.
   - `robot-brain` — the embodied-AI/VLA trend bet; the sn360 core, opened at edges.
   - `drone-rehost` — credibility flagship tied to the firmware-analysis papers.
   - `scenario-format` — own-the-format slow-burn standard.
4. **Vector is a tool, not a second product.** Rule of thumb: if a task improves
   the shared brain/sim/firmware toolchain → do it; if it only improves Vector
   itself → skip it. Vector is the cheap, safe indoor **testbed**, a **demo**
   ("same brain, two bodies"), and a **second firmware target**.
5. **Monorepo of splittable folders.** A standalone GitHub repo could not be
   created from the working session (the GitHub integration is scoped to a single
   repo and lacks repo-creation permission). So each idea is a self-contained
   folder, splittable later via `git subtree split` (recipe in `README.md`).
   Revisit if a token with repo-creation scope (or an org) becomes available.
6. **Build real code, not just docs.** All four ship runnable scaffolds with
   self-tests/demos (verified). Production wiring is marked TODO in-code and in
   each `docs/BACKLOG.md`.

## Open questions / revisit later

- Create real separate private GitHub repos when repo-creation scope/an org is
  available; until then keep the monorepo.
- Confirm the exact sn360 product surface so funnel CTAs point at real offerings.
- Decide first public launch target (recommended: `sn360-bridge` as "the
  maintained AirSim successor").

## Branch & workflow

- All work on `claude/skytrack-oss-ideas-0ivndv`. Commit with descriptive
  messages; push with `git push -u origin claude/skytrack-oss-ideas-0ivndv`.
