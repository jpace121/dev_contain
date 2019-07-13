#!/usr/bin/env bash

# Build a base developement image for development.

alias buildah_run="buildah run --net host"

container=$(buildah from ubuntu:18.04)

buildah run --net host $container -- apt update -y
buildah run --net host $container -- apt upgrade -y

echo "==> Dev environment depenendencies."
buildah run --net host $container -- apt install -y emacs-nox
buildah run --net host $container -- apt install -y git

echo "==> Add user account."
buildah run $container -- useradd -m -s /bin/bash jimmy
buildah config --user jimmy $container

echo "==> Clone emacs cofig."
buildah run --net host --user jimmy --workingdir '/home/jimmy' $container -- git clone git://github.com/jpace121/evil-ed.git /home/jimmy/.emacs.d

echo "==> Save image."
buildah commit $container jwp-build-latest
buildah rm $container

