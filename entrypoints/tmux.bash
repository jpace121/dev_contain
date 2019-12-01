#!/usr/bin/env bash

tmux new -s container -d
if [ $# -gt 0 ]
then
    tmux send -t container "$@" ENTER
fi
tmux attach -t container
