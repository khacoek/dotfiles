#! /bin/bash 

lxsession &
picom --experimental-backends &
nitrogen --restore &
#/usr/bin/emacs --daemon &
dunst &
volumeicon &
nm-applet &
cbatticon &
udiskie -t &
