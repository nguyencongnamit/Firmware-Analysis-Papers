"""Drone HAL: speaks to a flight stack via sn360-bridge (MAVLink / ROS 2).

This is a stub that documents the binding. In a real deployment it would wrap the
`sn360-bridge` client: read MAVLink LOCAL_POSITION_NED / ATTITUDE for sensing and
send SET_POSITION_TARGET_LOCAL_NED for velocity setpoints. Until that transport
is wired, it falls back to the kinematic SimHAL so examples run anywhere.
"""
from __future__ import annotations

from core.types import Command, Goal, Observation

from .sim_hal import SimHAL


class DroneHAL(SimHAL):
    """Multirotor body. Tighter speed envelope than the generic sim body."""

    def __init__(self, start=(0.0, 0.0, 0.0), endpoint: str | None = None):
        super().__init__(start=start, dt=0.05, max_speed=12.0)
        self.endpoint = endpoint  # e.g. "udp:127.0.0.1:14540" for PX4 SITL via sn360-bridge
        # TODO: when endpoint is set, replace SimHAL integration with a
        # sn360-bridge MAVLink client (heartbeat, OFFBOARD, setpoints).

    def read_sensors(self) -> Observation:  # noqa: D401 - see TODO above
        return super().read_sensors()

    def send_commands(self, commands: list[Command]) -> None:
        super().send_commands(commands)

    def goal_reached(self, goal: Goal) -> bool:
        return super().goal_reached(goal)
