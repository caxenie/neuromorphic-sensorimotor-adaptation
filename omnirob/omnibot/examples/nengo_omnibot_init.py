import show_omnibot
import numpy as np
import time

arm_array = np.memmap("arm_config.npy", dtype = 'float', mode="r+", shape=(5))
base_array = np.memmap("base_config.npy", dtype = 'float', mode="r+", shape=(3))

arm_array[:] = [0.184, 0.172, 0.394, 0.052, 0.134]
base_array[:] = [0, 0, 0]

bot = show_omnibot.NSTBot()
bot.connect(show_omnibot.Serial('/home/caxenie/dev/ttyUSB2', baud=2000000))


# omnirob base
def bot_control(x):
    bot.motor(x[0], x[1], x[2], msg_period=0.1)


# omnirob arm
def arm_control(x):
    bot.arm(x[0], x[1], x[2], x[3], x[4], msg_period=0.1)

while True:
    bot_control(base_array)
    time.sleep(0.12/2.0)
    arm_control(arm_array)
    time.sleep(0.12/2.0)
