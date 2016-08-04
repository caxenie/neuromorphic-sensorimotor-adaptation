import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

import numpy as np

import json

from os import getcwd

import nstbot

# http://www.tornadoweb.org/en/stable/websocket.html#tornado.websocket.WebSocketHandler

base_values = [0,0,0]

# omnirob base
def bot_control(bot,x):
    if base_values[0]!=x[0] or base_values[1]!=x[1] or base_values[2]!=x[2]:
        base_values[:] = x
        bot.motor(x[0], x[1], x[2], msg_period=0.1)


# omnirob arm
def arm_control(bot,x):
    bot.arm(x[0], x[1], x[2], x[3], x[4], msg_period=0.1)

def arm_servo_read(bot):
    return bot.sensor['servo']

# omnirob arm retina tracker
def arm_tracker(omnirob_cam):
    dvs = np.array(omnirob_cam.get_frequency_info(0))
    dvs[np.isnan(dvs)]=np.zeros(len(dvs[np.isnan(dvs)]))
    xpos = dvs[0] # stimulus on x axis
    ypos = dvs[1] # stimulus on y axis
    prob = dvs[2] # likelihood that it is the stimulus
    return [xpos, ypos, prob]

connected = False

class ControllerWS(tornado.websocket.WebSocketHandler):
    def open(self):
        global connected

        if not connected:
            self.bot = nstbot.OmniBot()
            self.bot.connect(nstbot.Serial('/dev/ttyUSB2', baud=2000000))
            self.omnirob_arm_cam = nstbot.OmniBot()
            self.omnirob_arm_cam.connect(nstbot.Serial('/dev/ttyUSB3', baud=12000000))
            self.omnirob_arm_cam.retina(True)
            self.omnirob_arm_cam.track_frequencies([1000])

            self.omnirob_left_cam = nstbot.OmniBot()
            self.omnirob_left_cam.connect(nstbot.Serial('/dev/ttyUSB0', baud=12000000))
            self.omnirob_left_cam.retina(True)
            self.omnirob_left_cam.track_frequencies([1000])

            self.omnirob_right_cam = nstbot.OmniBot()
            self.omnirob_right_cam.connect(nstbot.Serial('/dev/ttyUSB1', baud=12000000))
            self.omnirob_right_cam.retina(True)
            self.omnirob_right_cam.track_frequencies([1000])
            connected = True
        print("WebSocket opened")

    def on_message(self, cmd):
        cmd = json.loads(cmd)
        if cmd['op']=="read":
            if cmd['array']=="arm_array":
                self.write_message(json.dumps(arm_servo_read(self.bot).tolist()))
            if cmd['array']=="base_array":
                self.write_message(json.dumps(base_values))
	    if cmd['array']=="arm_retina_array":
                self.write_message(json.dumps(arm_tracker(self.omnirob_arm_cam)))
  	    if cmd['array']=="left_retina_array":
                self.write_message(json.dumps(arm_tracker(self.omnirob_left_cam)))
  	    if cmd['array']=="right_retina_array":
                self.write_message(json.dumps(arm_tracker(self.omnirob_right_cam)))
        elif cmd['op']=="write":
            if cmd['array']=="arm_array":
                arm_control(self.bot,cmd['payload'])
	    if cmd['array']=="base_array":
                bot_control(self.bot,cmd['payload'])


    def on_close(self):
        global connected
        connected = False
        print("WebSocket closed")

handlers = [(r'/', ControllerWS),
            (r'/(.*)', tornado.web.StaticFileHandler, {'path': getcwd()})
            ]

application = tornado.web.Application(handlers)

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(9090)
    tornado.ioloop.IOLoop.instance().start()
