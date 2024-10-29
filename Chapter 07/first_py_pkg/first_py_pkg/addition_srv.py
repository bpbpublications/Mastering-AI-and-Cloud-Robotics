import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts



class AdditionService(Node):

    def __init__(self):
        super().__init__('AdditionService')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.addition_callback)
        self.get_logger().info('AdditionService server has been started...')


    def addition_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(str(request.a) + " + " + str(request.b) + " = " + str(response.sum))

        return response
     

def main(args=None):
    rclpy.init(args=args)
    node = AdditionService()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()

