from Simulation import Simulation
from DB import DB

import sys

if __name__ == '__main__':
    sim_id = int(sys.argv[ 1])
    print('SIM ID', sim_id)
    params = DB.get_parameters_simulation(sim_id=sim_id)
    simulation = Simulation(params=params)
    simulation_result = simulation.run_simulation()
    DB.insert_simulation_result(simulation_result=simulation_result)

