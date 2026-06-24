"""A pure-Python kinematic HAL: no engine, no hardware.

This is the cheap testbed body. It integrates velocity commands with a fixed
timestep so you can exercise a brain end-to-end in milliseconds. The drone and
ground-robot HALs share this math and add body-specific limits / transport.
"""
from __future__ import annotations

import math

from core.brain import HAL
from core.types import Command, CommandKind, Goal, Observation


class SimHAL(HAL):
    def __init__(self, start=(0.0, 0.0, 0.0), dt: float = 0.05, max_speed: float = 8.0):
        self.dt = dt
        self.max_speed = max_speed
        self.t = 0.0
        self.position = list(start)
        self.velocity = [0.0, 0.0, 0.0]
        self.yaw = 0.0
        # Fault injection hooks (set by a scenario runner).
        self.gps_ok = True
        self.imu_ok = True

    def read_sensors(self) -> Observation:
        return Observation(
            t=self.t,
            position=tuple(self.position),
            velocity=tuple(self.velocity),
            attitude=(0.0, 0.0, self.yaw),
            gps_ok=self.gps_ok,
            imu_ok=self.imu_ok,
        )

    def send_commands(self, commands: list[Command]) -> None:
        for cmd in commands:
            if cmd.kind is CommandKind.VELOCITY and cmd.value is not None:
                v = self._clamp(cmd.value)
                self.velocity = list(v)
            elif cmd.kind is CommandKind.TAKEOFF and cmd.value is not None:
                self.position[2] = cmd.value[2]
                self.velocity = [0.0, 0.0, 0.0]
            elif cmd.kind is CommandKind.LAND:
                self.velocity = [0.0, 0.0, -1.0]
            elif cmd.kind is CommandKind.HOLD:
                self.velocity = [0.0, 0.0, 0.0]
        # integrate
        for i in range(3):
            self.position[i] += self.velocity[i] * self.dt
        self.position[2] = max(0.0, self.position[2])
        if any(self.velocity[:2]):
            self.yaw = math.atan2(self.velocity[1], self.velocity[0])
        self.t += self.dt

    def goal_reached(self, goal: Goal) -> bool:
        if goal.kind == "hover" and goal.deadline is not None:
            return self.t >= goal.deadline
        if goal.target is None:
            return True
        return math.dist(self.position, goal.target) <= 0.5

    def _clamp(self, v):
        speed = math.sqrt(sum(c * c for c in v))
        if speed <= self.max_speed or speed == 0:
            return v
        return tuple(c / speed * self.max_speed for c in v)
