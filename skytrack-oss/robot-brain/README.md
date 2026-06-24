# robot-brain

An open, body-agnostic autonomy interface: **`perceive → plan → act`** over a
hardware-abstraction layer (HAL). Write the brain once; run it on a drone, a
ground robot, or in simulation.

> Part of [skytrack-oss](../). Open the interface + a local tier; run the big
> multi-robot brain in **sn360**.

## Why this exists

Everyone is bolting LLMs and vision-language-action (VLA) models onto robots in
one-off, non-portable ways. `robot-brain` defines a small, stable contract so a
single autonomy stack can move between bodies and between sim and reality.

## The contract

```python
class Brain:
    def perceive(self, obs: Observation) -> WorldState: ...
    def plan(self, state: WorldState, goal: Goal) -> Plan: ...
    def act(self, plan: Plan) -> list[Command]: ...

class HAL:          # implemented per body
    def read_sensors(self) -> Observation: ...
    def send_commands(self, cmds: list[Command]) -> None: ...
```

- `core/` — the brain loop, types, and a reference VLM-perception / LLM-planner
  skeleton.
- `adapters/` — HAL implementations (drone via `sn360-bridge`, a ground-robot
  body, a pure-sim body).
- `examples/` — "same brain, two bodies" demos.
- `docs/` — the contract, the skill/tool interface, sim-to-real notes.

## One brain, many bodies

A drone and a small ground robot are the same loop with different HALs. The
ground robot is the **cheap, safe, indoor testbed**: iterate the AI fast and
harmlessly, then deploy the matured brain to the drone. Same `core/`, different
`adapters/`.

## What's open vs. what's sn360

| Open (this repo) | sn360 (proprietary) |
|------------------|---------------------|
| The interface + HAL contract | The hosted, large-model brain |
| A small local-model reference path | Multi-robot / fleet orchestration |
| Sim + drone + ground-robot adapters | Managed memory, datasets, evals |

## Status

🚧 Scaffold. Interfaces and structure only.

## Roadmap

- [ ] `core/`: brain loop + types, pluggable perception/planner
- [ ] `adapters/`: sim body (via sn360-bridge), drone body, ground-robot body
- [ ] `examples/`: one brain switching bodies via config
- [ ] Local-model reference (small VLM + LLM) for the free tier

## Scale this up

Want the hosted large-model brain, fleet orchestration, and managed evals?
→ **sn360**.

## License

Apache-2.0 — see [LICENSE](./LICENSE).
