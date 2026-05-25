FROM ubuntu:noble

ARG ROS_DISTRO=jazzy
ENV ROS_DISTRO=${ROS_DISTRO}
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl gnupg2 locales lsb-release \
        software-properties-common sudo \
    && locale-gen en_US.UTF-8 \
    && add-apt-repository universe \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
        -o /usr/share/keyrings/ros-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
        > /etc/apt/sources.list.d/ros2.list

RUN apt-get update && apt-get install -y --no-install-recommends \
        ros-${ROS_DISTRO}-desktop \
        ros-dev-tools \
        python3-colcon-common-extensions \
        python3-rosdep \
    && rosdep init && rosdep update --rosdistro=${ROS_DISTRO} \
    && rm -rf /var/lib/apt/lists/*

RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> /etc/bash.bashrc

CMD ["/bin/bash"]
