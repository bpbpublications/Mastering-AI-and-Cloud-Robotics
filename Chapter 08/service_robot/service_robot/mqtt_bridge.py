import json
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from awscrt import mqtt, io
from awsiot import mqtt_connection_builder


class MqttBridge(Node):
    def __init__(self):
        super().__init__('mqtt_bridge')
        self.declare_parameters(
            namespace='',
            parameters=[
                ('endpoint', ''),
                ('port', 8883),
                ('rootCAPath', ''),
                ('certificatePath', ''),
                ('privateKeyPath', ''),
                ('clientID', 'service-robot'),
                ('region', 'ap-south-1'),
                ('statsTopic', 'robot/service_robot/data'),
                ('cmdSubsTopic', 'robot/service_robot/order')
            ]
        )

        cloud_sub_topic = self.get_parameter("cmdSubsTopic").value

        retries = 0
        connected = False
        max_retries = 3

        while retries < max_retries:
            try:
                self.get_logger().info("Connecting to cloud endpoint")
                self.connect_to_cloud()
                connected = True
                break
            except Exception as e:
                self.get_logger().error(f'Connection Error: {e}.')


        if connected:
            
            # Subscribe to Cloud Command outbound topic
            self.subscribe_future, self.packet_id = self.mqtt_conn.subscribe(
                topic=cloud_sub_topic,
                qos=mqtt.QoS.AT_LEAST_ONCE,
                callback=self.on_message_received
            )

        else:
            self.get_logger().error('Failed to connect to MQTT broker, ending retries.')


        self.init_ros_subscriptions()
        self.init_ros_publishers('ros_cmd')



    def connect_to_cloud(self):
        self.mqtt_conn = mqtt_connection_builder.mtls_from_path(
            endpoint=self.get_parameter("endpoint").value,
            port=self.get_parameter("port").value,
            cert_filepath= self.get_parameter("certificatePath").value,
            pri_key_filepath= self.get_parameter("privateKeyPath").value,
            ca_filepath= self.get_parameter("rootCAPath").value,
            on_connection_interrupted=self.on_connection_interrupted,
            on_connection_resumed=self.on_connection_resumed,
            client_id= self.get_parameter("clientID").value,
            clean_session=False,
            keep_alive_secs=6,
            http_proxy_options=None
        )
        connected_future = self.mqtt_conn.connect()
        connected_future.result()
        self.get_logger().info("Connected!")

 

    def init_ros_subscriptions(self):
        """Subscribe to ros2 stats topic"""
        self.subscription = self.create_subscription(
            String,
            'ros_stats_topic',
            self.stats_callback,
            10
        )

    def stats_callback(self, msg):
        """Callback for the ros2 stats topic"""
        message_json = msg.data
        self.get_logger().info("Received data on ROS2 {}\nPublishing to cloud".format(msg.data))
        self.mqtt_conn.publish(
            topic=self.get_parameter("statsTopic").value,
            payload=message_json,
            qos=mqtt.QoS.AT_LEAST_ONCE
        )

    def init_ros_publishers(self,ros_topic):
        # ROS 2 publisher 
         global ros_publisher
         ros_publisher = self.create_publisher(String, ros_topic, 10)



    def on_message_received(self, topic, payload, **kwargs):
        self.get_logger().info(f"Received message on topic '{topic}': {payload}")

        # Publish the message to a ROS 2 topic
        self.pub_on_ros('ros_cmd', payload)


    def on_connection_interrupted(self, connection, error, **kwargs):
        self.get_logger().info(f"Cloud connection interrupted: {error}")


    def on_connection_resumed(self, connection, return_code, session_present, **kwargs):
        self.get_logger().info("Cloud connection resumed")

    
    def pub_on_ros(self, ros_topic, payload):
         self.get_logger().info(f"Publishing on ros topic '{ros_topic} ")
         json_data = json.loads(payload)         

         msg = String()
         msg.data = json.dumps(json_data)
         ros_publisher.publish(msg)





def main(args=None):
    rclpy.init(args=args)

    mqtt_bridge = MqttBridge()


    rclpy.spin(mqtt_bridge)
    mqtt_bridge.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

