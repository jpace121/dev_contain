#!/usr/bin/env bash

podman run \
    --mount type=bind,source=/home/jimmy/Develop/,destination=/home/jimmy \
    --rm \
    --user jimmy \
    -it jwp-build-latest \
    bash
