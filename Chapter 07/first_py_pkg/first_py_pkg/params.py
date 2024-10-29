import rclpy
from rclpy.node import Node

class NodeWithParams(Node):

    def __init__(self):
        super().__init__('NodeWithParams')
        self.declare_parameter('param_waypoint', 'Charging Station')

        self.timer = self.create_timer(1, self.timer_callback)
 

    def timer_callback(self):
        waypoint_name = self.get_parameter('param_waypoint').value

        self.get_logger().info('waypoint param value %s' % waypoint_name)

        

     

def main(args=None):
    rclpy.init(args=args)
    node = NodeWithParams()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()