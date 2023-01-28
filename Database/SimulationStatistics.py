from Database.Tables import GetTable
from Database.Result import DBResult
from SimulationAnalysis.SimulationStatistics import SimulationStatistics
from sqlalchemy import insert
from sqlalchemy.engine import Connection


class DBStatistics:
    @staticmethod
    def get_simulation_statistics(conn: Connection, sim_id: int) -> SimulationStatistics:
        result = DBResult.get_simulation_result(conn=conn, sim_id=sim_id)
        l2_norm_df = result.get_l2_norm_df()
        l2_norm_beginning = l2_norm_df.iloc[0]['l2_norm']
        l2_norm_end = l2_norm_df.iloc[-1]['l2_norm']
        sim_stats = SimulationStatistics(sim_id=sim_id, l2_norm_end=l2_norm_end,
                                         l2_norm_diff=l2_norm_beginning - l2_norm_end)

        return sim_stats

    @staticmethod
    def insert_simulation_statistics(conn: Connection, simulation_statistics: SimulationStatistics):
        sim_statistics_table = GetTable.get_simulation_statistics_table()
        stmt = insert(sim_statistics_table).values(sim_id=simulation_statistics.sim_id,
                                                   l2_norm_end=simulation_statistics.l2_norm_end,
                                                   l2_norm_diff=simulation_statistics.l2_norm_diff)
        conn.execute(stmt)