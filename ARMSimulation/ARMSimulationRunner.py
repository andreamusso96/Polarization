from config import is_cluster
from Database.DB import DB, ParameterValue
import os
import time


class ARMSimulationRunner:
    @staticmethod
    def get_params_incomplete_simulations():
        ids_incomplete_simulations = DB.get_arm_sim_ids(incomplete=True)
        params = DB.get_arm_parameters(sim_ids=ids_incomplete_simulations)
        return params

    @staticmethod
    def run_simulations():
        params_sims_to_run = ARMSimulationRunner.get_params_incomplete_simulations()
        batch_size = 401
        counter = 0
        for p in params_sims_to_run:
            if 0.09 < p.e < 0.11 or 0.29 < p.e < 0.31:
                sim_id = p.sim_id
                if is_cluster:
                    time_in_mins = 60
                    args_sim = ['sbatch', f'--time={time_in_mins}', f'--wrap="python -m main_arm {str(sim_id)}"']
                else:
                    args_sim = ['python', '-m', 'main_arm', str(sim_id)]

                os.system(" ".join(args_sim))
                print('SUBMITTED', sim_id, 'COMMAND', " ".join(args_sim))
                time.sleep(0.5)
                counter += 1

            if counter % batch_size == 0:
                time.sleep(600)


if __name__ == '__main__':
    ARMSimulationRunner.run_simulations()