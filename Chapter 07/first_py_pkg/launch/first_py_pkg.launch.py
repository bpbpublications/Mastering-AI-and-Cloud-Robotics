from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

        
    node=Node(
        package = 'first_py_pkg',
        name = 'FirstPublisher',
        executable = 'publisher'
       
    )

    ld.add_action(node)
    return ld