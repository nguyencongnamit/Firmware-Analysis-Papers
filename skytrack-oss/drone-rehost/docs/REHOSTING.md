# Rehosting notes

## Goal

Run flight-controller firmware on commodity hardware (no flight rig) so it can be
analyzed, fuzzed, and driven from simulation as a software-in-the-loop target.

## How it works

```
   firmware.elf
        │  boots under
        ▼
   qemu-system-arm  ──MMIO fault──▶  harness/rehost.py : MmioBus
   (Cortex-M)                              │  dispatches to
                                           ▼
                              peripherals/  IMU · GPS · ESC · ...
                                           │  ground truth from
                                           ▼
                              sim / scenario  (the oracle)
```

Unmodeled MMIO reads return 0 and are logged (P2IM style) so firmware keeps
making progress instead of trapping. You then promote the most-hit unmodeled
addresses into real peripheral models until the main control loop runs.

## Lineage

This follows the rehosting literature collected in the parent
[Firmware-Analysis-Papers](../../../README.md): HALucinator (abstraction-layer
emulation), P2IM (automatic peripheral interface modeling), Para-rehosting,
Avatar, FirmAE. `drone-rehost` applies those ideas specifically to drone/robot
flight firmware.

## Try it without QEMU

The MMIO dispatch is pure Python and self-tests standalone:

```bash
cd skytrack-oss/drone-rehost
python harness/rehost.py          # MMIO bus self-test
python fuzzer/mavlink_fuzzer.py -n 5000   # mutation-fuzz the toy parser
```

## With QEMU

```bash
./harness/run_qemu.sh path/to/firmware.elf netduinoplus2
# then attach a gdb/Unicorn MMIO hook that calls MmioBus.read/write
```

## Second target

The harness is not drone-specific. A ground robot's firmware (e.g. an Anki
Vector rebuild) is a natural second target — supporting both proves the toolchain
is general.

## Scale this up

Continuous, scaled fuzzing with a high-fidelity oracle and curated findings →
**sn360**.
