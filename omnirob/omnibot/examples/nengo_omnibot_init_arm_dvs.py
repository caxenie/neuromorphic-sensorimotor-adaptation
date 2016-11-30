import show_omnibot
import numpy as np
import time

arm_retina_array = np.memmap("arm_retina_config.npy", dtype = 'float', mode="r+", shape=(3))

omnirob_arm_cam = show_omnibot.NSTBot()
omnirob_arm_cam.connect(show_omnibot.Serial('/home/caxenie/dev/ttyUSB3', baud=12000000))
omnirob_arm_cam.retina(True)
omnirob_arm_cam.track_frequencies([1000])

# omnirob arm retina tracker
def arm_tracker():
    dvs = np.array(omnirob_arm_cam.get_frequency_info(0))
    dvs[np.isnan(dvs)]=np.zeros(len(dvs[np.isnan(dvs)]))
    xpos = dvs[0] # stimulus on x axis
    ypos = dvs[1] # stimulus on y axis
    prob = dvs[2] # likelihood that it is the stimulus
    return [xpos, ypos, prob]	
     	
while True:
    arm_retina_array[:] = arm_tracker()
    time.sleep(0.12/2)
