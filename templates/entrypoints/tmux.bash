#!/usr/bin/env bash
export TERM=xterm-256color

tmux new -s container -d

# Set additional prefix so 'tmux in tmux' works.
tmux set -g prefix2 'C-b'
tmux bind 'C-b' send-prefix -2
# Set unique to container background color.
tmux set -g status-bg blue
 
if [ $# -gt 0 ]
then
    tmux send -t container "$@" ENTER
fi
exec tmux attach -t container
