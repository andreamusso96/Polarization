from Database.Tables import GetTable
from Simulation.Parameters import SimulationParameters
from Simulation.Distribution import DistributionParameters
from sqlalchemy import select, insert
from sqlalchemy.engine import Connection


class ParameterValue:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class ParameterRange:
    def __init__(self, name: str, min_val, max_val):
        self.name = name
        self.min_val = min_val
        self.max_val = max_val


class DBParameters:
    @staticmethod
    def get_simulation_parameters(conn: Connection, sim_id: int) -> SimulationParameters:
        sim_table = GetTable.get_simulation_table()
        stmt = select(sim_table).where(sim_table.c.sim_id == sim_id)
        res = conn.execute(stmt).all()
        p = DBParameters._sim_table_row_to_parameters(row=res[0])
        return p

    @staticmethod
    def _sim_table_row_to_parameters(row) -> SimulationParameters:
        p = SimulationParameters(sim_id=row.sim_id, t=row.t, r=row.r, e=row.e, support=row.support, bin_size=row.bin_size, boundary=row.boundary,
                                 d0_parameters=DistributionParameters.from_string(row.d0_parameters), total_time_span=row.total_time_span,
                                 block_time_span=row.block_time_span,
                                 n_save_distributions_block=row.n_save_distributions_block, method=row.method)
        return p

    @staticmethod
    def insert_parameters(conn: Connection, params: SimulationParameters):
        sim_table = GetTable.get_simulation_table()
        stmt = insert(sim_table).values(sim_id=params.sim_id, t=params.t, r=params.r, e=params.e,
                                        total_time_span=params.total_time_span,
                                        block_time_span=params.block_time_span,
                                        n_save_distributions_block=params.n_save_distributions_block,
                                        support=params.support, bin_size=params.bin_size, boundary=params.boundary,
                                        method=params.method,
                                        d0_parameters=params.d0_parameters.to_string(), complete=False, success=False)
        conn.execute(stmt)
