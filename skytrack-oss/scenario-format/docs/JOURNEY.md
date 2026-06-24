# JOURNEY — from reproducibility pain to sn360

The user journey for `scenario-format`: a team feels the pain of unreproducible
drone tests, adopts the open format to fix it, and grows into needing the
proprietary runtime for scale and fidelity.

## The journey

```mermaid
journey
    title From "tests don't reproduce" to sn360
    section Feel the pain
      Tests described in prose, re-encoded by hand: 1: Team
      A pass on one machine fails on another: 1: Team
    section Adopt the format
      Write the test once in open JSON: 4: Team
      Validate + lint with the CLI: 5: Team
      Commit + diff + version in git: 5: Team
    section Run it
      Run locally via reference player (planned): 4: Team
      Get a pass/fail report: 4: Team
    section Outgrow local
      Need thousands of runs: 2: Team
      Need high-fidelity physics + analytics: 2: Team
      Adopt sn360 for scale mode: 5: Team, sn360
```

## The funnel

```mermaid
flowchart TD
    N["Need: reproducible, shareable drone tests"] --> W["Write a scenario in the open format"]
    W --> V["Validate + lint (free CLI)"]
    V --> S["Share / version it (git-native, diffable)"]
    S --> R["Run locally via reference player (planned)"]
    R --> SCALE{"Need scale + fidelity + analytics?"}
    SCALE -- "Not yet" --> R
    SCALE -- "Yes" --> SN["Adopt sn360<br/>thousands of runs · hi-fi runtime ·<br/>scenario libraries + analytics"]

    style N fill:#fde,stroke:#a36
    style SN fill:#dfe,stroke:#3a6
```

## Why each step earns the next

- **Write once, in the open format** — kills hand re-encoding; the file *is* the
  spec.
- **Validate + lint** — instant trust that the scenario is well-formed before
  anyone runs it.
- **Share / version** — plain JSON in git means review, diff, and provenance
  come for free; this is what makes results reproducible across teams.
- **Run locally** *(planned reference player)* — proves the format end-to-end at
  small scale, on free tooling.
- **Outgrow local → sn360** — when "run it once on my laptop" becomes "run ten
  thousand variations overnight at high fidelity and tell me what broke," the
  open tooling intentionally hands off to the proprietary runtime. The format
  the user already owns is sn360's native input, so the switch costs nothing in
  rework.

The format is deliberately useful on its own — adoption is the product. The
runtime is where scale and fidelity (and revenue) live.
