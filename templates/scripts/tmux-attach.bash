#!/usr/bin/env bash
# Set a default value. If not set somehow, the attach command will
# fail.
DEV_CONTAIN_CONTAINER_NAME="${DEV_CONTAIN_CONTAINER_NAME:-tmux}"

tmux new -A -s $DEV_CONTAIN_CONTAINER_NAME
