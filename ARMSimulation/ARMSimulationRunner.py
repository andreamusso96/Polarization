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
        n_sims = len(ids_incomplete_simulations)
        n_batches = int(np.ceil(n_sims / batch_size))
        batches = []
        for batch_number in range(n_batches):
            batch_start = batch_number * batch_size
            batch_start_end = min((batch_number + 1) * batch_size, n_sims + 1)
            ids_batch = ids_incomplete_simulations[batch_start:batch_start_end]
            sorted_ids_batch = sorted(ids_batch)
            batches.append((sorted_ids_batch[0], sorted_ids_batch[-1]))
        # The last batch we need to get the last sim id
        batches[-1] = (batches[-1][0], batches[-1][1] + 1)
        return batches

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