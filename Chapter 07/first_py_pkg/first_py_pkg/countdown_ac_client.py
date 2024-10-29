import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
import time

from my_interfaces.action import Countdown

class CountdownClient(Node):
        """CountdownClient is an action client that sends a goal to 
        action server for processing and wait for goal result.It uses 
        feedback to get goal progress.
        """
        def __init__(self):
            super().__init__("CountdownClient")
            self._action_client = ActionClient(self, Countdown, "countdown")

            
        def send_goal(self, num):
            cd_goal = Countdown.Goal()
            cd_goal.starting_num = num
            self._action_client.wait_for_server()

            # Get a goal handle
            self._send_goal_future =self._action_client.send_goal_async(cd_goal, feedback_callback=self.feedback_callback)

            # Register a callback for goal response
            self._send_goal_future.add_done_callback(self.goal_callback)

        
        def feedback_callback(self, feedback_msg):
            feedback = feedback_msg.feedback
            self.get_logger().info('Received feedback: {0}'.format(feedback.current_num))

        
        def goal_callback(self, future):
            # Get the goal handle
            goal_handle = future.result()

            if not goal_handle.accepted:
                self.get_logger().info('Goal rejected :')
                return

            self.get_logger().info('Goal accepted :')

            # Use goal handle for getting result
            self._get_result_future = goal_handle.get_result_async()
            self._get_result_future.add_done_callback(self.result_callback)

        def result_callback(self, future):
            result = future.result().result

            self.get_logger().info('Result: {0}'.format(result.is_finished))
            rclpy.shutdown()


def main(args=None):
	rclpy.init(args=args)
	cd_client = CountdownClient()

	# Sends goal
	future_res = cd_client.send_goal(5)
	rclpy.spin(cd_client, future_res)

if __name__ == '__main__':
	main()