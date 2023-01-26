from scipy.stats import norm, uniform
import numpy as np
from typing import Dict
import copy
import ast


class Distribution:
    def __init__(self, bin_probs: np.ndarray, bin_edges: np.ndarray):
        self.bin_size = np.abs(bin_edges[0] - bin_edges[1])
        self.bound = bin_edges[-1]
        self.bin_edges = bin_edges
        self.bin_probs = bin_probs
        self.bin_centers = (self.bin_edges + self.bin_size / 2)[:-1]


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
    def get_distribution(bound: float, bin_size: float, dist_params: DistributionParameters) -> Distribution:
        distribution_generating_function = getattr(DistributionGenerator, dist_params.name)
        return distribution_generating_function(bound, bin_size, dist_params)

    @staticmethod
    def get_bins(bound: float, bin_size: float) -> np.ndarray:
        bins = np.round(np.arange(start=-bound, stop=bound + bin_size, step=bin_size), decimals=2)
        return bins

    @staticmethod
    def normal(bound: float, bin_size: float, dp: DistributionParameters) -> Distribution:
        bin_edges = DistributionGenerator.get_bins(bound=bound, bin_size=bin_size)
        norm_rv = norm(**dp.params)
        bin_probs = norm_rv.pdf(bin_edges[1:])
        d = Distribution(bin_probs=bin_probs, bin_edges=bin_edges)
        return d

    @staticmethod
    def uniform(bound: float, bin_size: float, dp: DistributionParameters) -> Distribution:
        bin_edges = DistributionGenerator.get_bins(bound=bound, bin_size=bin_size)
        uniform_rv = uniform(**dp.params)
        bin_probs = uniform_rv.pdf(bin_edges[1:])
        d = Distribution(bin_probs=bin_probs, bin_edges=bin_edges)
        return d
