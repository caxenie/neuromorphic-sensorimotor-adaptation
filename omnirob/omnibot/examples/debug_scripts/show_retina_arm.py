import omnibot

import time

bot = omnibot.RetinaBot()
bot.connect(omnibot.Serial('/home/caxenie/dev/ttyUSB3', baud=12000000))
time.sleep(1)
bot.retina(True)
bot.show_image()
bot.track_frequencies(freqs=[1000])
while True:
    dvs_data = bot.get_frequency_info(0)
    print dvs_data
    time.sleep(0.05)
