import rclpy
from rclpy.node import Node
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from functools import partial
from my_interfaces.srv import StatsService



class CmdSubscriber(Node):

    def __init__(self):
        super().__init__("cmd_subscriber")
        self.declare_parameters(
            namespace='',
            parameters=[
                ('rosCmdTopic','ros_cmd')
            ]
        )
        self.rosCmdTopic = self.get_parameter("rosCmdTopic").value
        self.subscriber = self.create_subscription(String, self.rosCmdTopic, self.subs_callback, 10)
        self.get_logger().info("Subscribed to order topic")


    def subs_callback(self, message):
        self.get_logger().info('In CmdSubscriber callback')
        self.get_logger().info(message.data)
        #Call service for publishing data
        self.call_stats_svc(True, message.data)


    def call_stats_svc(self, publish, payload):
        client = self.create_client(StatsService, "cmd_srv")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for Stats Service ...")

        request = StatsService.Request()
        request.publish = publish
        request.payload = payload

        future = client.call_async(request)
        future.add_done_callback(
            partial(self.callback_call_stats_srv, publish=publish, payload=payload))

    def callback_call_stats_srv(self, future, publish, payload):
        try:
            response = future.result()
            self.get_logger().info(str(publish) + " + " +
                                   str(payload) + " = " + str(response.output))
        except Exception as e:
            self.get_logger().error("Stats Service call failed %r" % (e,))
    


     

def main(args=None):
    rclpy.init(args=args)
    cmd_subs = CmdSubscriber()
 
    rclpy.spin(cmd_subs)

    rclpy.shutdown()

if __name__ == "__main__":
    main()