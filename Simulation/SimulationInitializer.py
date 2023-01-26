from Simulation.Distribution import DistributionParameters
from Simulation.Parameters import SimulationParameters
from Database.DB import DB

from typing import List, Tuple
import numpy as np


class SimulationInitializer:
    @staticmethod
    def get_sim_ids(n_sims: int) -> List[int]:
        try:
            last_sim_id = DB.get_last_sim_id()
        except IndexError as e:
            last_sim_id = 0

        return list(range(last_sim_id+1, last_sim_id+1+n_sims))

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
        bin_size = 0.05
        total_density_threshold = 0.8
        return s_max, n_save_distribution, bound, bin_size, total_density_threshold

    @staticmethod
    def get_ts_rs_es() -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        num = 7
        ts = np.linspace(0.1, 0.7, num=num)
        rs = np.array([1]) #np.linspace(0.1, 1, num=num)
        es = np.array([0.5]) #np.linspace(0.1, 1, num=num)
        return ts, rs, es

    @staticmethod
    def get_simulation_parameters_list() -> List:
        ts, rs, es = SimulationInitializer.get_ts_rs_es()
        s_max, n_save_distribution, bound, bin_size, total_density_threshold = SimulationInitializer.get_other_params()
        initial_distributions = SimulationInitializer.get_d0_parameters()
        n_sims = len(ts)*len(rs)*len(es)*len(initial_distributions)
        sim_ids = SimulationInitializer.get_sim_ids(n_sims=n_sims)

        simulation_parameters = []
        c = 0
        for t in ts:
            for r in rs:
                for e in es:
                    for d0_params in initial_distributions:
                        sim_id = sim_ids[c]
                        sim_params = SimulationParameters(sim_id=sim_id, t=t, r=r, e=e, bound=bound, bin_size=bin_size, d0_parameters=d0_params, s_max=s_max, n_save_distributions=n_save_distribution, total_density_threshold=total_density_threshold)
                        simulation_parameters.append(sim_params)
                        c += 1

        return simulation_parameters

    @staticmethod
    def insert_simulation_parameters_in_db():
        simulation_parameters_list = SimulationInitializer.get_simulation_parameters_list()
        for sim_param in simulation_parameters_list:
            DB.insert_simulation_parameters(simulation_parameters=sim_param)


if __name__ == '__main__':
    from Database.Tables import CreateTable
    CreateTable.create_simulation_table()
    CreateTable.create_simulation_statistics_table()
    SimulationInitializer.insert_simulation_parameters_in_db()