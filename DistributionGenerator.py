import numpy as np
from MasterEquation import Distribution

from typing import Dict
import copy
import ast


class DistributionParameters:
    def __init__(self, name: str, sample_size: int, bin_size: float, ub: float, lb: float, params: Dict[str, float]):
        self.name = name
        self.sample_size = sample_size
        self.bin_size = bin_size
        self.ub = ub
        self.lb = lb
        self.params = params

    def to_string(self):
        temp_dict = copy.deepcopy(self.params)
        temp_dict['name'] = self.name
        temp_dict['sample_size'] = self.sample_size
        temp_dict['bin_size'] = self.bin_size
        temp_dict['ub'] = self.ub
        temp_dict['lb'] = self.lb
        return str(temp_dict)

    @staticmethod
    def from_string(string_parameters: str):
        dict_param = ast.literal_eval(string_parameters)
        name = dict_param['name']
        sample_size = dict_param['sample_size']
        bin_size = dict_param['bin_size']
        ub = dict_param['ub']
        lb = dict_param['lb']
        params = DistributionParameters._get_d0_params(dict_param=dict_param)
        return DistributionParameters(name=name, sample_size=sample_size, bin_size=bin_size, ub=ub, lb=lb,
                                      params=params)

    @staticmethod
    def _get_d0_params(dict_param: Dict) -> Dict[str, float]:
        keys_to_remove = ['name', 'sample_size', 'bin_size', 'ub', 'lb']
        d0_params = copy.deepcopy(dict_param)
        for k in keys_to_remove:
            del d0_params[k]

        return d0_params


class DistributionGenerator:
    @staticmethod
    def get_distribution(dist_params: DistributionParameters) -> Distribution:
        distribution_generating_function = getattr(DistributionGenerator, dist_params.name)
        return distribution_generating_function(dist_params)

    @staticmethod
    def get_bins(ub: float, lb: float, bin_size: float) -> np.ndarray:
        bins = np.arange(start=lb + bin_size, stop=ub + bin_size, step=bin_size)
        return bins

    @staticmethod
    def sample_to_distribution(sample: np.ndarray, ub: float, lb: float, bin_size: float) -> Distribution:
        bins = DistributionGenerator.get_bins(ub=ub, lb=lb, bin_size=bin_size)
        hist, _ = np.histogram(a=sample, bins=bins)
        d0 = hist / np.linalg.norm(hist, ord=1)
        d0 = np.insert(arr=d0, obj=[0, d0.shape[0]], values=[0, 0])
        d = Distribution(d0=d0, bin_size=bin_size)
        return d

    @staticmethod
    def uniform(dp: DistributionParameters) -> Distribution:
        sample = np.random.uniform(dp.lb, dp.ub, size=dp.sample_size)
        return DistributionGenerator.sample_to_distribution(sample=sample, ub=dp.ub, lb=dp.lb, bin_size=dp.bin_size)

    @staticmethod
    def normal(dp: DistributionParameters) -> Distribution:
        sample = DistributionGenerator._get_normal_sample(sample_size=dp.sample_size, **dp.params)
        return DistributionGenerator.sample_to_distribution(sample=sample, ub=dp.ub, lb=dp.lb, bin_size=dp.bin_size)

    @staticmethod
    def _get_normal_sample(sample_size: int, mean: float, std: float) -> np.ndarray:
        return np.random.normal(loc=mean, scale=std, size=sample_size)

    @staticmethod
    def exponential(dp: DistributionParameters) -> Distribution:
        sample = dp.lb + DistributionGenerator._get_exponential_sample(sample_size=dp.sample_size, **dp.params)
        return DistributionGenerator.sample_to_distribution(sample=sample, ub=dp.ub, lb=dp.lb, bin_size=dp.bin_size)

    @staticmethod
    def _get_exponential_sample(sample_size: int, scale: float) -> np.ndarray:
        return np.random.exponential(scale, size=sample_size)

    @staticmethod
    def bi_normal(dp: DistributionParameters) -> Distribution:
        sample = DistributionGenerator._get_bi_normal_sample(sample_size=dp.sample_size, **dp.params)
        return DistributionGenerator.sample_to_distribution(sample=sample, ub=dp.ub, lb=dp.lb, bin_size=dp.bin_size)

    @staticmethod
    def _get_bi_normal_sample(sample_size: int, mean1: float, std1: float, mean2: float, std2: float) -> np.ndarray:
        sample1 = np.random.normal(loc=mean1, scale=std1, size=int(sample_size / 2))
        sample2 = np.random.normal(loc=mean2, scale=std2, size=int(sample_size / 2))
        sample = np.append(sample1, sample2)
        return sample
