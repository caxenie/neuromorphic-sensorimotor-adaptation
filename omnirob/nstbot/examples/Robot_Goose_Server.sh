#!/bin/bash

# initialize the sensory data forwarding
./omnirob-port-mirroring-usbip.sh &
# initialize the memmapped file communication
nohup python nengo_omnibot_init_arm_dvs.py &
nohup python nengo_omnibot_init_left_dvs.py &
nohup python nengo_omnibot_init_right_dvs.py &
nohup python nengo_omnibot_init.py &
# needed ?!?
# nohup python tornado_websocket_server.py &
