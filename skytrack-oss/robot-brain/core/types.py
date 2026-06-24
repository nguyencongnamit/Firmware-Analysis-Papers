"""Core data types for the body-agnostic robot brain.

These are deliberately small and serializable so the same brain can run on a
drone, a ground robot, or in pure simulation without code changes.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

Vec3 = tuple[float, float, float]


class CommandKind(str, Enum):
    VELOCITY = "velocity"      # body-frame linear velocity setpoint (m/s)
    GOTO = "goto"              # world-frame position setpoint (m, ENU)
    TAKEOFF = "takeoff"
    LAND = "land"
    HOLD = "hold"


@dataclass(frozen=True)
class Observation:
    """Raw-ish sensor snapshot produced by a HAL."""
    t: float                              # seconds since scenario start
    position: Vec3                        # ENU meters (best estimate)
    velocity: Vec3                        # ENU m/s
    attitude: Vec3                        # roll, pitch, yaw (rad)
    gps_ok: bool = True
    imu_ok: bool = True
    extras: dict = field(default_factory=dict)  # camera frames, ToF, battery, ...


@dataclass(frozen=True)
class WorldState:
    """The brain's interpretation of the world after perception."""
    t: float
    position: Vec3
    velocity: Vec3
    heading: float
    localization_ok: bool
    notes: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Goal:
    """What the agent is currently trying to achieve."""
    kind: str                 # mirrors a mission action: goto / hover / land / ...
    target: Vec3 | None = None
    speed: float = 5.0
    deadline: float | None = None


@dataclass(frozen=True)
class Plan:
    """Planner output: an ordered list of intents to execute."""
    intents: list["Command"]
    rationale: str = ""


@dataclass(frozen=True)
class Command:
    """A single actuator-level command sent through the HAL."""
    kind: CommandKind
    value: Vec3 | None = None
    speed: float = 5.0
