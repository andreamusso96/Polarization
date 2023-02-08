from Database.Tables import GetTable
from SimulationAnalysis.SimulationStatistics import SimulationStatistics
from sqlalchemy import insert, select
from sqlalchemy.engine import Connection
from typing import List
import pandas as pd


class DBStatistics:
    @staticmethod
    def get_simulation_statistics(conn: Connection, sim_ids: List[int]) -> pd.DataFrame:
        sim_statistics_table = GetTable.get_simulation_statistics_table()
        stmt = select(sim_statistics_table).where(sim_statistics_table.c.sim_id.in_(sim_ids))
        df = pd.read_sql(sql=stmt, con=conn)
        return df

    @staticmethod
    def insert_simulation_statistics(conn: Connection, simulation_statistics: SimulationStatistics):
        sim_statistics_table = GetTable.get_simulation_statistics_table()
        stmt = insert(sim_statistics_table).values(sim_id=simulation_statistics.sim_id,
                                                   l2_norm_end=simulation_statistics.l2_norm_end,
                                                   l2_norm_diff=simulation_statistics.l2_norm_diff)
        conn.execute(stmt)