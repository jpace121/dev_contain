#!/usr/bin/env bash
# Make colors work.
export TERM=xterm-256color
# Make new session.
tmux new -s container -d
# Set additional prefix so 'tmux in tmux' works.
tmux set -g prefix2 'C-b'
tmux bind 'C-b' send-prefix -2
# Set unique to container background color.
tmux set -g status-bg blue
# Send commands, if any to tmux.
if [ $# -gt 0 ]
then
    tmux send -t container "$@" ENTER
fi
# Attach.
exec tmux attach -t container
