import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
import time

from my_interfaces.action import Countdown

class CountdownServer(Node):
        """CountdownServer is an action server that accepts a goal, 
        send goal response and can send feedback on request."""
	
        def __init__(self):
            super().__init__("CountdownServer")
            self._action_server = ActionServer(
                self,
                Countdown,
                "countdown",
                self.action_server_callback)
        

        def action_server_callback(self, goal_handle):
            self.get_logger().info("Starting countdown...")

            cd_feedback = Countdown.Feedback()

            # Get the number as the starting number for countdown request 
            cd_feedback.current_num = goal_handle.request.starting_num

            while cd_feedback.current_num > 0:
                # Decrement current number by 1 for the feedback
                cd_feedback.current_num = cd_feedback.current_num - 1

                self.get_logger().info('Feedback:{0}'.format(cd_feedback.current_num))
                goal_handle.publish_feedback(cd_feedback)

                # Sleep a second before the next number count
                time.sleep(1)

            goal_handle.succeed()
            result = Countdown.Result()
            result.is_finished = True
            return result
    
    
def main(args=None):
	rclpy.init(args=args)
	cd_server = CountdownServer()
	rclpy.spin(cd_server)


if __name__ == '__main__':
	main()