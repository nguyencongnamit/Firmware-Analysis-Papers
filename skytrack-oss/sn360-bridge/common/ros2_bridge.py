"""ROS 2 bridge node skeleton.

Exposes the engine's robot as a standard ROS 2 node: publishes sensor topics and
subscribes to a velocity command topic. Written so it degrades gracefully when
rclpy isn't installed (prints the shape instead), so the structure is reviewable
without a full ROS 2 toolchain.

Topics:
    pub   /sn360/imu          sensor_msgs/Imu
    pub   /sn360/odom         nav_msgs/Odometry
    sub   /sn360/cmd_vel      geometry_msgs/Twist
"""
from __future__ import annotations

try:
    import rclpy
    from rclpy.node import Node
    HAVE_ROS2 = True
except ImportError:  # pragma: no cover
    HAVE_ROS2 = False
    Node = object  # type: ignore


class Sn360BridgeNode(Node):
    """Bridges a Unity/Unreal scene <-> ROS 2 graph."""

    def __init__(self):
        if HAVE_ROS2:
            super().__init__("sn360_bridge")
            self._declare_io()
        self._latest_cmd = (0.0, 0.0, 0.0)

    def _declare_io(self) -> None:
        from geometry_msgs.msg import Twist
        from nav_msgs.msg import Odometry
        from sensor_msgs.msg import Imu
        self.pub_imu = self.create_publisher(Imu, "/sn360/imu", 10)
        self.pub_odom = self.create_publisher(Odometry, "/sn360/odom", 10)
        self.sub_cmd = self.create_subscription(Twist, "/sn360/cmd_vel", self._on_cmd, 10)

    def _on_cmd(self, msg) -> None:
        self._latest_cmd = (msg.linear.x, msg.linear.y, msg.linear.z)
        # Engine plugin polls latest_cmd() each tick and applies it to the body.

    def latest_cmd(self) -> tuple[float, float, float]:
        return self._latest_cmd

    # publish_* would be called by the engine each sim tick with real sensor data.


def main() -> None:
    if not HAVE_ROS2:
        print("rclpy not installed — node shape only.\n"
              "  pub  /sn360/imu, /sn360/odom\n"
              "  sub  /sn360/cmd_vel")
        return
    rclpy.init()
    node = Sn360BridgeNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
