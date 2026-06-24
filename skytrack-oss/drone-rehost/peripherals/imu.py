"""IMU peripheral model (MPU-6000-class), simplified.

Returns a plausible WHO_AM_I, a 'data ready' status bit, and synthetic
accel/gyro samples so the flight stack's sensor thread makes progress instead of
spinning on a missing device.
"""
from __future__ import annotations

import math

from .base import Peripheral

REG_WHO_AM_I = 0x75
REG_STATUS = 0x3A
REG_ACCEL_XOUT_H = 0x3B
WHO_AM_I_VALUE = 0x68


class IMU(Peripheral):
    def __init__(self, base: int = 0x4000_4000, size: int = 0x100):
        super().__init__("imu", base, size)
        self._t = 0.0
        self._accel = (0.0, 0.0, 9.81)  # m/s^2, at rest
        self._gyro = (0.0, 0.0, 0.0)

    def set_truth(self, accel, gyro) -> None:
        """A scenario/sim feeds ground truth here; reads quantize it."""
        self._accel, self._gyro = accel, gyro

    def read(self, offset: int, width: int) -> int:
        if offset == REG_WHO_AM_I:
            return WHO_AM_I_VALUE
        if offset == REG_STATUS:
            return 0x01  # data ready
        if offset >= REG_ACCEL_XOUT_H:
            # 16-bit big-endian samples; add a little dither for fuzzing realism.
            idx = (offset - REG_ACCEL_XOUT_H) // 2
            raw = self._sample(idx)
            return (raw >> 8) & 0xFF if (offset - REG_ACCEL_XOUT_H) % 2 == 0 else raw & 0xFF
        return 0

    def write(self, offset: int, value: int, width: int) -> None:
        pass  # config registers accepted and ignored

    def tick(self, t: float) -> None:
        self._t = t

    def _sample(self, idx: int) -> int:
        vals = (*self._accel, 0, *self._gyro)  # accel xyz, temp, gyro xyz
        v = vals[idx] if idx < len(vals) else 0.0
        dither = math.sin(self._t * 50 + idx) * 0.01
        return int((v + dither) * 100) & 0xFFFF
