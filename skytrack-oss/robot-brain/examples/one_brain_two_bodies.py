"""One brain, two bodies.

Runs the *same* ReferenceBrain through a drone HAL and a ground-robot HAL,
proving the brain is body-agnostic. No engine or hardware required.

    cd skytrack-oss/robot-brain
    python examples/one_brain_two_bodies.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from adapters import DroneHAL, GroundRobotHAL  # noqa: E402
from core import Goal, ReferenceBrain, run  # noqa: E402


def fly_drone() -> bool:
    brain = ReferenceBrain()
    hal = DroneHAL(start=(0, 0, 0))
    goals = [
        Goal("takeoff", target=(0, 0, 20)),
        Goal("goto", target=(50, 0, 20), speed=8),
        Goal("goto", target=(50, 40, 20), speed=8),
        Goal("land", target=(50, 40, 0)),
    ]
    ok = run(brain, hal, goals)
    print(f"[drone]  reached goals={ok}  final={tuple(round(p, 1) for p in hal.position)}")
    return ok


def drive_rover() -> bool:
    brain = ReferenceBrain()  # SAME brain class
    hal = GroundRobotHAL(start=(0, 0, 0))
    goals = [
        Goal("goto", target=(5, 0, 0), speed=1.2),
        Goal("goto", target=(5, 3, 0), speed=1.2),
    ]
    ok = run(brain, hal, goals)
    print(f"[rover]  reached goals={ok}  final={tuple(round(p, 1) for p in hal.position)}")
    return ok


if __name__ == "__main__":
    results = [fly_drone(), drive_rover()]
    raise SystemExit(0 if all(results) else 1)
