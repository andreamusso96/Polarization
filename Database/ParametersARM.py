from ARMSimulation.ARMParameters import ARMSimulationParameters
from Database.Tables import GetTable
from typing import List
from sqlalchemy import select, insert
from sqlalchemy.engine import Connection


class DBParametersARM:
    @staticmethod
    def get_simulation_parameters(conn: Connection, sim_ids: List[int]) -> List[ARMSimulationParameters]:
        arm_sim_table = GetTable.get_arm_simulation_table()
        stmt = select(arm_sim_table).where(arm_sim_table.c.sim_id.in_(sim_ids))
        res = conn.execute(stmt).all()
        params = []
        for row in res:
            p = DBParametersARM._arm_sim_table_row_to_parameters(row=row)
            params.append(p)
        return params

    @staticmethod
    def _arm_sim_table_row_to_parameters(row) -> ARMSimulationParameters:
        p = ARMSimulationParameters(sim_id=row.sim_id, n=row.n, t=row.t, r=row.r, e=row.e, mean=row.mean, std=row.std, n_steps=row.n_steps, b=row.b, frequency_save=row.frequency_save)
        return p

    @staticmethod
    def insert_parameters(conn: Connection, params: ARMSimulationParameters):
        arm_sim_table = GetTable.get_arm_simulation_table()
        stmt = insert(arm_sim_table).values(sim_id=params.sim_id, n=params.n, t=params.t, r=params.r, e=params.e, mean=params.mean, std=params.std, n_steps=params.n_steps, b=params.b, frequency_save=params.frequency_save, complete=False)
        conn.execute(stmt)
