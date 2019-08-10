#!/usr/bin/env bash
set -e

# Build container for running ros2

container=$(buildah from localhost/jwp-build-latest)

echo "==> Dependencies."
buildah run --net host $container -- apt install -y curl gnupg2 lsb-release
echo "==> Apt key"
buildah run --net host $container -- bash -c 'curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add -'
buildah run --net host $container -- bash -c 'echo "deb [arch=amd64,arm64] http://packages.ros.org/ros2/ubuntu `lsb_release -cs` main" > /etc/apt/sources.list.d/ros2-latest.list'
buildah run --net host $container -- apt update
echo "==> Install."
buildah run --net host $container -- apt install -y ros-dashing-desktop
buildah run --net host $container -- apt install -y python3-colcon-common-extensions

echo "==> Save image."
buildah commit $container jwp-ros2-latest
buildah rm $container

#echo "===> Send to Docker."
#buildah push jwp-ros2-latest docker-daemon:jwp-ros2:latest
