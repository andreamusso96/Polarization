import numpy as np

from ARMSimulation.ARMStatistics import ARMStatistics
from Database.DB import DB
from typing import List
from tqdm import tqdm


class ARMStatisticsCalculator:
    @staticmethod
    def save_arm_stats(sim_ids: List[int]):
        for sim_id in sim_ids:
            try:
                result = DB.get_arm_result(sim_id=sim_id)
                end_var = result.get_normalized_variance_final_opinion_distribution()
                arm_stats = ARMStatistics(sim_id=sim_id, end_var=end_var)
                DB.insert_arm_statistics(arm_statistics=arm_stats)
            except Exception as e:
                print('ERROR', sim_id, e)


if __name__ == '__main__':
    from Database.Tables import CreateTable, GetTable
    from Database.Engine import engine
    #GetTable.get_arm_statistics_table().drop(engine)
    CreateTable.create_arm_statistics_table()
    ARMStatisticsCalculator.save_arm_stats(sim_ids=DB.get_sim_ids(arm=True))