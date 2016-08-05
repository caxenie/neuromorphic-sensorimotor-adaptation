# Example showing the use of spiking cameras in V-REP
# The network uses a memory to remember where it has last seen the ball
# Scene File: ss_vision.ttt
import nengo
import sensors
import actuators
from robots import CustomRobot
from nengo.networks import InputGatedMemory
from functools import partial
import numpy as np

# Dimensions of the camera: 32x32
DIM = 32

# Set-up for creating transformation from 32x32 visual scene
# to 2-dimensional x-y location
# this is probably a bad and inefficient way to do this, but it works
x_loc_transform = [[]]
y_loc_transform = [[]]
for i in range(DIM):
    for j in range(DIM):
        y_loc_transform[0].append(i-DIM/2)
        x_loc_transform[0].append(j-DIM/2)

# Transformation from visual input to approximate x-y location
def location_transform(v):
    v_mat = np.matrix(v).T
    total = np.sum(v)
    if total > 0:
        x_loc = (np.matrix(x_loc_transform)*v_mat)/total
        y_loc = (np.matrix(y_loc_transform)*v_mat)/total
    else:
        x_loc = 0
        y_loc = 0
    return [x_loc, y_loc]

# if there is very little visual input (noise) gate the memory
def gating_function(v):
    total = np.sum(v)
    if total < 5:
        return 1
    else:
        return 0

robot = CustomRobot(sim_dt=0.05, sync=True)
robot.add_sensor("DVS128_sensor", sensors.dvs_vision)

model = nengo.Network(seed=13)
with model:
  robot_node = nengo.Node(robot, size_in=1, size_out=DIM*DIM)

  # Current location of the ball from vision
  location = nengo.Ensemble(n_neurons=300, dimensions=2, radius=DIM/2)
  
  # Location of where the ball was last seen (same as the memory)
  last_seen = nengo.Ensemble(n_neurons=300, dimensions=2, radius=DIM/2)
  
  mem_config = nengo.Config(nengo.Ensemble, nengo.Connection)
  mem_config[nengo.Ensemble].radius=DIM/2
  mem_config[nengo.Connection].synapse = nengo.Lowpass(0.1)
  #memory = InputGatedMemory(n_neurons=300, dimensions=2, difference_gain=15, gate_gain=30, mem_config=mem_config)
  with mem_config:
      # Memory of where the ball was last seen
      memory = InputGatedMemory(n_neurons=300, dimensions=2, difference_gain=15)

  nengo.Connection(robot_node, location, function=location_transform)
  nengo.Connection(location, memory.input)
  nengo.Connection(robot_node, memory.gate, function=gating_function, transform=30, synapse=0.002)
  nengo.Connection(memory.output, last_seen)
