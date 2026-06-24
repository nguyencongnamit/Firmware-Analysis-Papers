"""A small, dependency-free reference brain.

It does dead-reckoning perception and a proportional waypoint planner. It is
deliberately simple: the point is to show the contract, not to be a good
controller. Swap in a VLM perceiver / LLM planner behind the same interface for
the sn360-grade brain.
"""
from __future__ import annotations

import math

from .brain import Brain
from .types import Command, CommandKind, Goal, Observation, Plan, WorldState


def _dist(a, b) -> float:
    return math.dist(a, b)


class ReferenceBrain(Brain):
    def __init__(self, arrive_radius: float = 0.5):
        self.arrive_radius = arrive_radius

    def perceive(self, obs: Observation) -> WorldState:
        # If GPS dropped, flag degraded localization but keep flying on inertial.
        return WorldState(
            t=obs.t,
            position=obs.position,
            velocity=obs.velocity,
            heading=obs.attitude[2],
            localization_ok=obs.gps_ok and obs.imu_ok,
            notes={"gps_ok": obs.gps_ok, "imu_ok": obs.imu_ok},
        )

    def plan(self, state: WorldState, goal: Goal) -> Plan:
        if goal.kind == "takeoff":
            return Plan([Command(CommandKind.TAKEOFF, value=goal.target)], "takeoff")
        if goal.kind == "land":
            return Plan([Command(CommandKind.LAND, value=goal.target)], "land")
        if goal.kind == "hover":
            return Plan([Command(CommandKind.HOLD)], "hold position")

        # goto / follow: proportional velocity toward the target, capped at goal.speed.
        assert goal.target is not None
        dx = tuple(t - p for t, p in zip(goal.target, state.position))
        d = math.sqrt(sum(c * c for c in dx)) or 1.0
        speed = min(goal.speed, d)  # ease in as we approach
        vel = tuple(c / d * speed for c in dx)
        slow = " (localization degraded)" if not state.localization_ok else ""
        return Plan([Command(CommandKind.VELOCITY, value=vel, speed=speed)],
                    f"steer toward {goal.target}{slow}")

    def act(self, plan: Plan) -> list[Command]:
        # Reference brain plans directly in actuator terms, so this is a pass-through.
        return list(plan.intents)
