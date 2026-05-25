FROM ubuntu:noble

ARG GZ_DISTRO=harmonic
ENV GZ_DISTRO=${GZ_DISTRO}
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl gnupg2 locales lsb-release sudo \
    && locale-gen en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://packages.osrfoundation.org/gazebo.gpg \
        -o /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" \
        > /etc/apt/sources.list.d/gazebo-stable.list

RUN apt-get update && apt-get install -y --no-install-recommends \
        gz-${GZ_DISTRO} \
    && rm -rf /var/lib/apt/lists/*

CMD ["gz", "sim", "--help"]
