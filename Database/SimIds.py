from Database.Tables import GetTable
from Database.Parameters import ParameterRange, ParameterValue
from sqlalchemy import select, union, intersect, Table
from sqlalchemy.engine import Connection
from typing import List


class DBSimId:
    @staticmethod
    def get_sim_ids(conn: Connection, arm: bool = False, param_ranges: List[ParameterRange] = None, param_values: List[ParameterValue] = None, method: str = 'intersection') -> List[int]:
        if not arm:
            table = GetTable.get_simulation_table()
        else:
            table = GetTable.get_arm_simulation_table()

        if param_ranges is None and param_values is None:
            stmt = select(table.c.sim_id)
        elif param_ranges is None and param_values is not None:
            stmt = DBSimId._set_operations_on_statements(
                stmts=DBSimId._get_stmts_for_parameter_values(sim_table=table, param_values=param_values),
                method=method)
        elif param_ranges is not None and param_values is None:
            stmt = DBSimId._set_operations_on_statements(
                stmts=DBSimId._get_stmts_for_parameter_ranges(sim_table=table, param_ranges=param_ranges),
                method=method)
        else:
            stmts_param_ranges = DBSimId._get_stmts_for_parameter_ranges(sim_table=table, param_ranges=param_ranges)
            stmts_param_values = DBSimId._get_stmts_for_parameter_values(sim_table=table, param_values=param_values)
            stmt = DBSimId._set_operations_on_statements(stmts=stmts_param_ranges + stmts_param_values, method=method)

        ids = conn.execute(stmt).scalars().all()
        return ids

    @staticmethod
    def _get_stmts_for_parameter_ranges(sim_table: Table, param_ranges: List[ParameterRange]) -> List[select]:
        stmts = []
        for r in param_ranges:
            stmt = select(sim_table.c.sim_id).where(getattr(sim_table.c, r.name) >= r.min_val).where(
                getattr(sim_table.c, r.name) < r.max_val)
            stmts.append(stmt)
        return stmts

    @staticmethod
    def _get_stmts_for_parameter_values(sim_table: Table, param_values: List[ParameterValue]) -> List[select]:
        stmts = []
        for v in param_values:
            stmt = select(sim_table.c.sim_id).where(getattr(sim_table.c, v.name) == v.value)
            stmts.append(stmt)
        return stmts

    @staticmethod
    def _set_operations_on_statements(stmts: List[select], method: str) -> select:
        if method == 'intersection':
            stmt = intersect(*stmts)
        elif method == 'union':
            stmt = union(*stmts)
        else:
            class InvalidMethod(Exception):
                def __init__(self, message):
                    super().__init__(message)

            raise InvalidMethod(f"The method provided {method} is not valid")
        return stmt