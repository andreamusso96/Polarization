from DB import DB
from config import is_cluster

import os
import time


class SimulationRunner:
    @staticmethod
    def run_simulations():
        ids_sims_to_run = DB.get_ids_incomplete_simulations()
        ids_sims_to_run = ids_sims_to_run[:10]
        for sim_id in ids_sims_to_run:
            if is_cluster:
                time_in_mins = 20
                args_sim = ['sbatch', f'--time={time_in_mins}', f'--wrap="python -m main {str(sim_id)}"']
            else:
                args_sim = ['python', '-m', 'main', str(sim_id)]

            os.system(" ".join(args_sim))
            print('SUBMITTED', sim_id, 'COMMAND', " ".join(args_sim))
            time.sleep(1)


def check():
    incomp_sim = DB.get_parameters_incomplete_simulations()
    ids_incom_sim = DB.get_ids_incomplete_simulations()
    sim_id = 1
    sres = DB.get_simulation_result(sim_id=sim_id)
    return 0

if __name__ == '__main__':
    SimulationRunner.run_simulations()
    #check()