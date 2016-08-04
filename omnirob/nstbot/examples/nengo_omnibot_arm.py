import nstbot
import numpy as np
import nengo
import time

# omnirob base control
def bot_control(t, x):
    bot.motor(x[0], x[1], x[2], msg_period=0.1)


# omnirob arm control
def arm_control(t, x):
    bot.arm(x[0], x[1], x[2], x[3], x[4], msg_period=0.1)


# limits for arm motion
min_pos = np.array([0.16, 0.12, 0.25, 0.0, 0.1])
max_pos = np.array([0.5, 0.5, 0.5, 0.1, 0.25])


# functions for demo filtering the values from sliders
def arm_cmd_filter(t, x):
    x[x < min_pos] = min_pos[x < min_pos]
    x[x > max_pos] = max_pos[x > max_pos]
    return x

# create model and connect to robot
bot = nstbot.OmniBot()
bot.connect(nstbot.Serial('/dev/ttyUSB2', baud=2000000))

model = nengo.Network()
with model:
    base = nengo.Node([0] * 3)
    arm = nengo.Node([0.184, 0.25, 0.5, 0.052, 0.134])
    arm_filter = nengo.Node(arm_cmd_filter, size_in=5, size_out=5)

    bot_c = nengo.Node(bot_control, size_in=3, size_out=0)
    nengo.Connection(base, bot_c)

    arm_c = nengo.Node(arm_control, size_in=5, size_out=0)
    nengo.Connection(arm, arm_filter, synapse=None)
    nengo.Connection(arm_filter, arm_c)
