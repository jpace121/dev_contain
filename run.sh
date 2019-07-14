#!/usr/bin/env bash

podman run \
    --volume /home/jimmy/Develop:/root/Develop:rw \
    --rm \
    --workdir /root \
    -it jwp-ros2-latest \
    bash
