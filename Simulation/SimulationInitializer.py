from Simulation.Distribution import DistributionParameters
from Simulation.Parameters import SimulationParameters
from Database.DB import DB

from typing import List, Tuple
import numpy as np


class SimulationInitializerHighVarianceSimulations:
    @staticmethod
    def get_ids() -> List[int]:
        return [18, 27, 31, 32, 33, 34, 52, 53, 81, 96, 109, 111, 119, 127, 128, 129, 130, 133, 135, 136, 143, 144]


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
        params = {'loc': 0, 'scale': 0.2}
        d0_params_normal = DistributionParameters(name='normal', params=params)
        return [d0_params_normal]

    @staticmethod
    def get_other_params() -> Tuple[int, int, int, float, float, float or None]:
        total_time_span = 10**2
        block_time_span = 10
        n_save_distribution_block = 10
        support = 5
        bin_size = 0.01
        boundary = None
        return total_time_span, n_save_distribution_block, block_time_span, support, bin_size, boundary

    @staticmethod
    def get_other_params_test() -> Tuple[int, int, int, float, float, float or None]:
        total_time_span = 10
        block_time_span = 10
        n_save_distribution_block = 5
        support = 5
        bin_size = 0.01
        boundary = None
        return total_time_span, n_save_distribution_block, block_time_span, support, bin_size, boundary

    @staticmethod
    def get_ts_rs_es() -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        ts = np.linspace(0.1, 0.7, num=7)
        rs = np.linspace(0.3, 1, num=8)
        es = np.array([0.2, 0.5, 0.8])
        return ts, rs, es

    @staticmethod
    def get_ts_rs_es_test() -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        ts = np.array([0.2, 0.7])
        rs = np.array([1, 0.3])
        es = np.array([0.2, 0.8])
        return ts, rs, es

    @staticmethod
    def get_simulation_parameters_list(test: bool) -> List:
        if test:
            ts, rs, es = SimulationInitializer.get_ts_rs_es_test()
            total_time_span, n_save_distribution_block, block_time_span, support, bin_size, boundary = SimulationInitializer.get_other_params_test()
        else:
            ts, rs, es = SimulationInitializer.get_ts_rs_es()
            total_time_span, n_save_distribution_block, block_time_span, support, bin_size, boundary = SimulationInitializer.get_other_params()

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
                            sim_params = SimulationParameters(sim_id=sim_id, t=t, r=r, e=e, support=support, bin_size=bin_size, boundary=boundary, d0_parameters=d0_params, total_time_span=total_time_span, block_time_span=block_time_span, n_save_distributions_block=n_save_distribution_block, method=method)
                            simulation_parameters.append(sim_params)
                            c += 1

        return simulation_parameters

    @staticmethod
    def insert_simulation_parameters_in_db(test: bool = False):
        simulation_parameters_list = SimulationInitializer.get_simulation_parameters_list(test=test)
        for sim_param in simulation_parameters_list:
            DB.setup_database_for_simulation(params=sim_param)


if __name__ == '__main__':
    from Database.Tables import CreateTable
    CreateTable.create_simulation_table()
    SimulationInitializer.insert_simulation_parameters_in_db(test=True)