from ARMSimulation.ARMAverageNSTDResult import ARMAverageNSTDResult
from ARMSimulation.ARMAverageNSTDParams import ARMAverageNSTDParams, ARMSimulationParameters
from Database.Tables import GetTable
from sqlalchemy.engine import Connection
from sqlalchemy import insert, select, update
import pandas as pd


class DBAverageNSTD:
    @staticmethod
    def get_average_nstd_table(conn: Connection) -> pd.DataFrame:
        avg_nstd_table = GetTable.get_average_nstd_table()
        stmt = select(avg_nstd_table)
        df = pd.read_sql(sql=stmt, con=conn)
        return df

    @staticmethod
    def get_average_nstd_params(conn: Connection, sim_id: int) -> ARMAverageNSTDParams:
        average_nstd_table = GetTable.get_average_nstd_table()
        stmt = select(average_nstd_table).where(average_nstd_table.c.sim_id == sim_id)
        res = conn.execute(stmt).first()
        params = DBAverageNSTD._table_row_to_parameters(row=res)
        return params

    @staticmethod
    def _table_row_to_parameters(row) -> ARMAverageNSTDParams:
        arm_params = ARMSimulationParameters(sim_id=row.sim_id, n=row.n, t=row.t, r=row.r, e=row.e, mean=row.mean, std=row.std,
                                    n_steps=row.n_steps, b=row.b, frequency_save=row.frequency_save)
        arm_avg_nstd_params = ARMAverageNSTDParams(arm_params=arm_params, n_runs=row.n_runs)
        return arm_avg_nstd_params


    @staticmethod
    def insert_average_nstd_params(conn: Connection, average_nstd_params: ARMAverageNSTDParams):
        avg_nstd_table = GetTable.get_average_nstd_table()
        arm_params = average_nstd_params.arm_params
        stmt = insert(avg_nstd_table).values(sim_id=average_nstd_params.sim_id, n=arm_params.n, t=arm_params.t, r=arm_params.r, e=arm_params.e,
                                             mean=arm_params.mean, std=arm_params.std, n_steps=arm_params.n_steps, b=arm_params.b,
                                             frequency_save=arm_params.frequency_save, complete=False,
                                             n_runs=average_nstd_params.n_runs)
        conn.execute(stmt)

    @staticmethod
    def insert_average_nstd_result(conn: Connection, average_nstd_result: ARMAverageNSTDResult):
        avg_nstd_table = GetTable.get_average_nstd_table()
        stmt = update(avg_nstd_table).values(nstd_mean=average_nstd_result.nstd_mean, nstd_std=average_nstd_result.nstd_std, complete=True).where(avg_nstd_table.c.sim_id == average_nstd_result.params.sim_id)
        conn.execute(stmt)