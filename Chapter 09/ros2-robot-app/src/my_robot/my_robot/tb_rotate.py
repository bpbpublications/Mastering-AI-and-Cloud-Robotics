#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TBRotateNode (Node):

    def __init__ (self):
        super ().__init__ ("tb_rotate")
        self.cmv_vel_pub_ = self.create_publisher (Twist, "/turtle1/cmd_vel", 10)
        self.timer_ = self.create_timer (0.5, self.rotate_callback)
        self.get_logger ().info ("Turtle roatation started!")

    def rotate_callback (self):
        msg = Twist ()
        msg.linear.x = 1.0
        msg.angular.z = 0.5
        self.cmv_vel_pub_.publish (msg)

def main (args = None):
    rclpy.init (args = args)
    node = TBRotateNode ()
    rclpy.spin (node)
    rclpy.shutdown ()
