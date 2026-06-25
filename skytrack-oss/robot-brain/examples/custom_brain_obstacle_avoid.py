"""Build-your-own-brain example: obstacle avoidance in ~15 lines of real logic.

Shows the `Brain` seam (see docs/EXTENDING.md): subclass ReferenceBrain, reuse
its waypoint planner, and add a dodge when a forward range sensor sees something.
A tiny HAL subclass injects a virtual obstacle so the avoidance visibly triggers
— no engine or hardware needed.

    cd skytrack-oss/robot-brain
    python examples/custom_brain_obstacle_avoid.py
"""
from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from adapters import GroundRobotHAL  # noqa: E402
from core import Goal, ReferenceBrain, run  # noqa: E402
from core.types import Command, CommandKind, Observation, Plan, WorldState  # noqa: E402

SAFE_RANGE = 2.5  # m: closer than this ahead -> dodge


class ObstacleAvoidBrain(ReferenceBrain):
    """Reuses the waypoint planner; steers around a close forward obstacle."""

    def perceive(self, obs: Observation) -> WorldState:
        state = super().perceive(obs)
        # carry the range reading through into notes so plan() can use it
        return WorldState(
            t=state.t, position=state.position, velocity=state.velocity,
            heading=state.heading, localization_ok=state.localization_ok,
            notes={**state.notes, "front_range": obs.extras.get("front_range", 999.0)},
        )

    def plan(self, state: WorldState, goal: Goal) -> Plan:
        front = state.notes.get("front_range", 999.0)
        if front < SAFE_RANGE:
            # dodge laterally (in +Y) until the path is clear
            return Plan([Command(CommandKind.VELOCITY, value=(0.0, 1.2, 0.0))],
                        f"obstacle at {front:.1f} m — dodging")
        return super().plan(state, goal)


class RangeSimHAL(GroundRobotHAL):
    """Ground robot with a virtual obstacle and a forward range sensor."""

    def __init__(self, obstacle=(3.0, 0.0, 0.0), **kw):
        super().__init__(**kw)
        self.obstacle = obstacle

    def read_sensors(self) -> Observation:
        obs = super().read_sensors()
        d = math.dist(self.position, self.obstacle)
        return Observation(
            t=obs.t, position=obs.position, velocity=obs.velocity,
            attitude=obs.attitude, gps_ok=obs.gps_ok, imu_ok=obs.imu_ok,
            extras={"front_range": d},
        )


if __name__ == "__main__":
    hal = RangeSimHAL(start=(0, 0, 0), obstacle=(3.0, 0.0, 0.0))
    ok = run(ObstacleAvoidBrain(), hal, [Goal("goto", target=(6, 0, 0), speed=1.2)],
             max_steps=4000)
    final = tuple(round(p, 1) for p in hal.position)
    dodged = abs(hal.position[1]) > 0.3  # did it leave the straight line?
    print(f"[obstacle-avoid] reached={ok}  final={final}  dodged_sideways={dodged}")
    raise SystemExit(0 if dodged else 1)
