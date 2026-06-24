"""The brain contract and the run loop.

Write the brain once (perceive -> plan -> act); implement a HAL per body. The
loop below is body-agnostic: swap the HAL, keep the brain.
"""
from __future__ import annotations

import abc

from .types import Command, Goal, Observation, Plan, WorldState


class Brain(abc.ABC):
    """Body-agnostic autonomy. Subclass and implement the three phases."""

    @abc.abstractmethod
    def perceive(self, obs: Observation) -> WorldState:
        """Turn raw sensor data into a world-state estimate."""

    @abc.abstractmethod
    def plan(self, state: WorldState, goal: Goal) -> Plan:
        """Decide what to do given the state and the current goal."""

    @abc.abstractmethod
    def act(self, plan: Plan) -> list[Command]:
        """Lower a plan into actuator commands."""


class HAL(abc.ABC):
    """Hardware-abstraction layer. One implementation per body."""

    @abc.abstractmethod
    def read_sensors(self) -> Observation: ...

    @abc.abstractmethod
    def send_commands(self, commands: list[Command]) -> None: ...

    @abc.abstractmethod
    def goal_reached(self, goal: Goal) -> bool: ...


def run(brain: Brain, hal: HAL, goals: list[Goal], *, max_steps: int = 10_000) -> bool:
    """Drive `goals` to completion through `brain` over `hal`.

    Returns True if every goal was reached within `max_steps`.
    """
    for goal in goals:
        steps = 0
        while not hal.goal_reached(goal):
            if steps >= max_steps:
                return False
            obs = hal.read_sensors()
            state = brain.perceive(obs)
            plan = brain.plan(state, goal)
            hal.send_commands(brain.act(plan))
            steps += 1
    return True
