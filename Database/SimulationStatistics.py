from Database.Tables import GetTable
from SimulationAnalysis.SimulationStatistics import SimulationStatistics
from sqlalchemy import insert, select
from sqlalchemy.engine import Connection


class DBStatistics:
    @staticmethod
    def get_simulation_statistics(conn: Connection, sim_id: int) -> SimulationStatistics:
        l2_norm_table = GetTable.get_l2_norm_table(sim_id=sim_id)
        stmt_l2_norm_end = select(l2_norm_table.c.l2_norm).order_by(l2_norm_table.c.time.desc())
        l2_norm_end = conn.execute(stmt_l2_norm_end).scalars().first()

        stmt_l2_norm_beginning = select(l2_norm_table.c.l2_norm).order_by(l2_norm_table.c.time.asc())
        l2_norm_beginning = conn.execute(stmt_l2_norm_beginning).scalars().first()

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