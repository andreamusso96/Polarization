from ARMSimulation.ARMStatistics import ARMStatistics
from Database.DB import DB
from typing import List
from tqdm import tqdm

class ARMStatisticsCalculator:
    @staticmethod
    def save_arm_end_variance(sim_ids: List[int]):
        for sim_id in tqdm(sim_ids):
            try:
                result = DB.get_arm_result(sim_id=sim_id)
                end_var = result.get_normalized_variance_last_step()
                arm_stats = ARMStatistics(sim_id=sim_id, end_var=end_var)
                DB.insert_arm_statistics(arm_statistics=arm_stats)
            except Exception as e:
                print('Error in sim_id: ', sim_id)
                print(e)


if __name__ == '__main__':
    from Database.Tables import CreateTable, GetTable
    from Database.Engine import engine
    #GetTable.get_arm_statistics_table().drop(engine)
    CreateTable.create_arm_statistics_table()
    ARMStatisticsCalculator.save_arm_end_variance(sim_ids=DB.get_sim_ids(arm=True))