import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():


    launch_args = [
        DeclareLaunchArgument('namespace', default_value='',description='Namespace for ROS nodes'),

       ]
   
    namespace = LaunchConfiguration('namespace')

    config = os.path.join(
        get_package_share_directory('my_robot'),
        'config',
        'params.yaml'
        )
    
    ts_node = Node(
        name='TurtleSim',
        package="turtlesim",
        executable="turtlesim_node",
        namespace=namespace,
        output='screen'
    )

    tb_rotate = Node(
        name='TurtleBot',
        package="my_robot",
        executable="tb_rotate",
        parameters = [config],
        namespace=namespace,
        output='screen'
    )



    ld = LaunchDescription(launch_args + [tb_rotate,ts_node,
                                 ])



    return ld