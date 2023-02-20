from config import is_cluster
from Database.DB import DB, ParameterValue
import os
import time


class SimulationRunner:
    @staticmethod
    def get_params_incomplete_simulations():
        ids_incomplete_simulations = DB.get_sim_ids(param_values=[ParameterValue(name='complete', value=False)])
        params = DB.get_simulation_parameters(sim_ids=ids_incomplete_simulations)
        return params

    @staticmethod
    def run_simulations():
        params_sims_to_run = SimulationRunner.get_params_incomplete_simulations()
        for p in params_sims_to_run:
            sim_id = p.sim_id
            if is_cluster:
                time_in_mins = 10*60
                cpus_per_task = p.num_processes
                args_sim = ['sbatch', f'--time={time_in_mins}', f'--cpus-per-task={cpus_per_task}', f'--wrap="python -m main {str(sim_id)}"']
            else:
                args_sim = ['python', '-m', 'main', str(sim_id)]

            os.system(" ".join(args_sim))
            print('SUBMITTED', sim_id, 'COMMAND', " ".join(args_sim))
            time.sleep(0.5)


if __name__ == '__main__':
    SimulationRunner.run_simulations()