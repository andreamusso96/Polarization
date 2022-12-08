from MasterEquation import MasterEquation, Distribution
from DistributionGenerator import DistributionParameters, DistributionGenerator

import copy
from typing import Dict, List
import numpy as np
from tqdm import tqdm


class Parameters:
    def __init__(self, sim_id: int, t: float, r: float, e: float, d0_parameters: DistributionParameters, s_max: int, n_save_distributions: int):
        self.sim_id = sim_id
        self.t = t
        self.r = r
        self.e = e
        self.d = DistributionGenerator.get_distribution(dist_params=d0_parameters)
        self.d0_parameters = d0_parameters
        self.s_max = s_max
        self.n_save_distributions = n_save_distributions

    def __str__(self):
        return f'(sim_id={self.sim_id}, t={self.t}, r={self.r}, e={self.e}, d0={self.d0_parameters.to_string()}, s_max={self.s_max}, n_save={self.n_save_distributions})'

    def __repr__(self):
        return self.__str__()


class SimulationResult:
    def __init__(self, params: Parameters):
        self.params = params
        self.interval_save_distribution = int(np.round(params.s_max / params.n_save_distributions, decimals=0))
        self.distributions: Dict[int, Distribution] = {}
        self.l2_norm: List[float] = []

    def save_step(self, d: Distribution, s: int):
        self.save_l2_norm(d=d)
        self.save_distribution(d=d, s=s)

    def save_l2_norm(self, d: Distribution):
        self.l2_norm.append(float(np.sum(np.square(d.d))))

    def save_distribution(self, d: Distribution, s: int):
        if s % self.interval_save_distribution == 0:
            self.distributions[s] = copy.deepcopy(d)


class Simulation:
    def __init__(self, params: Parameters):
        self.params = params
        self.me = MasterEquation(t=params.t, r=params.r, e=params.e, d=params.d)
        self.sim_result = SimulationResult(params=params)

    def run_simulation(self):
        for s in tqdm(range(self.params.s_max)):
            d = self.me.step()
            self.sim_result.save_step(d=d, s=s)

        return self.sim_result
