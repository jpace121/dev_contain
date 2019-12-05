#!/usr/bin/env bash
# Make sure used environment variable is set.
export DEV_CONTAIN_CONTAINER_NAME="${DEV_CONTAIN_CONTAINER_NAME:=dev}"
# Make new session.
tmux new -s $DEV_CONTAIN_CONTAINER_NAME -d
exec sleep +Inf
