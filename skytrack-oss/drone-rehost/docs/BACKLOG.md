# BACKLOG — drone-rehost

Prioritized milestones. Honest about scaffold state: today only the pure-Python
`MmioBus` self-test and the toy-target fuzzer actually run; full QEMU rehosting and
real-firmware fuzzing are **not yet built**.

## Current state (done)

- [x] `Peripheral` ABC (`handles` / `read` / `write` / `tick`) — `peripherals/base.py`
- [x] IMU model (MPU-6000-class, `WHO_AM_I 0x68`, `set_truth`) — `peripherals/imu.py`
- [x] GPS model (UBX NAV-PVT, `fix_ok` GPS-denied toggle) — `peripherals/gps.py`
- [x] ESC model (per-channel PWM duty, `throttle()`) — `peripherals/esc.py`
- [x] `MmioBus` dispatch + P2IM-style unmodeled logging + self-test — `harness/rehost.py`
- [x] QEMU boot scaffold (Cortex-M + gdb stub) — `harness/run_qemu.sh`
- [x] MAVLink mutation fuzzer against the `toy_parse` target — `fuzzer/mavlink_fuzzer.py`
- [x] Seed corpus: heartbeat, sys_status, param_request — `corpus/*.bin`

## M1 — Wire the MMIO hook into QEMU

Connect the (working) `MmioBus` to a live emulator. **The missing link for real rehosting.**

- [ ] gdb-Python or Unicorn script that catches MMIO access faults and calls
      `MmioBus.read/write(addr, width)`.
- [ ] Feed serviced values back to the faulting load/store and resume execution.
- [ ] Surface the `unhandled` list as a ranked "addresses to model next" report.
- [ ] Document the attach step in `run_qemu.sh` / [REHOSTING.md](./REHOSTING.md).

## M2 — Bring a real firmware image to the main loop

- [ ] Boot a PX4 / ArduPilot-class Cortex-M image under QEMU.
- [ ] Iterate the P2IM loop: promote hot unmodeled addresses into models until the
      sensor/control main loop runs.
- [ ] Extend `default_peripherals()` as needed (clocks, UART, timers, barometer).
- [ ] Capture a reproducible bring-up recipe for at least one public image.

## M3 — Fuzz a real rehosted MAVLink parser

- [ ] Replace `toy_parse` with a bridge to the **rehosted firmware** MAVLink parser.
- [ ] Crash triage: dedup by crash site, classify exception/fault type.
- [ ] Crash **minimization** (shrink the offending input).
- [ ] Auto-add minimized crashes back to `corpus/` as regression seeds.
- [ ] Optional: coverage feedback (greybox) to guide mutation.

## M4 — Sim/scenario oracle as ground truth

- [ ] Drive `IMU.set_truth(accel, gyro)` and `GPS.fix_ok` from a live sim/scenario.
- [ ] Read back ESC `duty` / `throttle()` so the oracle can close the loop.
- [ ] Use the oracle to judge "interesting" beyond crash-only (e.g. motor_loss /
      GPS-denied behavior, divergence from expected trajectory).
- [ ] (Funnel) hi-fidelity oracle + scaled continuous fuzzing live in **sn360**.

## M5 — Ground-robot second target

- [ ] Bring up a ground-robot (Anki Vector rebuild) firmware image with the same harness.
- [ ] Add any robot-specific peripheral models; reuse the bus and bring-up loop.
- [ ] Document it as the "toolchain is general" proof point for talks/write-ups.
- [ ] Keep it a *second target*, not a parallel product (drone stays the focus).

---

Resume here. See [CLAUDE.md](../CLAUDE.md) for status, [ARCHITECTURE](./ARCHITECTURE.md)
for the design, and [STRATEGY](./STRATEGY.md) for the open-vs-sn360 split.
