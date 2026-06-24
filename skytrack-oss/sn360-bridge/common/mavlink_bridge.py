"""Minimal MAVLink bridge core: heartbeat + position/velocity setpoints.

Engine-agnostic. The Unity/Unreal plugins talk to this over a local socket (or
embed an equivalent client). It depends on `pymavlink`, the de-facto MAVLink
library, so it speaks to PX4 / ArduPilot SITL out of the box.

    pip install -r requirements.txt
    python mavlink_bridge.py --endpoint udp:127.0.0.1:14540

Without a reachable endpoint it runs in --dry-run mode and just logs the frames
it would send, so the wiring can be tested with no autopilot present.
"""
from __future__ import annotations

import argparse
import time

try:
    from pymavlink import mavutil
except ImportError:  # pragma: no cover
    mavutil = None

HEARTBEAT_HZ = 1.0


class MavlinkBridge:
    def __init__(self, endpoint: str, dry_run: bool = False):
        self.endpoint = endpoint
        self.dry_run = dry_run or mavutil is None
        self.conn = None

    def connect(self) -> None:
        if self.dry_run:
            print(f"[dry-run] would connect to {self.endpoint}")
            return
        print(f"connecting to {self.endpoint} ...")
        self.conn = mavutil.mavlink_connection(self.endpoint)
        self.conn.wait_heartbeat()
        print(f"heartbeat from system {self.conn.target_system} "
              f"component {self.conn.target_component}")

    def send_heartbeat(self) -> None:
        if self.dry_run:
            print("[dry-run] HEARTBEAT")
            return
        self.conn.mav.heartbeat_send(
            mavutil.mavlink.MAV_TYPE_GCS,
            mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)

    def send_velocity_ned(self, vx: float, vy: float, vz: float) -> None:
        """Body/local velocity setpoint (m/s, NED)."""
        if self.dry_run:
            print(f"[dry-run] SET_POSITION_TARGET_LOCAL_NED vel=({vx},{vy},{vz})")
            return
        # type_mask: ignore position & accel, use velocity (0b0000111111000111)
        self.conn.mav.set_position_target_local_ned_send(
            0, self.conn.target_system, self.conn.target_component,
            mavutil.mavlink.MAV_FRAME_LOCAL_NED,
            0b0000111111000111,
            0, 0, 0, vx, vy, vz, 0, 0, 0, 0, 0)

    def spin(self, duration_s: float = 5.0) -> None:
        """Demo loop: heartbeat + a gentle forward nudge."""
        self.connect()
        t_end = time.monotonic() + duration_s
        next_hb = 0.0
        while time.monotonic() < t_end:
            now = time.monotonic()
            if now >= next_hb:
                self.send_heartbeat()
                next_hb = now + 1.0 / HEARTBEAT_HZ
            self.send_velocity_ned(1.0, 0.0, 0.0)
            time.sleep(0.1)


def main() -> None:
    ap = argparse.ArgumentParser(description="sn360-bridge MAVLink core")
    ap.add_argument("--endpoint", default="udp:127.0.0.1:14540")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--seconds", type=float, default=5.0)
    args = ap.parse_args()
    MavlinkBridge(args.endpoint, dry_run=args.dry_run).spin(args.seconds)


if __name__ == "__main__":
    main()
