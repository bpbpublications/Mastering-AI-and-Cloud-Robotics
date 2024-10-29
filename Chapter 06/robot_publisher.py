import rospy 
from std_msgs.msg import String 
import paho.mqtt.client as mqtt 
 
# Initialization publisher ROS Node rospy.init_node('robot_publisher', anonymous=True) 
 
# MQTT Configurations 
mqtt_broker_address = 127.0.0.1 
mqtt_broker_port = 1883 
mqtt_topic = "robot_data" 
 
# ROS Callback for Data 
def data_callback(data): 
    payload = data.data 
    mqtt_client.publish(mqtt_topic, payload) 
 
# ROS Subscriber 
rospy.Subscriber("data_topic", String, data_callback) 
 
# MQTT Client Initialization 
mqtt_client = mqtt.Client() 
mqtt_client.connect(mqtt_broker_address, mqtt_broker_port) 
 
# ROS Spin 
rospy.spin() 