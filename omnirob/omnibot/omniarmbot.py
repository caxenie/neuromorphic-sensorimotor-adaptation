from . import retinabot
import numpy as np


class OmniArmBot(retinabot.RetinaBot):
    def initialize(self):
        super(OmniArmBot, self).initialize()
        self.motor(0, 0, 0)
        self.arm(0.184, 0.172, 0.394, 0.052, 0.134)

    def disconnect(self):
        self.motor(0, 0, 0)
        self.arm(0.184, 0.172, 0.394, 0.052, 0.134)
        super(OmniArmBot, self).disconnect()

    def motor(self, x, y, rot, msg_period=None):
        vrange = 70
        x = int(x * vrange)
        y = int(y * vrange)
        rot = int(rot * vrange)

        if x > vrange: x = vrange
        if x < -vrange: x = -vrange
        if y > vrange: y = vrange
        if y < -vrange: y = -vrange
        if rot > vrange: rot = vrange
        if rot < -vrange: rot = -vrange
        cmd = '!D%d,%d,%d\n' % (x, y, rot)
        self.send('motor', cmd, msg_period=msg_period)

    def arm(self, j1, j2, j3, j4, j5, msg_period=None):

        # motion should be limited by the dynamics of the robot
        # min pos and max pos in the range
        vrange = 4096
        min_pos = np.array([630, 250, 1100, 0, 550])
        max_pos = np.array([2700, 2700, 3000, 600, 1000])
        joints = (np.array([j1, j2, j3, j4, j5])*vrange).astype(dtype=np.int)

        # apply limits
        joints[joints < min_pos] = min_pos[joints < min_pos]
        joints[joints > max_pos] = max_pos[joints > max_pos]

        # indices for motor IDs
        for ids in range(3, 8, 1):
            cmd = '!G%d%d\n' % (ids, joints[ids - 3])
            self.send('arm%d' % ids, cmd, msg_period=msg_period)

if __name__ == '__main__':
    import connection

    bot = OmniArmBot()
    bot.connect(connection.Serial('/dev/ttyUSB2', baud=2000000))
    import time

    while True:
        time.sleep(1)
        bot.motor(0.0, 0.0, 0.0)
