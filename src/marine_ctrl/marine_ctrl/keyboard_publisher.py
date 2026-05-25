"""Keyboard teleop: w/s fwd/rev, a/d yaw, r/f up/down, space stop, q quit."""

import os
import select
import sys
import termios
import time
import tty

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node

LINEAR = 0.5
ANGULAR = 0.5
PUBLISH_HZ = 20.0
KEY_TIMEOUT_SEC = 0.3


class KeyboardTwistPublisher(Node):
    def __init__(self):
        super().__init__("marine_ctrl_keyboard")
        self.declare_parameter("topic", "/cmd_vel")
        topic = self.get_parameter("topic").value

        self.pub = self.create_publisher(Twist, topic, 10)
        self.cmd = Twist()
        self.last_key_time = 0.0

        self.fd = sys.stdin.fileno() if sys.stdin.isatty() else None
        self.old_term = termios.tcgetattr(self.fd) if self.fd is not None else None
        if self.fd is not None:
            tty.setcbreak(self.fd)
        else:
            self.get_logger().warn("No TTY; keyboard input disabled.")

        self.timer = self.create_timer(1.0 / PUBLISH_HZ, self.on_timer)
        self.get_logger().info(f"keyboard teleop on '{topic}'")

    def destroy_node(self):
        if self.fd is not None and self.old_term is not None:
            try:
                termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_term)
            except Exception:
                pass
        super().destroy_node()

    def read_key(self):
        if self.fd is None:
            return None
        if select.select([self.fd], [], [], 0.0)[0]:
            raw = os.read(self.fd, 1)
            if raw:
                try:
                    return raw.decode("utf-8")
                except UnicodeDecodeError:
                    return None
        return None

    def on_timer(self):
        key = self.read_key()
        now = time.time()

        if key is not None:
            self.last_key_time = now
            self.cmd = Twist()

            if key == "q":
                self.pub.publish(self.cmd)
                rclpy.shutdown()
                return
            elif key == "w": self.cmd.linear.x = LINEAR
            elif key == "s": self.cmd.linear.x = -LINEAR
            elif key == "a": self.cmd.angular.z = ANGULAR
            elif key == "d": self.cmd.angular.z = -ANGULAR
            elif key == "r": self.cmd.linear.z = LINEAR
            elif key == "f": self.cmd.linear.z = -LINEAR

        if now - self.last_key_time > KEY_TIMEOUT_SEC:
            self.cmd = Twist()

        self.pub.publish(self.cmd)


def main():
    rclpy.init()
    node = KeyboardTwistPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
