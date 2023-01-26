from Database.Tables import GetTable
from Database.Engine import engine
from Simulation.Parameters import SimulationParameters
from Simulation.Distribution import DistributionParameters
from sqlalchemy import select, insert


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
    def get_simulation_parameters(sim_id: int) -> SimulationParameters:
        sim_table = GetTable.get_simulation_table()
        with engine.begin() as conn:
            stmt = select(sim_table).where(sim_table.c.sim_id == sim_id)
            res = conn.execute(stmt).all()
            p = DBParameters._sim_table_row_to_parameters(row=res[0])

        return p

    @staticmethod
    def _sim_table_row_to_parameters(row) -> SimulationParameters:
        p = SimulationParameters(sim_id=row.sim_id, t=row.t, r=row.r, e=row.e, bound=row.bound, bin_size=row.bin_size,
                                 d0_parameters=DistributionParameters.from_string(row.d0_parameters), s_max=row.s_max,
                                 n_save_distributions=row.n_save_distributions, total_density_threshold=row.total_density_threshold)
        return p

    @staticmethod
    def insert_parameters(params: SimulationParameters):
        sim_table = GetTable.get_simulation_table()
        with engine.begin() as conn:
            stmt = insert(sim_table).values(sim_id=params.sim_id, t=params.t, r=params.r, e=params.e,
                                            s_max=params.s_max, bound=params.bound, bin_size=params.bin_size,
                                            n_save_distributions=params.n_save_distributions,
                                            total_density_threshold=params.total_density_threshold,
                                            d0_parameters=params.d0_parameters.to_string(), complete=False, success=False)
            conn.execute(stmt)