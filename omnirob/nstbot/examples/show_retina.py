import nstbot

import time

bot = nstbot.OmniBot()
bot.connect(nstbot.Serial('/home/caxenie/dev/ttyUSB0', baud=12000000))
time.sleep(1)
bot.retina(True)
bot.show_image()
# bot.track_frequencies(freqs=[1000])
while True:
    # dvs_data = bot.get_frequency_info(0)
    # print dvs_data
    time.sleep(0.2)
