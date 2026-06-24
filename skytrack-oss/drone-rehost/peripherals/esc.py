"""ESC / motor-output peripheral model.

Models a timer/PWM block: firmware writes duty-cycle (throttle) per channel; the
model latches them so a sim/oracle can read back commanded motor outputs and
close the loop (or detect a motor_loss fault injection).
"""
from __future__ import annotations

from .base import Peripheral

NUM_CHANNELS = 8
REG_CH0_DUTY = 0x00  # 4 bytes per channel


class ESC(Peripheral):
    def __init__(self, base: int = 0x4000_6000, size: int = 0x100):
        super().__init__("esc", base, size)
        self.duty = [0] * NUM_CHANNELS

    def read(self, offset: int, width: int) -> int:
        ch = offset // 4
        return self.duty[ch] if 0 <= ch < NUM_CHANNELS else 0

    def write(self, offset: int, value: int, width: int) -> None:
        ch = offset // 4
        if 0 <= ch < NUM_CHANNELS:
            self.duty[ch] = value & 0xFFFF

    def throttle(self) -> list[float]:
        """Commanded throttle per channel in [0, 1] (1000-2000us PWM convention)."""
        return [max(0.0, min(1.0, (d - 1000) / 1000)) for d in self.duty]
