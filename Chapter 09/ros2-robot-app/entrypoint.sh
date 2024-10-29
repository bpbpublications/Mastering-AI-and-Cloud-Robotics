#!/bin/bash
# Basic entrypoint for ROS / Colcon Docker containers

# Source ROS 2
source /opt/ros/${ROS_DISTRO}/setup.bash
echo "Sourced ROS 2 ${ROS_DISTRO}"

# Source the base workspace, if built
if [ -f /ros2_ws/install/setup.bash ]
then
  source /ros2_ws/install/setup.bash
  echo "Sourced TurtleBot3 base workspace"
fi

#printenv
# Execute the command passed into this entrypoint
exec "$@"
