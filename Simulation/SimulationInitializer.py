from Simulation.Distribution import DistributionParameters
from Simulation.Parameters import SimulationParameters
from Database.DB import DB, engine

from typing import List, Tuple
import numpy as np


class SimulationInitializerHighVarianceSimulations:
    @staticmethod
    def get_ids() -> List[int]:
        return [18, 27, 31, 32, 33, 34, 52, 53, 81, 96, 109, 111, 119, 127, 128, 129, 130, 133, 135, 136, 143, 144]

    @staticmethod
    def get_params():
        ids = SimulationInitializerHighVarianceSimulations.get_ids()
        params = [DB.get_simulation_parameters(sim_id=sim_id) for sim_id in ids]
        return SimulationInitializerHighVarianceSimulations.change_ids(params=params, shift=1000)

    @staticmethod
    def get_modified_params():
        params = SimulationInitializerHighVarianceSimulations.get_params()
        modified_params = []
        for p in params:
            p.bin_size = 0.01
            modified_params.append(p)
        return SimulationInitializerHighVarianceSimulations.change_ids(params=params, shift=2000)

    @staticmethod
    def change_ids(params: List[SimulationParameters], shift: int) -> List[SimulationParameters]:
        for p in params:
            p.sim_id = p.sim_id + shift
        return params

    @staticmethod
    def insert_simulation_parameters_in_db():
        simulation_parameters_list = SimulationInitializerHighVarianceSimulations.get_params()
        simulation_parameters_list += SimulationInitializerHighVarianceSimulations.get_modified_params()
        for sim_param in simulation_parameters_list:
            DB.insert_simulation_parameters(simulation_parameters=sim_param)


class SimulationInitializer:
    @staticmethod
    def get_sim_ids(n_sims: int) -> List[int]:
        try:
            last_sim_id = DB.get_last_sim_id()
        except IndexError as e:
            last_sim_id = 0

        return list(range(last_sim_id+1, last_sim_id+1+n_sims))

    @staticmethod
    def get_methods() -> List[str]:
        return ['BDF', 'LSODA']

    @staticmethod
    def get_d0_parameters() -> List[DistributionParameters]:
        params = {'loc': 0, 'scale': 0.2}
        d0_params_normal = DistributionParameters(name='normal', params=params)
        return [d0_params_normal]

    @staticmethod
    def get_other_params() -> Tuple[int, int, float, float, float]:
        s_max = 10**2
        n_save_distribution = 10**2
        bound = 10.0
        bin_size = 0.005
        total_density_threshold = 0.8
        return s_max, n_save_distribution, bound, bin_size, total_density_threshold

    @staticmethod
    def get_other_params_test() -> Tuple[int, int, float, float, float]:
        s_max = 10
        n_save_distribution = 10
        bound = 10.0
        bin_size = 0.1
        total_density_threshold = 0.8
        return s_max, n_save_distribution, bound, bin_size, total_density_threshold

    @staticmethod
    def get_ts_rs_es() -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        ts = np.linspace(0.1, 0.7, num=7)
        rs = np.linspace(0.3, 1, num=8)
        es = np.array([0.2, 0.5, 0.8])
        return ts, rs, es

    @staticmethod
    def get_ts_rs_es_test() -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        ts = np.array([0.2])
        rs = np.array([1])
        es = np.array([0.5])
        return ts, rs, es

    @staticmethod
    def get_simulation_parameters_list(test: bool) -> List:
        if test:
            ts, rs, es = SimulationInitializer.get_ts_rs_es_test()
            s_max, n_save_distribution, bound, bin_size, total_density_threshold = SimulationInitializer.get_other_params_test()
        else:
            ts, rs, es = SimulationInitializer.get_ts_rs_es()
            s_max, n_save_distribution, bound, bin_size, total_density_threshold = SimulationInitializer.get_other_params()

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
                            sim_params = SimulationParameters(sim_id=sim_id, t=t, r=r, e=e, bound=bound, bin_size=bin_size, d0_parameters=d0_params, s_max=s_max, n_save_distributions=n_save_distribution, total_density_threshold=total_density_threshold, method=method)
                            simulation_parameters.append(sim_params)
                            c += 1

        return simulation_parameters

    @staticmethod
    def insert_simulation_parameters_in_db(test: bool = False):
        simulation_parameters_list = SimulationInitializer.get_simulation_parameters_list(test=test)
        for sim_param in simulation_parameters_list:
            DB.insert_simulation_parameters(simulation_parameters=sim_param)


if __name__ == '__main__':
    from Database.Tables import CreateTable
    CreateTable.create_simulation_table()
    SimulationInitializer.insert_simulation_parameters_in_db(test=False)