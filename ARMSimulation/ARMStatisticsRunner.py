import time

from Database.DB import DB
import numpy as np
from config import is_cluster
import os


class ARMStatisticsRunner:
    @staticmethod
    def get_batches():
        batch_size = 80
        sim_ids = DB.get_sim_ids(arm=True)
        n_batches = int(np.ceil(len(sim_ids) / batch_size))
        complete_batches = np.array_split(sim_ids, n_batches)
        ends_batches = [(batch[0], batch[-1] + 1) for batch in complete_batches]
        return ends_batches

    @staticmethod
    def run():
        batches = ARMStatisticsRunner.get_batches()
        for batch in batches:
            if is_cluster:
                time_in_mins = 30
                args_sim = ['sbatch', f'--time={time_in_mins}', f'--wrap="python -m main_arm_stats {str(batch[0])} {str(batch[1])}"']
            else:
                args_sim = ['python', '-m', 'main_arm_stats', str(batch[0]), str(batch[1])]

            os.system(" ".join(args_sim))
            time.sleep(1)


if __name__ == '__main__':
    from Database.Tables import CreateTable, GetTable
    from Database.Engine import engine
    #GetTable.get_arm_statistics_table().drop(engine)
    CreateTable.create_arm_statistics_table()
    ARMStatisticsRunner.run()