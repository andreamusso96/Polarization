from DB import DB
from config import is_cluster

import os
import time
import numpy as np


class SimulationRunner:
    @staticmethod
    def run_simulations():
        ids_sims_to_run = DB.get_ids_incomplete_simulations()
        for sim_id in ids_sims_to_run:
            if is_cluster:
                time_in_mins = 30
                args_sim = ['sbatch', f'--time={time_in_mins}', f'--wrap="python -m main {str(sim_id)}"']
            else:
                args_sim = ['python', '-m', 'main', str(sim_id)]

            os.system(" ".join(args_sim))
            print('SUBMITTED', sim_id, 'COMMAND', " ".join(args_sim))
            time.sleep(0.5)


def check():
    ids_incom_sim = DB.get_ids_incomplete_simulations()
    sim_id = [1,2,3,4,5]
    for s in sim_id:
        sres = DB.get_simulation_result(sim_id=s)
    return 0

if __name__ == '__main__':
    SimulationRunner.run_simulations()
    #check()