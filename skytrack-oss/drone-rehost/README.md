# drone-rehost

A firmware **rehosting / emulation harness** for flight controllers and small
robots — run autopilot firmware on commodity hardware (no flight rig), with
peripheral modeling for IMU/GPS/ESC and a **MAVLink fuzzer** + crash corpus.

> Part of [skytrack-oss](../). The credibility flagship — it makes the
> [firmware-analysis research](../../README.md) *executable*.

## Why this exists

The firmware-analysis literature (HALucinator, P2IM, FirmAE, Avatar,
para-rehosting, etc.) shows how to emulate embedded firmware on commodity
hardware. None of it is packaged for the **drone** world. `drone-rehost` applies
that lineage to flight-controller firmware so researchers can analyze, fuzz, and
test it without hardware — and feed it straight into simulation as a
software-in-the-loop target.

## What it does

- `harness/` — QEMU-based rehosting scaffolding + peripheral interface modeling.
- `peripherals/` — models for IMU, barometer, GPS, ESC/motor, MAVLink links.
- `fuzzer/` — greybox MAVLink / companion-link fuzzer (FIRM-AFL / IoTFuzzer
  lineage), with the simulator as the behavioral oracle.
- `corpus/` — seed inputs and known crash cases.
- `docs/` — rehosting notes, target bring-up, references back to the paper list.

## One toolchain, multiple targets

The harness is **not drone-specific**. A drone autopilot is the first target; a
small ground robot's firmware (e.g. an Anki Vector rebuild) is a natural second
target. Supporting both proves the toolchain is genuinely general — exactly the
"show strength" credibility goal.

## What's open vs. what's sn360

| Open (this repo) | sn360 (proprietary) |
|------------------|---------------------|
| Rehosting harness + peripheral models | Hi-fidelity sensor/physics oracle |
| MAVLink fuzzer + crash corpus | Managed continuous fuzzing at scale |
| Bring-up docs | Curated vuln datasets / reports |

## Status

🚧 Scaffold. Structure and design notes only.

## Roadmap

- [ ] `harness/`: bring up a PX4/ArduPilot-class image under QEMU
- [ ] `peripherals/`: IMU + GPS + ESC stubs sufficient to reach the main loop
- [ ] `fuzzer/`: MAVLink message fuzzer with crash triage
- [ ] `corpus/`: seed messages + reproducible crashes
- [ ] Pipe rehosted firmware into the sim as a SITL target

## Scale this up

Want continuous, scaled fuzzing with a high-fidelity oracle and curated
findings? → **sn360**.

## License

Apache-2.0 — see [LICENSE](./LICENSE).
