from Database.Tables import GetTable
from ARMSimulation.ARMStatistics import ARMStatistics
from sqlalchemy.engine import Connection
from sqlalchemy import insert, select
import pandas as pd
from typing import List


class DBStatisticsARM:
    @staticmethod
    def get_arm_statistics(conn: Connection, sim_ids: List[int]) -> pd.DataFrame:
        arm_statistics_table = GetTable.get_arm_statistics_table()
        arm_sim_table = GetTable.get_arm_simulation_table()
        stmt = select(arm_statistics_table, arm_sim_table).join(arm_statistics_table,
                                                                arm_statistics_table.c.sim_id == arm_sim_table.c.sim_id).filter(
            arm_statistics_table.c.sim_id.in_(sim_ids))
        df = pd.read_sql(con=conn, sql=stmt)
        return df

    @staticmethod
    def insert_arm_statistics(conn: Connection, arm_statistics: ARMStatistics):
        table = GetTable.get_arm_statistics_table()
        stmt = insert(table).values(sim_id=arm_statistics.sim_id, end_variance=arm_statistics.end_var)
        conn.execute(stmt)
