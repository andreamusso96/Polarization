from Database.DB import DB, ParameterValue
from config import is_cluster
from typing import List
import os
import time


class ARMAverageNSTDRunner:
    @staticmethod
    def get_sim_ids() -> List[int]:
        sim_table_df = DB.get_average_nstd_table()
        sim_table_df = sim_table_df[sim_table_df['complete'] == False]
        sim_ids = list(sim_table_df['sim_id'].values)
        return sim_ids

    @staticmethod
    def run():
        sim_ids = ARMAverageNSTDRunner.get_sim_ids()
        for sid in sim_ids:
            if is_cluster:
                time_in_mins = 50
                args_sim = ['sbatch', f'--time={time_in_mins}', f'--wrap="python -m main_avg_nstd {str(sid)}"']
            else:
                args_sim = ['python', '-m', 'main_avg_nstd', str(sid)]

            os.system(" ".join(args_sim))
            time.sleep(1)


if __name__ == '__main__':
    ARMAverageNSTDRunner.run()