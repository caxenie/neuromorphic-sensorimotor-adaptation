import omnibot

import time

bot = omnibot.OmniArmBot()
bot.connect(omnibot.Serial('/home/caxenie/dev/ttyUSB2', baud=2000000))
bot.activate_sensors(servo=True, wheel=True, load=True)

while True:

    # Basic test for IO with omnirob

    # base motion
    bot.motor(0, 0, 0.5)
    time.sleep(1)
	
    # read sensor
    joints = bot.sensor['servo']

    # move arm
    bot.arm(0.184, 0.172, 0.394, 0.052, 0.134)
    time.sleep(3)
    bot.arm(0.256, 0.207, 0.362, 0.052, 0.134)
    time.sleep(2)

