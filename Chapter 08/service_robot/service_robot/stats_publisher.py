import rclpy
import json
import random
from rclpy.node import Node
from std_msgs.msg import String
from my_interfaces.srv import StatsService


class StatsPublisher(Node):

    is_publishing = False

    def __init__(self):
        super().__init__('stats_publisher')
        self.declare_parameters(
            namespace='',
            parameters=[
                ('rosCmdTopic','ros_cmd'),
                ('rosStatsTopic','ros_stats_topic')
            ]
        )
        global is_publishing
        self.rosCmdTopic = self.get_parameter("rosCmdTopic").value
        self.rosStatsTopic = self.get_parameter("rosStatsTopic").value
        
        self.stats_pub = self.create_publisher(String,self.rosStatsTopic,10)
        self.timer = None
        self.task_srv = self.create_service(StatsService,'cmd_srv', self.srv_callback)


    def timer_callback(self):
        if self.is_publishing:
            msg = String()
            # Create data and publish various stats data
            stats = {}
            stats["battery"] = round(random.uniform(85, 90), 2)
            stats["velocity"] = round(random.uniform(3, 4), 2)
            msg.data = json.dumps(stats)
            self.stats_pub.publish(msg)
        else:
            self.get_logger().info('stop publishing stats data')


    def srv_callback(self, request, response):
        p_state = ''

        if request.publish:
            self.is_publishing = True
            # create a timer for publishing
            timer_period = 0.5  
            self.timer = self.create_timer(timer_period, self.timer_callback)
            p_state = 'Publishing'

        elif request.publish == False:
             self.get_logger().info('destroying timer')
             self.timer.cancel()
             p_state = 'Stopped'

        else:
            self.get_logger().info('Undefined state....')
            p_state = 'Unknown'
            

        response.output = p_state
        
        return response




def main(args=None):
    rclpy.init(args=args)

    stats_publisher = StatsPublisher()

    rclpy.spin(stats_publisher)

    # Destroy the node
    stats_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
