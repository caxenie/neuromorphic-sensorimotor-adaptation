# A omnirob with arm performing motor babbling
# Scene File: omni3wheel1arm_model.ttt
import nengo
import sensors
import actuators
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
omnibot.add_actuator("OmniWheel", actuators.joint_torque)
omnibot.add_actuator("OmniWheel#0", actuators.joint_torque)
omnibot.add_actuator("OmniWheel#1", actuators.joint_torque)
# robot arm
omnibot.add_actuator("PhantomXPincher_joint2", actuators.joint_torque)
omnibot.add_actuator("PhantomXPincher_joint3", actuators.joint_torque)
omnibot.add_actuator("PhantomXPincher_joint4", actuators.joint_torque)
omnibot.add_actuator("PhantomXPincher_joint5", actuators.joint_torque)


model.config[nengo.Ensemble].neuron_type=nengo.LIF()
with model:
  # Create a Node that interfaces Nengo with V-REP
  robot = nengo.Node(omnibot, size_in=7, size_out=0)

  motors = nengo.Ensemble(n_neurons=100, dimensions=3, radius=3)
  servos = nengo.Ensemble(n_neurons=100, dimensions=4, radius=3)

  # Create a single slider to control the speed
  speed = nengo.Node([0])
  joints = nengo.Node([0])

  nengo.Connection(speed, motors, transform=[[1],[2],[10]])
  nengo.Connection(joints, servos,  transform=[[1],[20],[1],[40]])


  nengo.Connection(motors, robot[1:4])
  nengo.Connection(servos, robot[3:7])
