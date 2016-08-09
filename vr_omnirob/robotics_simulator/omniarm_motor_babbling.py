# A omnirob with arm performing motor babbling
# Scene File: omni3wheel1arm_model.ttt
import nengo
import sensors
import actuators
import math
from robots import CustomRobot
from functools import partial

model = nengo.Network(label="omnibotarm", seed=13)

# Create a robot object that can have sensors and actuators added to it
# The 'sim_dt' parameter is the dt it is expecting V-REP to be run with
# this can be different than Nengo's dt and the difference is accounted
# for when the two simulators are set to be synchronized
omnibot = CustomRobot(sim_dt=0.05, nengo_dt=0.001, sync=True)

# When adding sensors and actuators, the string names given must match
# the names of the specific sensors and actuators in V-REP
# These names can be found in the Scene Hierarchy pane


# robot wheels
omnibot.add_actuator("OmniWheel", actuators.joint_velocity)
omnibot.add_actuator("OmniWheel#0", actuators.joint_velocity)
omnibot.add_actuator("OmniWheel#1", actuators.joint_velocity)
# robot arm
omnibot.add_actuator("PhantomXPincher", actuators.joint_positions,4)

model.config[nengo.Ensemble].neuron_type=nengo.LIF()
with model:
  # Create a Node that interfaces Nengo with V-REP
  robot = nengo.Node(omnibot, size_in=7, size_out=0)

  motors_population = nengo.Ensemble(n_neurons=100, dimensions=3, radius=3)
  servos_population = nengo.Ensemble(n_neurons=100, dimensions=4, radius=3)

  # Create a single slider to control the speed
  speed = nengo.Node([0]*3)
  joints = nengo.Node([0]*4)

  nengo.Connection(speed, motors_population, transform=[10, 10, 10])
  nengo.Connection(joints, servos_population)


  nengo.Connection(motors_population, robot[1:4])
  nengo.Connection(servos_population, robot[3:7])
