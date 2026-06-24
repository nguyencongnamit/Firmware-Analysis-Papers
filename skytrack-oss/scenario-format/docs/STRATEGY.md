# STRATEGY

## Positioning

**Own the interchange standard.** `scenario-format` aims to be the portable,
reproducible *de facto* way to describe drone/robot test scenarios — the
"OpenScenario for drones." It is the *rim* in skytrack-oss's "open rim, closed
hub" strategy: the format and tooling are free and ubiquitous; the value that
scales — high-fidelity runtime, cloud execution, libraries, and analytics —
stays in **sn360**.

In the monorepo's painpoint ranking this is the **slow-burn ecosystem standard**:
medium pain, medium interest, long compounding payoff. It is sequenced last
because its value grows with adoption of the other projects (especially
`sn360-bridge` and `robot-brain`).

## Open vs. sn360 split

| Capability | Open (this repo, Apache-2.0) | sn360 (proprietary) |
|------------|------------------------------|---------------------|
| Scenario format + JSON Schema | ✅ | imports/exports it |
| CLI validator + lint | ✅ | — |
| Reference player (planned) | ✅ basic, drives `sn360-bridge` | — |
| Example scenarios | ✅ 4 today | — |
| High-fidelity runtime & physics | — | ✅ |
| Scaled / cloud scenario execution (thousands of runs) | — | ✅ |
| Scenario libraries & analytics | — | ✅ |
| Result/report storage, dashboards, regression tracking | report *schema* planned (open) | ✅ product |

Rule: the open side must be genuinely useful standalone; the paid side is the
*scale mode / easy mode / fidelity mode*, never a crippled gate.

## Licensing

- **Apache-2.0** — permissive + patent grant, maximizing adoption. The folder
  carries its own `LICENSE` so it stays correct after a split into a standalone
  repo.
- The schema `$id` is namespaced under `sn360.dev` to anchor the standard to the
  product without restricting use.

## Go-to-market

1. **Be the default format.** Ship a clean schema, a fast validator, and clear
   examples so the easiest way to write a drone test scenario is this format.
2. **Integrate where developers already are.** The reference player drives
   `sn360-bridge`; bodies bind through `robot-brain`'s HAL. Adopting any sibling
   project pulls the format along.
3. **Make reproducibility the hook.** "Commit the file, get the same run" is the
   pitch — git-native, diffable, deterministic.
4. **Seed an ecosystem.** A scenario gallery (BACKLOG M4) and CI-validated
   examples (M5) lower the cost of contributing and citing.
5. **Funnel to sn360.** Every README/spec carries an honest "scale this up →
   sn360" CTA; the format users already own is sn360's native input.

## Versioning & governance

- **Semver, scenario-declared.** Files pin `scenario_version`; within `0.1.x`
  only backward-compatible additions land; breaking changes bump the minor
  pre-1.0. The version is embedded in the schema `$id`.
- **Validator is the contract.** It must always pass on the shipped examples;
  CI validation of all examples is the planned guardrail (M5).
- **Planned governance policy** (M5): a documented process for proposing schema
  changes, an extension/`x-` namespace convention, and a deprecation policy
  before 1.0.

## Success metrics

- **Adoption:** external repos / tools that read or write the format; GitHub
  stars, forks, citations.
- **Reproducibility:** scenarios shared and re-run unmodified across teams.
- **Ecosystem:** number of contributed gallery scenarios; integrations through
  `sn360-bridge` / `robot-brain`.
- **Funnel:** conversions from open-format users to sn360 for scale/fidelity.
- **Health:** examples always validate in CI; schema changes follow the semver
  policy without surprise breakage.
