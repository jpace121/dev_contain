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

# Build a base development image for development.

container=$(buildah from ubuntu:18.04)

username=$(whoami)
userid=$(id -u)

buildah run --net host $container -- apt update -y
buildah run --net host $container -- apt upgrade -y

echo "==> Grab tzdata. It gets randomly installed sometimes and needs noninteractive."
buildah run --net host $container -- bash -c 'DEBIAN_FRONTEND=noninteractive apt install -y tzdata'

buildah run --net host $container -- bash -c 'apt install -y sudo'
buildah run --net host $container -- useradd -m -G sudo -s /bin/bash -u $userid $username
buildah run --net host $container -- bash -c 'echo "%sudo  ALL=(ALL)       NOPASSWD: ALL" >> /etc/sudoers.d/container'
buildah run --net host $container -- chmod 0440 /etc/sudoers.d/container

buildah run --net host $container -- apt install -y iproute2

echo "==> Dev environment depenendencies."
buildah run --net host $container -- apt install -y emacs-nox vim-nox
buildah run --net host $container -- apt install -y git tmux silversearcher-ag

echo "==> Clone emacs cofig."
buildah run --net host --user $username $container -- git clone git://github.com/jpace121/evil-ed.git /home/$username/.emacs.d
buildah run --net host --user $username $container -- bash /home/$username/.emacs.d/add_emc_and_tmux.sh

echo "==> Setting git config."
buildah run --net host --user $username $container -- git config --global user.name "James Pace"
buildah run --net host --user $username $container -- git config --global user.email "jpace121@gmail.com"

echo "==> Save image."
buildah commit --squash --rm $container jwp-build-latest

#echo "===> Send to Docker."
#buildah push jwp-build-latest docker-daemon:jwp-build:latest
