#!/bin/bash

# Script to enable the USB port mirroring from the robot, such that the dvs, base and arm data and
# commands are available on the processing machine
# the port forwarding script on the robot enables the following:

# make sure the custom baudrates are set
# ./set_cust_baud /dev/ttyUSB0 12000000 &
# ./set_cust_baud /dev/ttyUSB1 12000000 &
# ./set_cust_baud /dev/ttyUSB2 2000000 &
# ./set_cust_baud /dev/ttyUSB3 12000000 &

# run the evil machinery ...
#  to debug add option: -d (up to 4 times for 4 level of debug messages)
# socat TCP-LISTEN:54320,reuseaddr,fork /dev/ttyUSB0,raw & 
# socat TCP-LISTEN:54321,reuseaddr,fork /dev/ttyUSB1,raw &
# socat TCP-LISTEN:54322,reuseaddr,fork /dev/ttyUSB2,raw &
# socat TCP-LISTEN:54323,reuseaddr,fork /dev/ttyUSB3,raw &

# to debug add option: -d (up to 4 times for 4 level of debug messages)
socat pty,link=/home/caxenie/dev/ttyUSB0,echo=0 tcp:10.162.177.29:54320 & 
socat pty,link=/home/caxenie/dev/ttyUSB1,echo=0 tcp:10.162.177.29:54321 & 
socat pty,link=/home/caxenie/dev/ttyUSB2,echo=0 tcp:10.162.177.29:54322 &
socat pty,link=/home/caxenie/dev/ttyUSB3,echo=0 tcp:10.162.177.29:54323 & 


