#!/bin/sh

# Script to enable the USB port mirroring from the robot, such that the dvs, base and arm data and
# commands are available on the processing machine
# the port forwarding script on the robot enables the following:

# socat tcp-l:54320,reuseaddr,fork file:/dev/ttyUSB0,nonblock,waitlock=/home/nst/ttyUSB0.lock & # left dvs
# socat tcp-l:54321,reuseaddr,fork file:/dev/ttyUSB1,nonblock,waitlock=/home/nst/ttyUSB1.lock & # right dvs
# socat tcp-l:54322,reuseaddr,fork file:/dev/ttyUSB2,nonblock,waitlock=/home/nst/ttyUSB2.lock & # robot and arm
# socat tcp-l:54323,reuseaddr,fork file:/dev/ttyUSB3,nonblock,waitlock=/home/nst/ttyUSB3.lock & # arm dvs

# create a virual port pair for avoiding disconnection from the bridge when client terminates (e.g. Nengo finishes simulation)
socat pty,raw,echo=0,link=$HOME/dev/ttyVUSB0 pty,raw,echo=0,link=$HOME/dev/ttyUSB0 &
socat pty,raw,echo=0,link=$HOME/dev/ttyVUSB1 pty,raw,echo=0,link=$HOME/dev/ttyUSB1 &
socat pty,raw,echo=0,link=$HOME/dev/ttyVUSB2 pty,raw,echo=0,link=$HOME/dev/ttyUSB2 &
socat pty,raw,echo=0,link=$HOME/dev/ttyVUSB3 pty,raw,echo=0,link=$HOME/dev/ttyUSB3 &
# create the links from the serial to the TCP port
socat open:$HOME/dev/ttyVUSB0,raw,echo=0,nonblock tcp:10.162.177.29:54320,reuseaddr & # left dv
socat open:$HOME/dev/ttyVUSB1,raw,echo=0,nonblock tcp:10.162.177.29:54321,reuseaddr & # right dvs
socat open:$HOME/dev/ttyVUSB2,raw,echo=0,nonblock tcp:10.162.177.29:54322,reuseaddr & # robot and arm
socat open:$HOME/dev/ttyVUSB3,raw,echo=0,nonblock tcp:10.162.177.29:54323,reuseaddr & # arm dvs
