from ARMSimulation.ARMResult import ARMSimulationResult
from Database.Tables import GetTable
from Database.ParametersARM import DBParametersARM
from sqlalchemy.engine import Connection
from sqlalchemy import select, update
import pandas as pd


class DBResultARM:
    table_name = "arm_result"

    @staticmethod
    def get_result(conn: Connection, sim_id: int):
        arm_result_table = GetTable.get_table(table_name=f"{DBResultARM.table_name}_{sim_id}")
        stmt_distributions = select(arm_result_table)
        arm_result_df = pd.read_sql_query(sql=stmt_distributions, con=conn)
        params = DBParametersARM.get_simulation_parameters(conn=conn, sim_ids=[sim_id])[0]
        arm_result = ARMSimulationResult(sim_params=params, states=arm_result_df.values)
        return arm_result

    @staticmethod
    def insert_arm_result_in_table(conn: Connection, arm_simulation_result: ARMSimulationResult):
        sim_id = arm_simulation_result.sim_params.sim_id
        result_as_df = arm_simulation_result.result_as_df()
        result_as_df.to_sql(con=conn, name=f"{DBResultARM.table_name}_{sim_id}", index=False)
        DBResultARM._set_arm_simulation_complete_flag(conn=conn, sim_id=sim_id)

    @staticmethod
    def _set_arm_simulation_complete_flag(conn: Connection, sim_id: int):
        arm_simulation_table = GetTable.get_arm_simulation_table()
        stmt = update(arm_simulation_table).values(complete=True).where(arm_simulation_table.c.sim_id == sim_id)
        conn.execute(stmt)