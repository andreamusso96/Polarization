from Database.Tables import GetTable
from Database.Parameters import DBParameters
from Simulation.Parameters import SimulationParameters
from Simulation.Simulator import SimulationResult
from sqlalchemy import select, insert
from sqlalchemy.engine import Connection
import pandas as pd


class Result:
    def __init__(self, params: SimulationParameters, distributions_df: pd.DataFrame, l2_norm_df: pd.DataFrame):
        self.params = params
        self.distributions_df = distributions_df
        self.l2_norm_df = l2_norm_df


class DBResult:
    @staticmethod
    def get_simulation_result(conn: Connection, sim_id: int) -> Result:
        params = DBParameters.get_simulation_parameters(sim_id=sim_id)
        l2_norm_table = GetTable.get_l2_norm_table(sim_id=sim_id)
        distributions_table = GetTable.get_distributions_table(sim_id=sim_id)
        stmt_l2_norm = select(l2_norm_table)
        l2_norm_df = pd.read_sql_query(sql=stmt_l2_norm, con=conn)

        stmt_distributions = select(distributions_table)
        distributions_df = pd.read_sql_query(sql=stmt_distributions, con=conn)

        return Result(params=params, distributions_df=distributions_df, l2_norm_df=l2_norm_df)

    @staticmethod
    def insert_simulation_result(conn: Connection, sim_result: SimulationResult):
        DBResult.insert_result_in_l2_norm_table(conn=conn, simulation_result=sim_result)
        DBResult.insert_result_in_distribution_table(conn=conn, simulation_result=sim_result)


    @staticmethod
    def insert_result_in_l2_norm_table(conn: Connection, simulation_result: SimulationResult):
        l2_norm_table = GetTable.get_l2_norm_table(sim_id=simulation_result.params.sim_id)
        for s in simulation_result.l2_norm:
            stmt = insert(l2_norm_table).values(time=s, l2_norm=simulation_result.l2_norm[s])
            conn.execute(stmt)

    @staticmethod
    def insert_result_in_distribution_table(conn: Connection, simulation_result: SimulationResult):
        distributions_table = GetTable.get_distributions_table(sim_id=simulation_result.params.sim_id)
        for s in simulation_result.distributions:
            left_bins = simulation_result.distributions[s].bin_edges[:-1]
            dist_values = simulation_result.distributions[s].bin_probs
            for i in range(left_bins.shape[0]):
                stmt = insert(distributions_table).values(time=s, left_bin=left_bins[i], dist_value=dist_values[i])
                conn.execute(stmt)