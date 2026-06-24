"""GPS peripheral model: feeds UBX-style NAV-PVT frames over a UART register.

Enough to satisfy a firmware GPS driver: a readable data register that streams a
canned position fix, plus a status bit. A scenario can flip `fix_ok` to emulate
GPS-denied conditions.
"""
from __future__ import annotations

from .base import Peripheral

REG_STATUS = 0x00
REG_DATA = 0x04


class GPS(Peripheral):
    def __init__(self, base: int = 0x4000_5000, size: int = 0x100):
        super().__init__("gps", base, size)
        self.fix_ok = True
        self._frame = self._ubx_nav_pvt(lat=473977420, lon=85455940, alt=488000)
        self._cursor = 0

    def read(self, offset: int, width: int) -> int:
        if offset == REG_STATUS:
            return 0x01 if self.fix_ok and self._cursor < len(self._frame) else 0x00
        if offset == REG_DATA and self.fix_ok:
            byte = self._frame[self._cursor % len(self._frame)]
            self._cursor += 1
            return byte
        return 0

    def write(self, offset: int, value: int, width: int) -> None:
        if offset == REG_STATUS:
            self._cursor = 0  # firmware acking / resetting the stream

    @staticmethod
    def _ubx_nav_pvt(lat: int, lon: int, alt: int) -> bytes:
        # Minimal UBX header + little-endian lon/lat/height; not checksum-perfect,
        # enough to exercise a parser and as a fuzzing seed.
        body = b"\xb5\x62\x01\x07" + b"\x00" * 24
        body += lon.to_bytes(4, "little", signed=True)
        body += lat.to_bytes(4, "little", signed=True)
        body += alt.to_bytes(4, "little", signed=True)
        return body
