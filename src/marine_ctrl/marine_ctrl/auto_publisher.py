import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


class AutoTwistPublisher(Node):
    def __init__(self):
        super().__init__("marine_ctrl_auto")
        self.declare_parameter("topic", "/cmd_vel")
        self.declare_parameter("forward", 0.5)
        self.declare_parameter("rate_hz", 1.0)

        topic = self.get_parameter("topic").value
        self.forward = self.get_parameter("forward").value
        rate_hz = self.get_parameter("rate_hz").value

        self.pub = self.create_publisher(Twist, topic, 10)
        self.timer = self.create_timer(1.0 / rate_hz, self.tick)
        self.count = 0
        self.get_logger().info(
            f"publishing Twist(forward={self.forward}) on '{topic}' at {rate_hz} Hz"
        )

    def tick(self):
        msg = Twist()
        msg.linear.x = self.forward
        self.pub.publish(msg)
        self.count += 1
        if self.count % 5 == 0:
            self.get_logger().info(f"published {self.count} messages")


def main():
    rclpy.init()
    node = AutoTwistPublisher()
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
