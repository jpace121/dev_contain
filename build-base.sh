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

DEFAULT_BASE_IMAGE=ubuntu:18.04
DEFAULT_IMAGE_NAME=jwp-build-latest
SHOULD_BUILD=0

BASE_IMAGE=$DEFAULT_BASE_IMAGE
IMAGE_NAME=$DEFAULT_IMAGE_NAME

function useage {
    echo "Useage: build-base.sh -f BASE_IMAGE -n IMAGE_NAME"
    echo ""
    echo "Builds an image using container with my dev environment from"
    echo "preexisting image BASE_IMAGE, saved as image IMAGE_NAME."
    echo "Defaults: "
    echo "BASE_IMAGE = $DEFAULT_BASE_IMAGE IMAGE_NAME = $DEFAULT_IMAGE_NAME"
    echo ""
    echo "BASE_IMAGE assumed to be Debian/Apt based."
}

while getopts ":hf:n:" opt; do
case ${opt} in
    f ) BASE_IMAGE=$OPTARG
    ;;
    n ) IMAGE_NAME=$OPTARG
    ;;
    h ) useage; SHOULD_BUILD=1
    ;;
    \? ) useage; SHOULD_BUILD=1
    ;;
    : ) useage; SHOULD_BUILD=1
    ;;
esac
done
shift $((OPTIND -1))

function build_image {
    # Build a base development image for development.

    echo "==> Building from image $BASE_IMAGE"
    container=$(buildah from $BASE_IMAGE)

    username=$(whoami)
    userid=$(id -u)

    echo "==> Updating and upgrading."
    buildah run --net host $container -- apt update -y
    buildah run --net host $container -- apt upgrade -y

    echo "==> Grab tzdata. It gets randomly installed sometimes and needs noninteractive."
    buildah run --net host $container -- bash -c 'DEBIAN_FRONTEND=noninteractive apt install -y tzdata'

    echo "==> Set up sudo."
    buildah run --net host $container -- bash -c 'apt install -y sudo'
    buildah run --net host $container -- useradd -m -G sudo -s /bin/bash -u $userid $username
    buildah run --net host $container -- bash -c 'echo "%sudo  ALL=(ALL)       NOPASSWD: ALL" >> /etc/sudoers.d/container'
    buildah run --net host $container -- chmod 0440 /etc/sudoers.d/container


    echo "==> Dev environment depenendencies."
    buildah run --net host $container -- apt install -y iproute2
    buildah run --net host $container -- apt install -y emacs-nox vim-nox
    buildah run --net host $container -- apt install -y git tmux silversearcher-ag

    echo "==> Clone emacs cofig."
    buildah run --net host --user $username $container -- git clone git://github.com/jpace121/evil-ed.git /home/$username/.emacs.d
    buildah run --net host --user $username $container -- bash /home/$username/.emacs.d/add_emc_and_tmux.sh

    echo "==> Setting git config."
    buildah run --net host --user $username $container -- git config --global user.name "James Pace"
    buildah run --net host --user $username $container -- git config --global user.email "jpace121@gmail.com"

    echo "==> Save image."
    buildah commit --squash --rm $container $IMAGE_NAME

    #echo "===> Send to Docker."
    #buildah push $IMAGE_NAME docker-daemon:$IMAGE_NAME:latest
}


function confirm_args {
    # If -h or related options were selected don't build.
    if [ ! $SHOULD_BUILD ]
    then
        return 1
    fi
    # If we changed the base image name, we should change the saved image name
    if [ "$BASE_IMAGE" != "$DEFAULT_BASE_IMAGE" ]
    then
      if [ "$IMAGE_NAME" == "$DEFAULT_IMAGE_NAME" ]
      then
        echo "Abort!"
        echo "Not default base image $BASE_IMAGE, with default image name $IMAGE_NAME."
        useage
        return 1
      fi
    fi
    return 0
}

if confirm_args 
   then
       build_image
fi
