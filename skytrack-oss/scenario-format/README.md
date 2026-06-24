# scenario-format

An open, versionable interchange format for **drone/robot test scenarios** —
missions, wind/weather, sensor failures, GPS-denied zones, and swarm
choreography — plus a CLI **validator** and reference player.

> Part of [skytrack-oss](../). Own the format; run it at fidelity & scale in
> **sn360**. Classic "open the standard, monetize the runtime."

## Why this exists

There is no portable, reproducible way to share drone test scenarios across
tools. Teams re-encode the same wind/failure/mission setups by hand. A clean
JSON-Schema standard lets scenarios be versioned, diffed, shared, and replayed
anywhere — and makes results reproducible.

## What it does

- `schema/` — JSON Schema for the scenario DSL (missions, environment, faults,
  swarms, success criteria).
- `examples/` — reference scenarios (GPS-denied approach, wind gust, sensor
  dropout, swarm formation).
- `validator/` — CLI that validates and lints a scenario file.
- `docs/` — the spec, versioning policy, and an extension guide.

## Design goals

- **Portable** — engine- and stack-agnostic; runs through `sn360-bridge`.
- **Versioned** — semantic versioning of the schema; scenarios declare their version.
- **Reproducible** — deterministic seeds; everything needed to replay is in the file.
- **Composable** — environments, faults, and missions are independent modules.

## What's open vs. what's sn360

| Open (this repo) | sn360 (proprietary) |
|------------------|---------------------|
| The format + JSON Schema | High-fidelity runtime & physics |
| Validator + reference player | Scaled/cloud scenario execution |
| Example scenarios | Scenario libraries & analytics |

## Status

🚧 Scaffold. Schema and examples to be filled in.

## Roadmap

- [ ] `schema/`: v0.1 — mission + environment + success criteria
- [ ] `schema/`: faults (sensor dropout, GPS-denied, wind) + swarm blocks
- [ ] `validator/`: validate + lint + helpful errors
- [ ] `examples/`: 4 reference scenarios
- [ ] Reference player via `sn360-bridge`

## Scale this up

Want to run thousands of scenarios at high fidelity with analytics?
→ **sn360**.

## License

Apache-2.0 — see [LICENSE](./LICENSE).
