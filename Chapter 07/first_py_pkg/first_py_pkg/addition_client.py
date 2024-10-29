import rclpy
from rclpy.node import Node
from functools import partial

from example_interfaces.srv import AddTwoInts


class AdditionClient(Node):

    def __init__(self):
        super().__init__("AdditionClient")
        self.call_addition_svc(6, 7)
        self.call_addition_svc(3, 1)
        self.call_addition_svc(5, 2)

    def call_addition_svc(self, a, b):
        client = self.create_client(AddTwoInts, "add_two_ints")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for Addition Service ...")

        request = AddTwoInts.Request()
        request.a = a
        request.b = b

        future = client.call_async(request)
        future.add_done_callback(
            partial(self.callback_call_addition_srv, a=a, b=b))

    def callback_call_addition_srv(self, future, a, b):
        try:
            response = future.result()
            self.get_logger().info(str(a) + " + " +
                                   str(b) + " = " + str(response.sum))
        except Exception as e:
            self.get_logger().error("Addition Service call failed %r" % (e,))


def main(args=None):
    rclpy.init(args=args)
    node = AdditionClient()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()