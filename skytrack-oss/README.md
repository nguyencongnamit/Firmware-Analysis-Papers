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

## The four projects

| Folder | Project | What it is | Role in the funnel |
|--------|---------|-----------|--------------------|
| [`sn360-bridge/`](./sn360-bridge) | **sn360-bridge** | Unity/Unreal ↔ PX4 · MAVLink · ROS 2 connector — the maintained **AirSim successor** | Adoption on-ramp: everyone installs this before they ever pay |
| [`robot-brain/`](./robot-brain) | **robot-brain** | Open `perceive → plan → act` interface + HAL; one brain runs a drone *or* a ground robot | The sn360 core, opened at the edges |
| [`drone-rehost/`](./drone-rehost) | **drone-rehost** | Firmware rehosting/emulation harness + MAVLink fuzzer | Credibility flagship — ties to the firmware-analysis research |
| [`scenario-format/`](./scenario-format) | **scenario-format** | Open mission/scenario interchange standard + validator | Own the format; monetize the runtime |

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
