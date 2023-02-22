from config import is_cluster
from Database.DB import DB, ParameterValue
import os
import time
import numpy as np


class ARMSimulationRunner:
    @staticmethod
    def get_sim_id_batches():
        batch_size = 80
        ids_incomplete_simulations = DB.get_sim_ids(arm=True, param_values=[ParameterValue(name='complete', value=False)])
        n_batches = int(np.ceil(len(ids_incomplete_simulations) / batch_size))
        complete_batches = np.array_split(ids_incomplete_simulations, n_batches)
        ends_batches = [(batch[0], batch[-1] + 1) for batch in complete_batches]
        return ends_batches

    @staticmethod
    def run_simulations():
        ids_batches = ARMSimulationRunner.get_sim_id_batches()
        for batch in ids_batches:
            if is_cluster:
                time_in_mins = 4*60 - 2
                args_sim = ['sbatch', f'--time={time_in_mins}', f'--wrap="python -m main_arm {str(batch[0])} {str(batch[1])}"']
            else:
                args_sim = ['python', '-m', 'main_arm', str(batch[0]), str(batch[1])]

            os.system(" ".join(args_sim))
            print('SUBMITTED', str(batch[0]), str(batch[1]), 'COMMAND', " ".join(args_sim))
            time.sleep(10)


if __name__ == '__main__':
    ARMSimulationRunner.run_simulations()