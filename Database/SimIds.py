from Database.Tables import GetTable
from Database.Parameters import ParameterRange, ParameterValue
from sqlalchemy import select, union, intersect
from sqlalchemy.engine import Connection
from typing import List


class DBSimId:
    @staticmethod
    def get_all_sim_ids(conn: Connection) -> List[int]:
        sim_table = GetTable.get_simulation_table()
        stmt = select(sim_table.c.sim_id)
        res = conn.execute(stmt).scalars().all()
        return res

    @staticmethod
    def get_last_sim_id(conn: Connection) -> int:
        sim_table = GetTable.get_simulation_table()
        stmt = select(sim_table.c.sim_id)
        res = conn.execute(stmt).scalars().all()
        last_sim_id = sorted(res)[-1]
        return last_sim_id

    @staticmethod
    def get_ids_with_parameter_value(conn: Connection, param_value: ParameterValue) -> List[int]:
        sim_table = GetTable.get_simulation_table()
        stmt = select(sim_table.c.sim_id).where(getattr(sim_table.c, param_value.name) == param_value.value)
        sim_ids = conn.execute(stmt).scalars().all()
        return sim_ids

    @staticmethod
    def get_ids_in_parameter_ranges(conn: Connection, param_ranges: List[ParameterRange], method: str) -> List[int]:
        sim_table = GetTable.get_simulation_table()
        select_stmts = []
        for r in param_ranges:
            stmt = select(sim_table.c.sim_id).where(getattr(sim_table.c, r.name) >= r.min_val).where(
                getattr(sim_table.c, r.name) < r.max_val)
            select_stmts.append(stmt)

        if method == 'intersection':
            stmt = intersect(*select_stmts)
        elif method == 'union':
            stmt = union(*select_stmts)
        else:
            class InvalidMethod(Exception):
                def __init__(self, message):
                    super().__init__(message)

            raise InvalidMethod(f"The method provided {method} is not valid")

        sim_ids = conn.execute(stmt).scalars().all()
        return sim_ids