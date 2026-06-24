"""Peripheral models for firmware rehosting."""
from .base import Peripheral
from .esc import ESC
from .gps import GPS
from .imu import IMU

__all__ = ["Peripheral", "IMU", "GPS", "ESC"]


def default_peripherals() -> list[Peripheral]:
    """A minimal flight-controller peripheral set."""
    return [IMU(), GPS(), ESC()]
