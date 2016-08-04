#!/bin/bash

nohup python nengo_omnibot_init_arm_dvs.py &
nohup python nengo_omnibot_init_left_dvs.py &
nohup python nengo_omnibot_init_right_dvs.py &
nohup python nengo_omnibot_init.py &
nohup python tornado_websocket_server.py & 
