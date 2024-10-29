import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class FirstListener(Node):

    def __init__(self):
        super().__init__("FirstListener")
        self.counter_ = 0
        self.subscriber = self.create_subscription(String, "GreetingTopic", self.callback_greeting, 10)
        self.get_logger().info("Subscribed to GreetingTopic topic")

    def callback_greeting(self, message):
        self.get_logger().info(message.data)
     

def main(args=None):
    rclpy.init(args=args)
    node = FirstListener()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()