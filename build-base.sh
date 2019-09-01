#!/usr/bin/env bash
set -e

# Build a base developement image for development.

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


echo "==> Dev environment depenendencies."
buildah run --net host $container -- apt install -y emacs-nox vim-nox
buildah run --net host $container -- apt install -y git iproute2

echo "==> Clone emacs cofig."
buildah run --net host --user $username $container -- git clone git://github.com/jpace121/evil-ed.git /home/$username/.emacs.d

echo "==> Save image."
buildah commit $container jwp-build-latest
buildah rm $container

#echo "===> Send to Docker."
#buildah push jwp-build-latest docker-daemon:jwp-build:latest
