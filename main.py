from Simulation.Simulator import Simulator
from Database.DB import DB

import sys

if __name__ == '__main__':
    sim_id = int(sys.argv[ 1])
    print('SIM ID', sim_id)
    params = DB.get_simulation_parameters(sim_id=sim_id)
    simulation = Simulator(params=params)
    simulation_result = simulation.run_simulation()
    DB.insert_simulation_result(simulation_result=simulation_result)

