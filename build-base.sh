#!/usr/bin/env bash
set -e

# Build a base developement image for development.

container=$(buildah from ubuntu:18.04)

buildah run --net host $container -- apt update -y
buildah run --net host $container -- apt upgrade -y

echo "==> Grab tzdata. It gets randomly installed sometimes and needs noninteractive."
buildah run --net host $container -- bash -c 'DEBIAN_FRONTEND=noninteractive apt install -y tzdata'

echo "==> Dev environment depenendencies."
buildah run --net host $container -- apt install -y emacs-nox vim-nox
buildah run --net host $container -- apt install -y git

echo "==> Clone emacs cofig."
buildah run --net host $container -- git clone git://github.com/jpace121/evil-ed.git /root/.emacs.d

echo "==> Save image."
buildah commit $container jwp-build-latest
buildah rm $container

