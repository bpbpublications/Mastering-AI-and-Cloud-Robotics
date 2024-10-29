import os, subprocess
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():


    launch_args = [
        DeclareLaunchArgument('namespace', default_value='',description='Namespace for ROS nodes'),

       ]
   
    namespace = LaunchConfiguration('namespace')

    config = os.path.join(
        get_package_share_directory('service_robot'),
        'config',
        'params.yaml'
        )
    

    mqtt_bridge = Node(
        name='MqttBridge',
        package="service_robot",
        executable="mqtt_bridge",
        parameters = [config],
        namespace=namespace,
        output='screen'
    )

    stats_publisher = Node(
        name='StatsPublisher',
        package='service_robot',
        executable='stats_publisher',
        parameters = [config],
        namespace=namespace,
        output='screen'
    )

    cmd_subscriber = Node(
        name='CmdSubscriber',
        package='service_robot',
        executable='cmd_subscriber',
        parameters = [config],
        namespace=namespace,
        output='screen'
    )


    ld = LaunchDescription(launch_args + [mqtt_bridge,
                                 stats_publisher, cmd_subscriber,
                                 ])



    return ld