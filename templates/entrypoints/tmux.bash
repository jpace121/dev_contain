#!/usr/bin/env bash
# Make sure used environment variables are set.
export CONTAINER_NAME="${CONTAINER_NAME:=dev}"
# Make new session.
tmux new -s $CONTAINER_NAME -d
exec sleep +Inf
