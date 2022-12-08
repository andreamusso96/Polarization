from DistributionGenerator import DistributionParameters
from Simulation import Parameters
from DB import DB

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
        sample_size = 10 ** 5
        bin_size = 0.05
        ub = 0.5
        lb = -0.5
        params = {'mean': 0, 'std': 0.2}
        d0_params_normal = DistributionParameters(name='normal', sample_size=sample_size, bin_size=bin_size, ub=ub, lb=lb, params=params)
        return [d0_params_normal]

    @staticmethod
    def get_other_params() -> Tuple[int, int]:
        s_max = 10**3
        n_save_distribution = 10**2
        return s_max, n_save_distribution

    @staticmethod
    def get_ts_rs_es() -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        num = 10
        ts = np.linspace(0.1, 1, num=num)
        rs = np.linspace(0.1, 1, num=num)
        es = np.linspace(0.1, 1, num=num)
        return ts, rs, es

    @staticmethod
    def get_simulation_parameters_list() -> List:
        ts, rs, es = SimulationInitializer.get_ts_rs_es()
        s_max, n_save_distribution = SimulationInitializer.get_other_params()
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
                        sim_params = Parameters(sim_id=sim_id, t=t, r=r, e=e, d0_parameters=d0_params, s_max=s_max, n_save_distributions=n_save_distribution)
                        simulation_parameters.append(sim_params)
                        c += 1

        return simulation_parameters

    @staticmethod
    def insert_simulation_parameters_in_db():
        simulation_parameters_list = SimulationInitializer.get_simulation_parameters_list()
        for sim_param in simulation_parameters_list:
            DB.insert_simulation_parameters(simulation_parameters=sim_param)


if __name__ == '__main__':
    SimulationInitializer.insert_simulation_parameters_in_db()