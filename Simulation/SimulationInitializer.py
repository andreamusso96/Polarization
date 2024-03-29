from Simulation.Distribution import DistributionParameters
from Simulation.Parameters import SimulationParameters
from Database.DB import DB

from typing import List, Tuple
import numpy as np


class SimulationInitializer:
    @staticmethod
    def get_sim_ids(n_sims: int) -> List[int]:
        try:
            last_sim_id = sorted(DB.get_sim_ids())[-1]
        except IndexError as e:
            last_sim_id = 0

        return list(range(last_sim_id+1, last_sim_id+1+n_sims))

    @staticmethod
    def get_methods() -> List[str]:
        return ['DOP853']

    @staticmethod
    def get_d0_parameters() -> List[DistributionParameters]:
        d0_params_bipolar = DistributionParameters(name='bipolar', params={'loc1': 1, 'scale1': 0.2, 'loc2': -1, 'scale2': 0.2})
        d0_params_normal = DistributionParameters(name='normal', params={'loc': 0, 'scale': 0.2})
        return [d0_params_normal, d0_params_bipolar]

    @staticmethod
    def get_other_params() -> Tuple[int, int, int, float, float, float or None, int]:
        total_time_span = 20
        block_time_span = 5
        n_save_distribution_block = 5
        support = 5
        bin_size = 0.005
        boundary = None
        num_processes = 1
        return total_time_span, n_save_distribution_block, block_time_span, support, bin_size, boundary, num_processes

    @staticmethod
    def get_other_params_test() -> Tuple[int, int, int, float, float, float or None, int]:
        total_time_span = 300
        block_time_span = 5
        n_save_distribution_block = 5
        support = 5
        bin_size = 0.005
        boundary = None
        num_processes = 1
        return total_time_span, n_save_distribution_block, block_time_span, support, bin_size, boundary, num_processes

    @staticmethod
    def get_ts_rs_es() -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        ts = np.array([0.1, 0.2, 0.3, 0.5, 0.8])
        rs = np.array([1])
        es = np.array([0.1, 0.3, 0.5, 0.7, 0.9])
        return ts, rs, es

    @staticmethod
    def get_ts_rs_es_test() -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        ts = np.array([0.2])
        rs = np.array([1])
        es = np.array([0.1])
        return ts, rs, es

    @staticmethod
    def get_simulation_parameters_list(test: bool) -> List:
        if test:
            ts, rs, es = SimulationInitializer.get_ts_rs_es_test()
            total_time_span, n_save_distribution_block, block_time_span, support, bin_size, boundary, num_processes = SimulationInitializer.get_other_params_test()
        else:
            ts, rs, es = SimulationInitializer.get_ts_rs_es()
            total_time_span, n_save_distribution_block, block_time_span, support, bin_size, boundary, num_processes = SimulationInitializer.get_other_params()

        methods = SimulationInitializer.get_methods()
        initial_distributions = SimulationInitializer.get_d0_parameters()
        n_sims = len(ts)*len(rs)*len(es)*len(initial_distributions)*len(methods)

        sim_ids = SimulationInitializer.get_sim_ids(n_sims=n_sims)
        simulation_parameters = []
        c = 0
        for t in ts:
            for r in rs:
                for e in es:
                    for d0_params in initial_distributions:
                        for method in methods:
                            sim_id = sim_ids[c]
                            sim_params = SimulationParameters(sim_id=sim_id, t=t, r=r, e=e, support=support, bin_size=bin_size, boundary=boundary, d0_parameters=d0_params, total_time_span=total_time_span, block_time_span=block_time_span, n_save_distributions_block=n_save_distribution_block, method=method, num_processes=num_processes)
                            simulation_parameters.append(sim_params)
                            c += 1

        return simulation_parameters

    @staticmethod
    def insert_simulation_parameters_in_db(test: bool = False):
        simulation_parameters_list = SimulationInitializer.get_simulation_parameters_list(test=test)
        for sim_param in simulation_parameters_list:
            DB.setup_database_for_simulation(params=sim_param)


def check_db():
    from Database.Tables import CreateTable, GetTable
    # CreateTable.create_simulation_table()
    # SimulationInitializer.insert_simulation_parameters_in_db(test=True)
    from Database.DB import engine
    from sqlalchemy import select
    import pandas as pd

    with engine.begin() as conn:
        table = GetTable.get_simulation_table()
        stmt = select(table)
        df = pd.read_sql(con=conn, sql=stmt)

    return df
if __name__ == '__main__':
    SimulationInitializer.insert_simulation_parameters_in_db(test=True)