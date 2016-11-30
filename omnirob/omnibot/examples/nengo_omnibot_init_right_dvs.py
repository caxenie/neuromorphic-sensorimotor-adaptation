import show_omnibot
import numpy as np
import time

right_retina_array = np.memmap("right_retina_config.npy", dtype = 'float', mode="r+", shape=(3))

omnirob_right_cam = show_omnibot.NSTBot()
omnirob_right_cam.connect(show_omnibot.Serial('/home/caxenie/dev/ttyUSB1', baud=12000000))
omnirob_right_cam.retina(True)
omnirob_right_cam.track_frequencies([1000])

# omnirob arm retina tracker
def arm_tracker():
    dvs = np.array(omnirob_right_cam.get_frequency_info(0))
    dvs[np.isnan(dvs)]=np.zeros(len(dvs[np.isnan(dvs)]))
    xpos = dvs[0] # stimulus on x axis
    ypos = dvs[1] # stimulus on y axis
    prob = dvs[2] # likelihood that it is the stimulus
    return [xpos, ypos, prob]

while True:
    right_retina_array[:] = arm_tracker()
    time.sleep(0.12/2)
