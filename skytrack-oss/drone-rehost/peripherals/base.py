"""Peripheral model interface for rehosting.

A peripheral model answers MMIO reads and absorbs MMIO writes for an emulated
region, standing in for real hardware (IMU, GPS, ESC, ...). This is the P2IM /
HALucinator idea: model just enough of each peripheral to keep firmware out of
fault loops and reach interesting code.
"""
from __future__ import annotations

import abc


class Peripheral(abc.ABC):
    """Models one MMIO-mapped device over [base, base+size)."""

    def __init__(self, name: str, base: int, size: int):
        self.name = name
        self.base = base
        self.size = size

    def handles(self, addr: int) -> bool:
        return self.base <= addr < self.base + self.size

    @abc.abstractmethod
    def read(self, offset: int, width: int) -> int:
        """Return the value firmware should see for an MMIO read."""

    @abc.abstractmethod
    def write(self, offset: int, value: int, width: int) -> None:
        """Absorb an MMIO write (configure registers, latch setpoints, ...)."""

    def tick(self, t: float) -> None:
        """Advance internal state one emulation step (optional)."""
