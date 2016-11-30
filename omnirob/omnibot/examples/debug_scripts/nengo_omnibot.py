import nengo
import numpy as np

# use shared memmapped streams for bypassing the re-creation of objects
arm_array = np.memmap("arm_config.npy", dtype = 'float', mode="r+", shape=(5))
base_array = np.memmap("base_config.npy", dtype = 'float', mode="r+", shape=(3))
arm_cam_array = np.memmap('arm_retina_config.npy', dtype='float', mode='r+', shape=(5))

# limits for arm motion
min_pos = np.array([0.16, 0.12, 0.25, 0.0, 0.1])
max_pos = np.array([0.5, 0.5, 0.5, 0.1, 0.25])


# tracking function for arm camera in vertical plane
def arm_tracker(t):
    return arm_cam_array[:]


# functions for demo filtering the values from sliders
def arm_cmd_filter(t, x):
    for i in range(len(x)):
        x[i] = np.interp(x[i], [-1,1], [min_pos[i], max_pos[i]])
    x[x < min_pos] = min_pos[x < min_pos]
    x[x > max_pos] = max_pos[x > max_pos]
    return x

model = nengo.Network()
with model:
    base = nengo.Node([0] * 3)
    arm = nengo.Node([-0.86, -0.73, 0.15, 0.04, -0.55])
    arm_filter = nengo.Node(arm_cmd_filter, size_in=5, size_out=5)

    # omnirob base
    #def bot_control(t, x):
        #base_array[:] = x

    # bot_c = nengo.Node(bot_control, size_in=3, size_out=0)
    # nengo.Connection(base, bot_c)


    # omnirob arm
    def arm_control(t, x):
        if t>2.0:
            arm_array[:] = x
    
    arm_c = nengo.Node(arm_control, size_in=5, size_out=0)
    nengo.Connection(arm, arm_filter, synapse=1.0)
    nengo.Connection(arm_filter, arm_c, synapse=None)

