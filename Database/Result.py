from Database.Tables import GetTable
from Database.Parameters import DBParameters
from Simulation.SimulationResult import SimulationResult
from sqlalchemy import select
from sqlalchemy.engine import Connection
import pandas as pd


class DBResult:
    @staticmethod
    def get_simulation_result(conn: Connection, sim_id: int) -> SimulationResult:
        params = DBParameters.get_simulation_parameters(conn=conn, sim_ids=[sim_id])[0]
        distributions_table = GetTable.get_distributions_table(sim_id=sim_id)
        stmt_distributions = select(distributions_table)
        distributions_df = pd.read_sql_query(sql=stmt_distributions, con=conn)
        return SimulationResult(params=params, distributions_df=distributions_df)

    @staticmethod
    def insert_result_in_distribution_table(conn: Connection, simulation_result: SimulationResult):
        distributions_table = GetTable.get_distributions_table(sim_id=simulation_result.params.sim_id)
        simulation_result.distributions_df.to_sql(con=conn, name=distributions_table.name, if_exists='append', index=False)