#!/usr/bin/env bash
# Launch a flight-controller firmware image under QEMU for rehosting.
#
# This is the bring-up scaffold. It boots a Cortex-M firmware in qemu-system-arm
# and (in the full setup) attaches a gdb/Unicorn MMIO hook that forwards
# unhandled peripheral accesses to harness/rehost.py:MmioBus.
#
# Usage: ./run_qemu.sh <firmware.elf> [machine]
set -euo pipefail

FW="${1:-}"
MACHINE="${2:-netduinoplus2}"   # a common Cortex-M4 board model

if [[ -z "$FW" ]]; then
  echo "usage: $0 <firmware.elf> [qemu-machine]" >&2
  exit 2
fi
if ! command -v qemu-system-arm >/dev/null 2>&1; then
  echo "qemu-system-arm not found. Install QEMU to run rehosting." >&2
  exit 1
fi

echo "[drone-rehost] booting $FW on machine '$MACHINE'"
echo "[drone-rehost] gdb stub on :1234 — attach a peripheral hook to MmioBus"

exec qemu-system-arm \
  -machine "$MACHINE" \
  -cpu cortex-m4 \
  -nographic \
  -kernel "$FW" \
  -S -gdb tcp::1234
# Next step: a gdb/Unicorn script catches MMIO faults and calls
# harness/rehost.py to service them via the peripheral models.
