from Database.Tables import GetTable
from Database.Parameters import ParameterValue
from Stability.StabilityAnalysis import StabilityResult
from Database.SimIds import DBSimId
from sqlalchemy import insert, select
from sqlalchemy.engine import Connection
from typing import List


class DBStability:
    @staticmethod
    def insert_stability_result(conn: Connection, stability_result: StabilityResult) -> None:
        stability_table = GetTable.get_stability_stable()
        stmt = insert(stability_table).values(t=stability_result.t, r=stability_result.r, e=stability_result.e,
                                              max_eig=stability_result.max_eig, stable=stability_result.stable,
                                              max_frequency=stability_result.max_frequency,
                                              max_eigs_far_from_max_frequency=stability_result.max_eigs_far_from_max_frequency)
        conn.execute(stmt)

    @staticmethod
    def get_stability_results(conn: Connection, param_values: List[ParameterValue] = None) -> List[StabilityResult]:
        stability_table = GetTable.get_stability_stable()
        if param_values is None:
            stmt = select(stability_table)
        else:
            stmts = []
            for param_value in param_values:
                stmt = select(stability_table).where(getattr(stability_table.c, param_value.name) == param_value.value)
                stmts.append(stmt)
            stmt = DBSimId._set_operations_on_statements(stmts=stmts, method='intersection')

        res = conn.execute(stmt).all()

        stability_results = []
        for row in res:
            stability_result = DBStability._stability_table_row_to_stability_result(row=row)
            stability_results.append(stability_result)

        return stability_results

    @staticmethod
    def _stability_table_row_to_stability_result(row) -> StabilityResult:
        sr = StabilityResult(t=row.t, r=row.r, e=row.e, max_eig=row.max_eig, stable=row.stable, max_frequency=row.max_frequency,
                            max_eigs_far_from_max_frequency=row.max_eigs_far_from_max_frequency)
        return sr
