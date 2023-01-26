from Database.Tables import GetTable
from Stability.StabilityAnalysis import StabilityResult
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
    def get_stability_result(conn: Connection, t: float, r: float, e: float) -> StabilityResult:
        stability_table = GetTable.get_stability_stable()
        stmt = select(stability_table).where(stability_table.c.t == t).where(stability_table.c.r == r).where(
            stability_table.c.e == e)
        res = conn.execute(stmt).all()[0]
        stability_result = DBStability._stability_table_row_to_stability_result(row=res)
        return stability_result

    @staticmethod
    def get_all_stability_results(conn: Connection) -> List[StabilityResult]:
        stability_table = GetTable.get_stability_stable()
        stmt = select(stability_table)
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
