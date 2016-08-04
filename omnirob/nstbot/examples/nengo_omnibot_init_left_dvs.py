import nstbot
import numpy as np
import time

left_retina_array = np.memmap("left_retina_config.npy", dtype = 'float', mode="r+", shape=(3))

omnirob_left_cam = nstbot.OmniBot()
omnirob_left_cam.connect(nstbot.Serial('/home/caxenie/dev/ttyUSB0', baud=12000000))
omnirob_left_cam.retina(True)
omnirob_left_cam.track_frequencies([1000])

# omnirob arm retina tracker
def arm_tracker():
    dvs = np.array(omnirob_left_cam.get_frequency_info(0))
    dvs[np.isnan(dvs)]=np.zeros(len(dvs[np.isnan(dvs)]))
    xpos = dvs[0] # stimulus on x axis
    ypos = dvs[1] # stimulus on y axis
    prob = dvs[2] # likelihood that it is the stimulus
    return [xpos, ypos, prob]	
     	
while True:
    left_retina_array[:] = arm_tracker()
    time.sleep(0.12/2)
