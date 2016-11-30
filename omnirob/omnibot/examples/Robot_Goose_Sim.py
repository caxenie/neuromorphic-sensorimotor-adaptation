#  create the simulator
def run_sim(t, nengo, model):
    with nengo.Simulator(model) as sim:
        sim.run(t)
