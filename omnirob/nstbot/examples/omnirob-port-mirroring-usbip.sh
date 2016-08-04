#!/bin/sh

# Script to enable the USB port mirroring from the robot, such that the dvs, base and arm data and
# commands are available on the processing machine
# the port forwarding script on the robot enables the following:

# socat tcp-l:58000,reuseaddr,fork file:/dev/ttyUSB0,nonblock,waitlock=/home/nst/ttyUSB0.lock & # left dvs
# socat tcp-l:58001,reuseaddr,fork file:/dev/ttyUSB1,nonblock,waitlock=/home/nst/ttyUSB1.lock & # right dvs
# socat tcp-l:58002,reuseaddr,fork file:/dev/ttyUSB2,nonblock,waitlock=/home/nst/ttyUSB2.lock & # robot and arm
# socat tcp-l:58003,reuseaddr,fork file:/dev/ttyUSB3,nonblock,waitlock=/home/nst/ttyUSB3.lock & # arm dvs


socat pty,link=$HOME/dev/ttyUSB0,raw,echo=0,waitslave tcp:10.162.177.29:58000 & # left dvs
socat pty,link=$HOME/dev/ttyUSB1,raw,echo=0,waitslave tcp:10.162.177.29:58001 & # right dvs
socat pty,link=$HOME/dev/ttyUSB2,raw,echo=0,waitslave tcp:10.162.177.29:58002 & # robot and arm
socat pty,link=$HOME/dev/ttyUSB3,raw,echo=0,waitslave tcp:10.162.177.29:58003 & # arm dvs
