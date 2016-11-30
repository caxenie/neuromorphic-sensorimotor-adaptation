import nengo

import numpy as np

import time

#
# Arrays used to access the shared memory between the websocket client and Nengo
# 
arm_array = np.memmap("arm_config.npy", dtype = 'float', mode="r+", shape=(5))
base_array = np.memmap("base_config.npy", dtype = 'float', mode="r+", shape=(3))
arm_retina_array = np.memmap("arm_retina_config.npy", dtype = 'float', mode="r+", shape=(3))
left_retina_array = np.memmap("left_retina_config.npy", dtype = 'float', mode="r+", shape=(3))
right_retina_array = np.memmap("right_retina_config.npy", dtype = 'float', mode="r+", shape=(3))

# DEBUG: makes sure arm_array is not accessing the shared memory
# arm_array = numpy.zeros(5)

# Makes sure the system receives the initial values.
initial_joints = np.array([-0.86, -0.73+0.1, 0.15, 0.04, -0.55])

# This is the array that receives the value stored inside joint_memory
arm_array_internal=np.copy(initial_joints)

# Limits for arm motion
# DANGER: THE UNITS HERE ARE THE ONES THE MOTOR RECEIVES, NOT
# THE ONE WE USE INSIDE NENGO!
min_pos = np.array([0.16, 0.12, 0.25, 0.0, 0.1])
max_pos = np.array([0.5, 0.5, 0.5, 0.1, 0.25])

# 
# Function for filtering/converting the values
# Nengo uses variables from -1 to 1, but the motors
# receive some weird values... that's why this function is here!
#
def arm_cmd_filter(x):
    x = np.array(x)
    for i in range(len(x)):
        x[i] = np.interp(x[i], [-1,1], [min_pos[i], max_pos[i]])
    x[x < min_pos] = min_pos[x < min_pos]
    x[x > max_pos] = max_pos[x > max_pos]
    return x

# Function called by the motor nengo.Node
# that sends commands to the robots
def cmd_arm(t,x):
    # Waits for a while before sending commands to the real robot
    if t>0.5:
        arm_array[:]=arm_cmd_filter(x)
    else:
        arm_array[:]=arm_cmd_filter(initial_joints[:])
        
    return arm_array[:]
        
retina_gain = 1
def read_retina_arm(t):
    # This just returns the numpy array where the retina
    # feedback is being recorded
    if t>0.025:
        return retina_gain*np.array([-arm_retina_array[0],-arm_retina_array[1],arm_retina_array[2]])
    else:
        return [0,0,0]
        

# Helper arrays to store information
arm_sine_wave = np.zeros(5)


# Initial gains for the sine waves that move the joints
# until the robot finds the blinking led
arm_sin_gains_init = np.array([1.5,3.0,0.0,0.0,0.0])/10.
arm_sin_gains = np.copy(arm_sin_gains_init)
arm_sin_freq = 8
def arm_osc(t):
    if t>0.5:
        # Calculates the next outputs
        arm_sine_wave[:] = arm_array_internal[:]+np.sin([arm_sin_freq*t]*5)*arm_sin_gains
    else:
        # Keeps them fixed during initialization
        arm_sine_wave[:] = initial_joints[:]
    
    return arm_sine_wave

def initialize_memory(t,x):
    # Loads up the integrator during the first ??? secs
    # with the initial_joints.
    # After that it sends ZERO so nothing happens to the integrator
    # ATTENTION: THE INTEGRATOR MUST BE FED WITH ERROR OTHERWISE IT 
    # ADDS UP UNTIL SATURATION!
    if t>0.25:
        return [0]*5 # after initialization
    else:
        return initial_joints-x
        
    
model = nengo.Network()
with model:
    # 0) move arm to starting position
    # 1) inject noise
    # 2) read the camera and test:
    #   if P is bigger:
    #       if y is closer to zero, keep it
    
    
    # This node tries to force an initial value into the joint_memory
    # otherwise it starts at zero as we can't pass initial conditions
    # to the integrator.
    init_mem_node = nengo.Node(initialize_memory, size_out=5, size_in=5)
    

    # This is the node that injects noise.
    joint_bias = nengo.Node(arm_osc,size_in=0, size_out=5)
    
    # Node receiving the input from the retina cam
    cam_input = nengo.Node(read_retina_arm, size_out=3)
    
    # Creates a delayed version of the inputs
    mem_y = nengo.Ensemble(100, dimensions=1)


    # Calculates the difference between the current 
    # absolute value of the retina y input and the delayed one.
    # This is done to find out if the value is going towards ZERO.
    y_comparison = nengo.Ensemble(100,dimensions=1)

    
    # BASAL GANGLIA
    # Decision making happens here!
    # It will receive three values:
    # -y_comparison
    # +y_comparison
    # idle
    # Idle must win when the other values are weak
    # Basal ganglia shows if the Y value from de camera
    # is moving towards to ZERO or away from it!
    bg_y = nengo.networks.actionselection.BasalGanglia(3)
    
    # THALAMUS
    # Makes sure the basal ganglia is not crazy...
    # (actually it filters the basal ganglia output and makes
    # the decisions clearer)
    thal_y = nengo.networks.actionselection.Thalamus(3)
    
    # Connects Basal ganglia to Thalamus
    # ATTENTION: you need to use ".output" and ".input"
    nengo.Connection(bg_y.output, thal_y.input)
    
    bg_bias=nengo.Node([.9]) # bias to keep basal ganglia's inputs
                             # inside the range 0.3 to 1.0
    
    # This ensemble forces neurons to respond better to fit the abs function
    # It does that by adjusting the neuron tuning curves...or something like that :)
    abs_neurons = nengo.Ensemble(100,dimensions=1,intercepts=nengo.dists.Uniform(0,1))
    
    # This is the connections that maps the "abs" function.
    nengo.Connection(cam_input[1],abs_neurons, function=np.abs, synapse=0.1)
    
    # This is the delayed version of the absolute value of y
    # It is necessary to verify if the signal is moving toward to zero
    # or away from zero.
    nengo.Connection(abs_neurons,mem_y,synapse=0.05)
    
    # ERROR between the current and the delayed version of
    # the Y reading from the arm retina
    # The value used with the "transform" can be used to 
    # increase the sensibility of the basal ganglia, but you
    # need to fiddle with the bg_bias too!
    nengo.Connection(mem_y,y_comparison,transform=-1.7)
    nengo.Connection(abs_neurons,y_comparison,transform=1.7)
    
    
    # The "transform" argument is big because we want to pump it up
    # to avoid letting the idle input win when the other ones
    # are active.
    nengo.Connection(y_comparison,bg_y.input[0], transform=1*4)
    nengo.Connection(y_comparison,bg_y.input[1], transform=-1*4)
    
    # Add the bias to keep the inputs between 0.3 and 1.0
    nengo.Connection(bg_bias,bg_y.input[0])
    nengo.Connection(bg_bias,bg_y.input[1])
    nengo.Connection(bg_bias,bg_y.input[2])
    
    # This is the idle input.
    # It must be strong enough to win when the other signals
    # are not active, but not too strong to suppress them otherwise
    bg_off=nengo.Node([.15])
    nengo.Connection(bg_off,bg_y.input[2], transform=1)
    
    # JOINT MEMORY
    # Here we should have the last "nice" set of joint angles
    # Those angles will be added with jitter to generate the next step
    # (quite hard to avoid drifting without making it too slow...)
    n_jm = 1000
    joint_memory = nengo.networks.EnsembleArray(n_jm, n_ensembles=5)
    nengo.Connection(joint_memory.output,joint_memory.input,synapse=0.015)
    
    # JOINT MEMORY GATE
    # This will transfer the "nice" joint values to the joint memory.
    # It will be, by default, inhibited by memory_locker.
    n_jme = 200
    joint_memory_error = nengo.networks.EnsembleArray(n_jme, n_ensembles=5, neuron_nodes=True)
    nengo.Connection(joint_memory_error.output,joint_memory.input, transform=1, synapse=0)
    nengo.Connection(joint_memory.output,joint_memory_error.input, transform=-1)
    
    # THIS IS THE EXPLORATORY INPUT
    # Joint bias is going to change around the value stored in joint_memory
    # in a senoidal way (could be noise, etc)
    nengo.Connection(joint_bias,joint_memory_error.input, synapse=0.1, transform=1)
    
    
    # thal_y.output[1] => green plot!
    # when the thalamus outputs the green plot we want 
    # to SAVE the current value from joint_bias into joint_memory
    # Thalamus inhibit memory_locker freeing joint_memory_error to set
    # joint_memory to the current joint angles (joint_bias).
    memory_locker_slider = nengo.Node([1])
    n_memlck = 100
    memory_locker = nengo.Ensemble(n_memlck,dimensions=1)
    nengo.Connection(memory_locker_slider,memory_locker)
    nengo.Connection(memory_locker,joint_memory_error.neuron_input, transform=[[-2.5]]*n_jme*5)
    nengo.Connection(thal_y.output[1],memory_locker.neurons, transform=[[-2.5]]*n_memlck)
    
    # Here we load the initial values into the joint_memory
    # Because "joint_memory" is an integrator, it needs to receive an
    # error signal, otherwise it sums until saturate!
    nengo.Connection(init_mem_node,joint_memory.input,synapse=0)
    nengo.Connection(joint_memory.output,init_mem_node,synapse=0.01)
    
    # This is the node that sends commands to the robot!
    # It is connected to the joint_bias.
    # =>The values here are already in "motor space"!!!!
    cmd = nengo.Node(cmd_arm,size_in=5,size_out=0)
    nengo.Connection(joint_bias,cmd,synapse=0.1)
    
    
    # This function reades the value from joint_memory and
    # makes it available to the joint_bias
    def set_joint_bias(t,x):
        if t>0.5 and x[5]==0:
            arm_array_internal[:]=x[:5] #ignores the gripper: x[5]!
        
    joint_memory_reader = nengo.Node(set_joint_bias, size_in=6,size_out=0)
    nengo.Connection(joint_memory.output, joint_memory_reader[:5], synapse=0.01)
    nengo.Connection(memory_locker, joint_memory_reader[5], synapse=0.01)
    

    # ARM
    # Receives inputs directly from Thalamus
    def arm_amplitude_mod(t,x):
        if x[0]>0.5: # output from Thalamus (value goes to zero)
            print "decay arm:",arm_sin_gains
            arm_sin_gains[:]-=0.1/100
            arm_sin_gains[arm_sin_gains<0]=[0]*len(arm_sin_gains[arm_sin_gains<0])
            
        if x[1]>0.6: # output from Thalamus (value goes away from zero)
            print "increase arm:",arm_sin_gains
            arm_sin_gains[:2]+=0.1/50
            if arm_sin_gains[0]>arm_sin_gains_init[0]:
                arm_sin_gains[0]=arm_sin_gains_init[0]
            if arm_sin_gains[1]>arm_sin_gains_init[1]:
                arm_sin_gains[1]=arm_sin_gains_init[0]

    
    # Receives Thalamus outputs and changes the amplitude of the sine wave
    # according with the position of Y retina camera in realtion to ZERO.
    arm_sin_locker = nengo.Node(arm_amplitude_mod,size_in=2,size_out=0)
    
    nengo.Connection(thal_y.output[1],arm_sin_locker[0], synapse=0)
    nengo.Connection(thal_y.output[0],arm_sin_locker[1], synapse=0)
    
    # BASE
    # Receives inputs directly from Thalamus
    base_sin_gains_init = np.array([0,0,1.0])/2. # We changing only the angle
    base_sin_gains = np.copy(base_sin_gains_init)
    base_freq = 8
    def base_oscillator(t,x):
        if t>0.5:
            base_array[:] = np.sin([base_freq*t]*3)*base_sin_gains
        else:
            base_array[:] = [0.0,0.0,0.0]
        
        if x[2]>1:
            if abs(x[0])<0.2: # This is the 
                print "decay base:",base_sin_gains
                base_sin_gains[:]-=0.1/10
                base_sin_gains[base_sin_gains<0]=[0]*len(base_sin_gains[base_sin_gains<0])
                
            elif abs(x[0])>0.4:
                print "increase base:",base_sin_gains
                base_sin_gains[2]+=0.1/5
                if base_sin_gains[2]>base_sin_gains_init[2]:
                    base_sin_gains[2]=base_sin_gains_init[2]
            else:
                base_array[:] = [0.5,0.0,0.0]
                print "Got it!"
        else:
            print "Parm:", x[2]
            base_array[:] = [0.0,0.0,0.7]
        

    base_osc = nengo.Node(base_oscillator,size_in=3,size_out=0)
    
    nengo.Connection(cam_input,base_osc,synapse=0) # X retina value
    
    Parm = nengo.Node(None, size_in=1)
    nengo.Connection(cam_input[2],Parm)
