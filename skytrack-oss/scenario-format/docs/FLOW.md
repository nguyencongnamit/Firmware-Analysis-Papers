# FLOW — authoring & execution

How a scenario goes from a JSON file to a pass/fail result. The validate/lint
path is **built and working today**; the run/evaluate path uses the **planned**
reference player + `sn360-bridge`.

## End-to-end flow

```mermaid
flowchart TD
    A["Author scenario<br/>(scenario.json)"] --> B["Validate against<br/>JSON Schema (v0.1.0)"]
    B -->|schema errors| AERR["Fix file"] --> A
    B -->|valid| C["Cross-field lint<br/>(unknown agent refs, etc.)"]
    C -->|lint warnings| C2["Review / fix<br/>(non-fatal)"]
    C2 --> D
    C -->|clean| D["Run scenario"]

    subgraph Run["Run (planned: reference player → sn360-bridge)"]
        D --> E["Reference player loads file"]
        E --> F["Drive runtime via sn360-bridge<br/>(MAVLink · PX4 · ROS 2)"]
        F --> G["Inject faults at trigger.at_s"]
        G --> H["Evaluate success_criteria"]
    end

    H --> I{"All criteria met?"}
    I -- yes --> PASS["PASS report"]
    I -- no --> FAIL["FAIL report<br/>(which criteria, why)"]

    PASS -.->|"scale to thousands + analytics"| SN["sn360"]
    FAIL -.->|"deeper hi-fi debugging"| SN

    classDef planned stroke-dasharray: 5 5;
    class Run,E,F,G,H,PASS,FAIL planned;
```

### Stages

1. **Author** — write a single JSON document (world, agents+missions, faults,
   success_criteria). Deterministic via `seed`.
2. **Validate** — `python validator/validate.py <path>` runs the JSON Schema.
   Schema errors are fatal (exit `1`).
3. **Lint** — cross-field checks the schema can't express (e.g. a fault or
   criterion referencing an agent id that doesn't exist). Reported as non-fatal
   `! lint:` warnings.
4. **Run** *(planned)* — the reference player loads the validated file and drives
   `sn360-bridge`; faults fire at their `trigger.at_s`.
5. **Evaluate** *(planned)* — `success_criteria` are checked to produce a
   pass/fail report (report schema is also planned — see BACKLOG M3).
6. **Funnel** — running thousands at high fidelity with analytics → sn360.

## Validation sequence (built today)

```mermaid
sequenceDiagram
    actor User
    participant CLI as validate.py
    participant FS as Filesystem
    participant JS as Draft202012Validator
    participant Lint as lint()

    User->>CLI: python validate.py examples/
    CLI->>CLI: expand args (dir → *.json)
    CLI->>FS: load schema/scenario.schema.json
    CLI->>JS: check_schema(schema)
    loop each scenario file
        CLI->>FS: read_text()
        alt invalid JSON
            CLI-->>User: FAIL <path>: invalid JSON
        else parsed
            CLI->>JS: iter_errors(scenario)
            alt schema errors
                JS-->>CLI: errors (sorted by path)
                CLI-->>User: FAIL <path>: N schema error(s)
            else valid
                CLI-->>User: OK <path>
                CLI->>Lint: lint(scenario)
                Lint-->>CLI: warnings (unknown agent refs)
                CLI-->>User: ! lint: <warning> (if any)
            end
        end
    end
    CLI-->>User: exit 0 (all pass) / 1 (any fail)
```

The validator is intentionally simple and dependency-light: one schema check
(`jsonschema`) plus a small hand-written lint pass. It is the only piece that
must always stay green for the format to be trustworthy.
