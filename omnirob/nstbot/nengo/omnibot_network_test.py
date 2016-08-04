import nstbot
import numpy as np
import nengo


model = nengo.Network()
with model:
    bot = nstbot.OmniBotNetwork(
        nstbot.Socket(nstbot.connection.Serial('/dev/ttyUSB2', baud=2000000)),
        motor=True, arm=True, retina=False,  # freqs=[100, 200, 300],
        wheel=True, servo=True, load=True, msg_period=0.1)

    motor = nengo.Node([0, 0, 0])
    arm = nengo.Node([0]*5)
    nengo.Connection(motor, bot.motor)
    nengo.Connection(arm, bot.arm)


