import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class FirstPublisher(Node):

    def __init__(self):
        super().__init__("FirstPublisher")
        self.counter_ = 0
        self.publisher = self.create_publisher(String, "GreetingTopic", 10)
        self._timer = self.create_timer(0.5, self.publish_greeting)
        self.get_logger().info("publishing message")

    def publish_greeting(self):
        msg = String()
        msg.data = "Hello World"
        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = FirstPublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()