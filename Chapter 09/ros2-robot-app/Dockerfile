ARG ROS_DISTRO=humble
 

FROM osrf/ros:${ROS_DISTRO}-desktop-full as base
ENV ROS_DISTRO=${ROS_DISTRO}
ENV DISPLAY=novnc:0.0
SHELL ["/bin/bash", "-c"]


RUN apt-get update && apt-get install -y git wget python3-pip vim

# install bootstrap tools
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    git \
    python3-colcon-common-extensions \
    python3-colcon-mixin \
    python3-rosdep \
    python3-vcstool \
    && rm -rf /var/lib/apt/lists/*


# Create Colcon workspace with external dependencies
RUN mkdir -p /ros2_ws
WORKDIR /ros2_ws
COPY . .

COPY dependencies.repos .
RUN vcs import < dependencies.repos

# Build the base Colcon workspace, installing dependencies first.
RUN source /opt/ros/${ROS_DISTRO}/setup.bash \
 && apt-get update -y \
 && rosdep install --from-paths src --ignore-src --rosdistro ${ROS_DISTRO} -y \
 && colcon build --symlink-install

# Set up the entrypoint
COPY ./entrypoint.sh /
ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "ros2", "launch","my_robot", "my_robot.launch.py" ]