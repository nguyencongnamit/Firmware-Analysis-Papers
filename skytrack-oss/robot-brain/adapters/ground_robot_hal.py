"""Ground-robot HAL: the cheap, safe, indoor testbed body.

Constrains motion to the ground plane (z stays 0) and a slow speed envelope so
the same brain that flies a drone can be iterated harmlessly on a desk robot
(e.g. an Anki Vector rebuild) before deploying to the drone.
"""
from __future__ import annotations

from core.types import Command, CommandKind, Goal, Observation

from .sim_hal import SimHAL


class GroundRobotHAL(SimHAL):
    def __init__(self, start=(0.0, 0.0, 0.0), endpoint: str | None = None):
        super().__init__(start=(start[0], start[1], 0.0), dt=0.05, max_speed=1.5)
        self.endpoint = endpoint  # e.g. Vector SDK / wire-pod, or ROS 2 via sn360-bridge

    def send_commands(self, commands: list[Command]) -> None:
        # Ground robot can't take off or change altitude; flatten any z intent.
        flat: list[Command] = []
        for cmd in commands:
            if cmd.kind in (CommandKind.TAKEOFF, CommandKind.LAND):
                flat.append(Command(CommandKind.HOLD))
            elif cmd.kind is CommandKind.VELOCITY and cmd.value is not None:
                vx, vy, _ = cmd.value
                flat.append(Command(CommandKind.VELOCITY, value=(vx, vy, 0.0), speed=cmd.speed))
            else:
                flat.append(cmd)
        super().send_commands(flat)
        self.position[2] = 0.0

    def read_sensors(self) -> Observation:
        return super().read_sensors()

    def goal_reached(self, goal: Goal) -> bool:
        return super().goal_reached(goal)
