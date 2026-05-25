ARG ROS_IMAGE_TAG=latest
FROM hsjin94/ros2-jazzy:${ROS_IMAGE_TAG}

ARG ROS_DISTRO=jazzy
ENV ROS_DISTRO=${ROS_DISTRO}
ENV WS=/root/ros2_ws

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-setuptools ros-${ROS_DISTRO}-geometry-msgs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR ${WS}
COPY src ${WS}/src
RUN . /opt/ros/${ROS_DISTRO}/setup.sh && colcon build --packages-select marine_ctrl

RUN echo "source ${WS}/install/setup.bash" >> /etc/bash.bashrc

CMD ["bash", "-lc", "source ${WS}/install/setup.bash && ros2 run marine_ctrl auto"]
