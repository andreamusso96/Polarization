from Simulation.Simulator import Simulator
from Database.DB import DB

import sys

if __name__ == '__main__':
    sim_id = int(sys.argv[1])
    print('SIM ID', sim_id)
    params = DB.get_simulation_parameters(sim_ids=[sim_id])[0]
    simulation = Simulator(params=params)
    simulation.run_simulation()
    print('DONE', sim_id)

