# CLAUDE.md — drone-rehost session memory

`drone-rehost` is a firmware **rehosting / emulation harness** for flight-controller
firmware plus a **MAVLink mutation fuzzer**. It makes the firmware-analysis research
in the parent [paper list](../../README.md) *executable* for drones and small robots:
boot autopilot firmware on commodity hardware (no flight rig), model just enough of
the IMU/GPS/ESC peripherals (P2IM / HALucinator / FirmAE lineage) to reach the main
control loop, and fuzz the message-parsing surface. It is the **credibility flagship**
of [skytrack-oss](../) — open the harness/fuzzer (the rim), funnel scaled continuous
fuzzing + a hi-fidelity oracle + curated vuln datasets to the commercial **sn360** (the hub).

## Current status (be honest about the scaffold)

- **Working today (pure Python, no QEMU needed):**
  - `harness/rehost.py` — `MmioBus` dispatch + a self-test that passes
    (`rehost MMIO bus self-test: OK`).
  - `peripherals/` — `IMU` (MPU-6000-class, `WHO_AM_I = 0x68`), `GPS` (UBX NAV-PVT
    stream with a `fix_ok` toggle for GPS-denied), `ESC` (PWM duty / throttle).
  - `fuzzer/mavlink_fuzzer.py` — mutation fuzzer, loads the 3 corpus seeds, runs
    5000 iterations clean against the built-in `toy_parse` target.
- **TODO / not built yet:**
  - **Full QEMU rehosting** needs a real `firmware.elf` **and** a gdb/Unicorn MMIO
    hook that catches MMIO faults and calls `MmioBus.read/write`. `run_qemu.sh`
    boots Cortex-M with a gdb stub but the hook is not wired up.
  - The fuzzer currently targets a **toy MAVLink v1 framer**, not real rehosted
    firmware. Pointing it at a rehosted parser is planned.
  - Sim/scenario oracle feeding ground truth into IMU/GPS is designed
    (`IMU.set_truth`, `GPS.fix_ok`) but not yet driven from a live sim.

## Key files

| Path | What |
|------|------|
| `harness/rehost.py` | `MmioBus` MMIO dispatch + self-test (the core, engine-independent) |
| `harness/run_qemu.sh` | `qemu-system-arm` Cortex-M boot + gdb stub (hook TODO) |
| `peripherals/base.py` | `Peripheral` ABC: `handles` / `read` / `write` / `tick` |
| `peripherals/imu.py` | IMU model, `WHO_AM_I 0x68`, `set_truth(accel, gyro)` |
| `peripherals/gps.py` | GPS model, UBX NAV-PVT frame, `fix_ok` toggle |
| `peripherals/esc.py` | ESC/PWM model, per-channel duty, `throttle()` |
| `peripherals/__init__.py` | `default_peripherals()` -> `[IMU, GPS, ESC]` |
| `fuzzer/mavlink_fuzzer.py` | mutation fuzzer, `toy_parse` target, corpus loader |
| `corpus/*.bin` | seed frames: heartbeat, sys_status, param_request |
| `docs/REHOSTING.md` | rehosting notes + bring-up commands |

## How to run

```bash
cd skytrack-oss/drone-rehost
python harness/rehost.py                 # MMIO bus self-test (smoke test)
python fuzzer/mavlink_fuzzer.py -n 5000  # mutation-fuzz the toy parser

# Full rehosting (needs a firmware image + the TODO MMIO hook):
./harness/run_qemu.sh path/to/firmware.elf netduinoplus2
```

## Conventions

- **P2IM-style unmodeled MMIO:** unknown reads return `0` and are appended to
  `MmioBus.unhandled` (never trap), so firmware keeps progressing. Promote
  hot/most-hit unmodeled addresses into real peripheral models.
- **License:** Apache-2.0 (`LICENSE` in this folder).
- **Funnel:** every doc ends with a "scale up -> sn360" CTA; keep the proprietary
  value (hi-fi oracle, scaled fuzzing, curated datasets) out of this repo.
- **Second target:** a ground robot (Anki Vector rebuild) is a *second firmware
  target* proving the toolchain is general — NOT a parallel product. Drone is the focus.

## Where to resume

See [`docs/BACKLOG.md`](./docs/BACKLOG.md) for the prioritized milestones (M1–M5).

## Links

- This repo: [README](./README.md) · [docs/REHOSTING.md](./docs/REHOSTING.md)
- Design docs: [IDEA](./docs/IDEA.md) · [ARCHITECTURE](./docs/ARCHITECTURE.md) ·
  [FLOW](./docs/FLOW.md) · [JOURNEY](./docs/JOURNEY.md) ·
  [STRATEGY](./docs/STRATEGY.md) · [BACKLOG](./docs/BACKLOG.md)
- Monorepo: [skytrack-oss](../) · [OSS-STRATEGY](../OSS-STRATEGY.md)
- Research: [Firmware-Analysis-Papers](../../README.md)

## Refresh checklist (before starting or clearing a session)

1. Re-read this file, [`README.md`](./README.md),
   [`docs/REHOSTING.md`](./docs/REHOSTING.md), and [`docs/BACKLOG.md`](./docs/BACKLOG.md).
2. Confirm you're on branch `claude/skytrack-oss-ideas-0ivndv`.
3. Smoke test: `python harness/rehost.py` and `python fuzzer/mavlink_fuzzer.py -n 5000`.
