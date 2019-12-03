#!/usr/bin/env bash
# Make colors work.
export TERM=xterm-256color
# Make sure used environment variables are set.
export PROJECT_NAME="${PROJECT_NAME:=dev}"
# Make new session.
tmux new -s $PROJECT_NAME -d
# Set additional prefix so 'tmux in tmux' works.
tmux set -g prefix2 'C-b'
tmux bind 'C-b' send-prefix -2
# Remove right status line.
tmux set-option -g status-right ""
# Set unique to container background color.
tmux set -g status-bg blue
# Attach.
exec tmux attach -t $PROJECT_NAME
