"""Rehosting harness: route emulated MMIO to peripheral models.

This is the core dispatch the QEMU bridge calls on every unhandled MMIO access.
It's engine-independent and fully testable without QEMU: `MmioBus` is exactly
what a Unicorn/QEMU hook would invoke. `run_qemu.sh` wires this into QEMU; the
self-test at the bottom exercises it directly.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from peripherals import Peripheral, default_peripherals  # noqa: E402


class MmioBus:
    """Dispatches MMIO reads/writes to the peripheral that owns the address."""

    def __init__(self, peripherals: list[Peripheral] | None = None):
        self.peripherals = peripherals or default_peripherals()
        self.unhandled: list[tuple[str, int]] = []

    def _find(self, addr: int) -> Peripheral | None:
        for p in self.peripherals:
            if p.handles(addr):
                return p
        return None

    def read(self, addr: int, width: int = 1) -> int:
        p = self._find(addr)
        if p is None:
            self.unhandled.append(("read", addr))
            return 0  # P2IM-style: return 0 for unmodeled reads, keep firmware moving
        return p.read(addr - p.base, width)

    def write(self, addr: int, value: int, width: int = 1) -> None:
        p = self._find(addr)
        if p is None:
            self.unhandled.append(("write", addr))
            return
        p.write(addr - p.base, value, width)

    def tick(self, t: float) -> None:
        for p in self.peripherals:
            p.tick(t)


def _selftest() -> int:
    bus = MmioBus()
    # IMU WHO_AM_I should read back the expected id through the bus.
    who = bus.read(0x4000_4000 + 0x75)
    assert who == 0x68, f"unexpected WHO_AM_I: {who:#x}"
    # ESC: write throttle, read it back as commanded duty.
    bus.write(0x4000_6000 + 0x00, 1500)
    assert bus.read(0x4000_6000 + 0x00) == 1500
    # Unmodeled address is recorded, not crashed.
    bus.read(0xDEAD_BEEF)
    assert ("read", 0xDEAD_BEEF) in bus.unhandled
    print("rehost MMIO bus self-test: OK")
    print(f"  peripherals: {[p.name for p in bus.peripherals]}")
    print(f"  unhandled accesses: {len(bus.unhandled)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_selftest())
