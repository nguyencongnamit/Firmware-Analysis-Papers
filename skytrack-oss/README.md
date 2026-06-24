# skytrack-oss

Open-source building blocks for the **SkyTrack** drone simulation platform — each
one genuinely useful to the robotics community on its own, and each one designed
to funnel adoption back to **sn360** (the proprietary high-fidelity sim + cloud
brain + fleet platform).

> **Strategy in one line:** open the *rim* (the connectors, formats, and tools
> people touch every day), keep the *hub* (the Unity/Unreal engine, the cloud
> brain, the high-fidelity models) in sn360.

This is a **monorepo of independent projects**. Each folder is a complete
mini-repo with its own README and LICENSE, ready to be extracted into a
standalone public repo when you announce it (see [Splitting out](#splitting-a-folder-into-its-own-repo)).

Each project ships **working code**, not just docs — runnable demos and
self-tests you can try right now:

```bash
# robot-brain: same brain flies a drone and drives a ground robot
python robot-brain/examples/one_brain_two_bodies.py

# drone-rehost: MMIO peripheral bus self-test + MAVLink mutation fuzzer
python drone-rehost/harness/rehost.py
python drone-rehost/fuzzer/mavlink_fuzzer.py -n 5000

# scenario-format: validate the example scenarios against the schema
pip install -r scenario-format/validator/requirements.txt
python scenario-format/validator/validate.py scenario-format/examples/

# sn360-bridge: MAVLink core in dry-run (no autopilot needed)
python sn360-bridge/common/mavlink_bridge.py --dry-run --seconds 3
```

## The four projects

| Folder | Project | What it is | Role in the funnel |
|--------|---------|-----------|--------------------|
| [`sn360-bridge/`](./sn360-bridge) | **sn360-bridge** | Unity/Unreal ↔ PX4 · MAVLink · ROS 2 connector — the maintained **AirSim successor** | Adoption on-ramp: everyone installs this before they ever pay |
| [`robot-brain/`](./robot-brain) | **robot-brain** | Open `perceive → plan → act` interface + HAL; one brain runs a drone *or* a ground robot | The sn360 core, opened at the edges |
| [`drone-rehost/`](./drone-rehost) | **drone-rehost** | Firmware rehosting/emulation harness + MAVLink fuzzer | Credibility flagship — ties to the firmware-analysis research |
| [`scenario-format/`](./scenario-format) | **scenario-format** | Open mission/scenario interchange standard + validator | Own the format; monetize the runtime |

## Documentation

**Start here / session memory:** [`CLAUDE.md`](./CLAUDE.md) ·
[`CONTEXT.md`](./CONTEXT.md) · [`BACKLOG.md`](./BACKLOG.md) ·
[`OSS-STRATEGY.md`](./OSS-STRATEGY.md)

**Platform diagrams:** [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md) ·
[`docs/JOURNEY.md`](./docs/JOURNEY.md)

**Per project**, each folder carries a `CLAUDE.md` (session memory) and a `docs/`
set: `IDEA.md`, `ARCHITECTURE.md`, `FLOW.md`, `JOURNEY.md`, `STRATEGY.md`,
`BACKLOG.md` — all with Mermaid diagrams.

> Before starting **or** clearing/compacting a session, run the refresh checklist
> in [`CLAUDE.md`](./CLAUDE.md): re-read the memory docs, check the branch, run
> the smoke tests, and update status + backlog.

## Priority & sequencing

1. **`sn360-bridge`** first — biggest, clearest market painpoint (AirSim is
   archived/unmaintained and there's no modern Unity/Unreal + ROS 2 option). You
   already own the engine. Highest chance of broad interest.
2. **`robot-brain`** second — rides the embodied-AI / VLA wave; this is where a
   cheap ground-robot testbed earns its keep iterating the AI fast and safely.
3. **`drone-rehost`** as the depth/credibility play — loud in the security
   community, smaller crowd, uniquely yours.
4. **`scenario-format`** as the slow-burn ecosystem standard.

## Focus

SkyTrack drone remains the **product focus**. The other bodies (e.g. a ground
robot) are *testbeds, demos, and a second firmware target* — they make the
shared brain / sim / firmware toolchain stronger; they are not parallel
products. Rule of thumb: *if a task improves the shared brain, sim, or firmware
toolchain → do it. If it only improves a side body → skip it.*

## Licensing

All projects use **Apache-2.0** (permissive, maximizes adoption, patent grant).
Each folder carries its own `LICENSE` so it stays correct after a split.

## Splitting a folder into its own repo

When you're ready to publish one project standalone (preserving its history):

```bash
# from the repo root, on a clean working tree
git subtree split --prefix=skytrack-oss/sn360-bridge -b sn360-bridge-export

# create an empty private repo on GitHub named sn360-bridge, then:
git push git@github.com:nguyencongnamit/sn360-bridge.git sn360-bridge-export:main
```

Repeat per folder. Until then, develop everything here on
`claude/skytrack-oss-ideas-0ivndv`.

---

*Note: a standalone private GitHub repo could not be created directly from this
session — the GitHub integration here is scoped to a single repository. These
projects are scaffolded as splittable folders so nothing is blocked; create the
private repos manually (or re-run with a token that has repo-creation scope) and
use the `git subtree split` recipe above to populate them.*
