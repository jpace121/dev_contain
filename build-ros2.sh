#!/usr/bin/env bash
set -e

username=$(whoami)

# Build container for running ros2 from source.

container=$(buildah from localhost/jwp-build-latest)

echo "==> Apt key"
buildah run --net host $container -- apt install -y curl gnupg2 lsb-release
buildah run --net host $container -- bash -c 'curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add -'
buildah run --net host $container -- bash -c 'echo "deb [arch=amd64,arm64] http://packages.ros.org/ros2/ubuntu `lsb_release -cs` main" > /etc/apt/sources.list.d/ros2-latest.list'

echo "==> Copy and run Script."
buildah copy --chown $username:$username $container ./ros2/build-from-source.bash /home/jimmy/build-from-source.bash
buildah run --user $username $container -- bash -c 'chmod +x /home/jimmy/build-from-source.bash'
buildah run --net host --user $username $container -- bash -c '/home/jimmy/build-from-source.bash'

echo "==> Save image."
buildah commit --squash --rm $container jwp-ros2-latest

#echo "===> Send to Docker."
#buildah push jwp-ros2-latest docker-daemon:jwp-ros2:latest

