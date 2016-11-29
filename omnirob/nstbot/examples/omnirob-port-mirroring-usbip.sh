#!/bin/bash

# Script to enable the USB port mirroring from the robot, such that the dvs, base and arm data and
# commands are available on the processing machine
# the port forwarding script on the robot enables the following:

# Server side setup - robot
# make sure sudo chown nst:nst /dev/ttyUSB*
# socat TCP-LISTEN:54320,reuseaddr,fork /dev/ttyUSB0,raw &
# socat TCP-LISTEN:54321,reuseaddr,fork /dev/ttyUSB1,raw &
# socat TCP-LISTEN:54322,reuseaddr,fork /dev/ttyUSB2,raw &
# socat TCP-LISTEN:54323,reuseaddr,fork /dev/ttyUSB3,raw &


socat -d -d pty,link=/home/caxenie/dev/ttyUSB0,echo=0 tcp:10.162.177.29:54320 & 
socat -d -d pty,link=/home/caxenie/dev/ttyUSB1,echo=0 tcp:10.162.177.29:54321 & 
socat -d -d pty,link=/home/caxenie/dev/ttyUSB2,echo=0 tcp:10.162.177.29:54322 &
socat -d -d pty,link=/home/caxenie/dev/ttyUSB3,echo=0 tcp:10.162.177.29:54323 & 


