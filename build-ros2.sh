#!/usr/bin/env bash
#
# Copyright 2019 James Pace
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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

