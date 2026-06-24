# CLAUDE.md — scenario-format session memory

**scenario-format** is an open, versionable JSON interchange format for
drone/robot test scenarios (missions, environment/wind, faults, swarms, success
criteria), shipped with a CLI validator and a (planned) reference player. It is
one project in the [skytrack-oss](../) monorepo and follows the "open the
format, monetize the runtime" funnel: the format, JSON Schema, and validator are
free and Apache-2.0; high-fidelity runtime/physics, scaled cloud scenario
execution, and scenario libraries + analytics live in the proprietary product
**sn360**. The goal is to become the portable, reproducible *de facto* standard
("OpenScenario for drones") and run scenarios through `sn360-bridge`.

## Current status

- ✅ **Schema** `schema/scenario.schema.json` — JSON Schema draft 2020-12,
  v0.1.0. Working.
- ✅ **Examples** — 4 reference scenarios, all validate:
  `gps_denied_approach.json`, `wind_gust.json`, `sensor_dropout.json`,
  `swarm_formation.json`.
- ✅ **Validator** `validator/validate.py` — `Draft202012Validator` + cross-field
  lint (faults/criteria referencing unknown agent ids). Working.
- 🚧 **Reference player** — **NOT built yet (TODO)**. The README, SPEC, and these
  docs describe it as planned; it will drive `sn360-bridge`.
- 🚧 **Result/report schema** (pass/fail output) — planned, not built.
- ⚠️ Requires `pip install -r validator/requirements.txt` for `jsonschema`.

## Key files

| Path | What |
|------|------|
| `README.md` | Project overview + open-vs-sn360 split |
| `docs/SPEC.md` | Human-readable spec for v0.1.0 |
| `schema/scenario.schema.json` | The schema (source of truth) |
| `validator/validate.py` | CLI validator + lint |
| `validator/requirements.txt` | `jsonschema` dependency |
| `examples/*.json` | 4 validating reference scenarios |
| `docs/IDEA.md` | Vision / painpoint / value |
| `docs/ARCHITECTURE.md` | Format structure + object model |
| `docs/FLOW.md` | Authoring + execution + validation flow |
| `docs/JOURNEY.md` | User journey + funnel |
| `docs/STRATEGY.md` | Positioning, open-vs-sn360, GTM, metrics |
| `docs/BACKLOG.md` | Prioritized milestones — **resume here** |

## How to run

```bash
pip install -r validator/requirements.txt
python validator/validate.py examples/        # validate every *.json in a dir
python validator/validate.py examples/wind_gust.json   # single file
```

Exit code is `0` when all files pass, `1` otherwise. Validation runs JSON Schema
checks then prints lint warnings (e.g. unknown agent refs).

## Conventions

- **Semver schema** — scenarios declare `scenario_version` (`0.1.x`). Within
  `0.1.x` only backward-compatible additions land; breaking changes bump the
  minor (pre-1.0).
- **Coordinate frame** — `[x, y, z]` in **meters, local ENU** relative to
  `world.origin` (x=East, y=North, z=Up).
- **Deterministic** — `seed` makes a run reproducible; everything needed to
  replay is in the file.
- **License** — Apache-2.0.
- **Funnel** — own the format / monetize the runtime; every doc keeps the sn360
  CTA honest (free format + validator, paid hi-fi runtime + scale + analytics).

## Where to resume

→ **[docs/BACKLOG.md](./docs/BACKLOG.md)** for prioritized milestones (M1–M5).

## Links

- Monorepo root: [../README.md](../README.md), [../OSS-STRATEGY.md](../OSS-STRATEGY.md)
- Sibling projects: [`sn360-bridge`](../sn360-bridge), [`robot-brain`](../robot-brain), [`drone-rehost`](../drone-rehost)

## Refresh checklist (before starting or clearing a session)

1. Re-read this file, then `README.md`, `docs/SPEC.md`, and `docs/BACKLOG.md`.
2. Confirm the git branch is `claude/skytrack-oss-ideas-0ivndv`.
3. Smoke test: `pip install -r validator/requirements.txt && python validator/validate.py examples/`
   — all 4 examples should print `OK`.
4. Remember: reference player and report schema are still TODO; don't document
   them as if they exist.
