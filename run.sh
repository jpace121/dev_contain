#!/usr/bin/env bash

username=$(whoami)
userid=$(id -u)

podman run \
    --rm \
    --workdir /home/$username \
    --user $username \
    --userns=keep-id \
    --volume /home/$username/Develop:/home/$username/Develop:Z \
    -it jwp-build-latest \
    bash

