from config import is_cluster
from Database.DB import DB, ParameterValue
import os
import time


class SimulationRunner:
    @staticmethod
    def get_ids_incomplete_simulations():
        ids_incomplete_simulations = DB.get_sim_ids(param_values=[ParameterValue(name='complete', value=False)])
        return ids_incomplete_simulations

    @staticmethod
    def run_simulations():
        ids_sims_to_run = SimulationRunner.get_ids_incomplete_simulations()
        for sim_id in ids_sims_to_run:
            if is_cluster:
                time_in_mins = 10*60
                args_sim = ['sbatch', f'--time={time_in_mins}', f'--wrap="python -m main {str(sim_id)}"']
            else:
                args_sim = ['python', '-m', 'main', str(sim_id)]

            os.system(" ".join(args_sim))
            print('SUBMITTED', sim_id, 'COMMAND', " ".join(args_sim))
            time.sleep(0.5)


if __name__ == '__main__':
    SimulationRunner.run_simulations()