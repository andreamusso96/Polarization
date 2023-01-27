import copy

from Simulation.MasterEquation import MasterEquation
from Simulation.Parameters import SimulationParameters
from Simulation.Distribution import Distribution, DistributionGenerator

from typing import Dict, List
import numpy as np


class SimulationResult:
    def __init__(self, params: SimulationParameters, res_scipy):
        self.params = params
        self.res_scipy = res_scipy
        self.distributions: Dict[int, Distribution] = self.get_distributions()
        self.l2_norm: Dict[int, float] = self.get_l2_norm()

    def get_distributions(self) -> Dict[int, Distribution]:
        distributions = {}
        for i in range(len(self.res_scipy.t)):
            time = int(self.res_scipy.t[i])
            bin_probs = self.res_scipy.y[:, i]
            bin_edges = DistributionGenerator.get_bins(bound=self.params.bound, bin_size=self.params.bin_size)
            distribution = Distribution(bin_probs=bin_probs, bin_edges=bin_edges)
            distributions[time] = distribution
        return distributions

    def get_l2_norm(self) -> Dict[int, float]:
        l2_norms = {}
        for time in self.res_scipy.t:
            dist = self.distributions[int(time)]
            l2_norm = float(np.sum(np.square(dist.bin_probs) * self.params.bin_size))
            l2_norms[int(time)] = l2_norm

        return l2_norms


class Simulator:
    def __init__(self, params: SimulationParameters):
        self.params = params
        self.me = MasterEquation(t=params.t, r=params.r, e=params.e, d0=params.d)

    def run_simulation(self) -> SimulationResult:
        res_scipy = self.me.solve(s_max=self.params.s_max, n_save_distributions=self.params.n_save_distributions, total_density_threshold=self.params.total_density_threshold, method=self.params.method)
        sim_result = SimulationResult(params=self.params, res_scipy=res_scipy)
        return sim_result


if __name__ == '__main__':
    from Simulation.Distribution import DistributionGenerator, DistributionParameters
    from Database.DB import DB

    bound = 10
    bin_size = 0.05
    dist_params = DistributionParameters(name='normal', params={'loc': 0, 'scale': 0.2})
    s_max = 50
    n_save_distributions = 10
    total_density_threshold = 0.7
    method = 'LSODA'
    params = SimulationParameters(sim_id=12, t=0.2, r=1, e=0.5, bound=bound, bin_size=bin_size,
                                  d0_parameters=dist_params,
                                  s_max=s_max, n_save_distributions=n_save_distributions, total_density_threshold=total_density_threshold, method=method)
    s = Simulator(params=params)
    res = s.run_simulation()
    DB.insert_simulation_result(simulation_result=res)

