from scipy.stats import norm, uniform
import numpy as np
from typing import Dict, Tuple
import copy
import ast


class Distribution:
    def __init__(self, bin_probs: np.ndarray, bin_edges: np.ndarray, boundary: float):
        self.boundary = boundary
        self.bin_edges = bin_edges
        self.bin_probs = bin_probs
        self.bin_size = np.round(np.abs(bin_edges[0] - bin_edges[1]), decimals=5)
        self.support = bin_edges[-1]
        self.bin_centers = (self.bin_edges + self.bin_size / 2)[:-1]
        self.n_bins = len(bin_probs)

        if self.boundary is not None:
            self.left_boundary_bin_index, self.right_boundary_bin_index = self.get_boundary_bins_indices()

    def get_boundary_bins_indices(self) -> Tuple[int, int]:
        left_boundary_bin_index = np.searchsorted(self.bin_edges, -self.boundary, side='left')
        right_boundary_bin_index = np.searchsorted(self.bin_edges, self.boundary, side='left')
        return left_boundary_bin_index, right_boundary_bin_index


class DistributionParameters:
    def __init__(self, name: str, params: Dict[str, float]):
        self.name = name
        self.params = params

    def to_string(self) -> str:
        d = {'name': self.name, **self.params}
        return str(d)

    @staticmethod
    def from_string(string_parameters: str):
        dict_param = ast.literal_eval(string_parameters)
        name = dict_param['name']
        params = DistributionParameters._get_d0_params(dict_param=dict_param)
        return DistributionParameters(name=name, params=params)

    @staticmethod
    def _get_d0_params(dict_param: Dict) -> Dict[str, float]:
        keys_to_remove = ['name']
        d0_params = copy.deepcopy(dict_param)
        for k in keys_to_remove:
            del d0_params[k]

        return d0_params


class DistributionGenerator:
    @staticmethod
    def get_distribution(support: float, bin_size: float, dist_params: DistributionParameters, boundary: float = None) -> Distribution:
        distribution_generating_function = getattr(DistributionGenerator, dist_params.name)
        return distribution_generating_function(support, bin_size, dist_params, boundary)

    @staticmethod
    def get_bins(support: float, bin_size: float) -> np.ndarray:
        bins = np.round(np.arange(start=-support, stop=support + bin_size, step=bin_size), decimals=3)
        return bins

    @staticmethod
    def normal(support: float, bin_size: float, dp: DistributionParameters, boundary: float) -> Distribution:
        bin_edges = DistributionGenerator.get_bins(support=support, bin_size=bin_size)
        norm_rv = norm(**dp.params)
        bin_probs = norm_rv.pdf(bin_edges[1:])
        d = Distribution(bin_probs=bin_probs, bin_edges=bin_edges, boundary=boundary)
        return d

    @staticmethod
    def uniform(support: float, bin_size: float, dp: DistributionParameters, boundary: float) -> Distribution:
        bin_edges = DistributionGenerator.get_bins(support=support, bin_size=bin_size)
        uniform_rv = uniform(**dp.params)
        bin_probs = uniform_rv.pdf(bin_edges[1:])
        d = Distribution(bin_probs=bin_probs, bin_edges=bin_edges, boundary=boundary)
        return d

    @staticmethod
    def bipolar(support: float, bin_size: float, dp: DistributionParameters, boundary: float) -> Distribution:
        bin_edges = DistributionGenerator.get_bins(support=support, bin_size=bin_size)
        loc1, scale1 = dp.params['loc1'], dp.params['scale1']
        loc2, scale2 = dp.params['loc2'], dp.params['scale2']
        norm_rv1 = norm(loc=loc1, scale=scale1)
        norm_rv2 = norm(loc=loc2, scale=scale2)
        bin_probs = 0.5 * (norm_rv1.pdf(bin_edges[1:]) + norm_rv2.pdf(bin_edges[1:]))
        d = Distribution(bin_probs=bin_probs, bin_edges=bin_edges, boundary=boundary)
        return d

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    support = 3
    bin_size = 0.1
    dp = DistributionParameters(name='bipolar', params={'loc1': 1, 'scale1': 0.2, 'loc2': -1, 'scale2': 0.2})
    d = DistributionGenerator.get_distribution(support=support, bin_size=bin_size, dist_params=dp, boundary=None)
    plt.plot(d.bin_centers, d.bin_probs)
    print(np.sum(d.bin_probs * d.bin_size))
    plt.show()