from Simulation.MasterEquation import MasterEquation
from Simulation.Parameters import SimulationParameters
from Simulation.Distribution import Distribution
from Simulation.SimulationResult import SimulationResult
import pandas as pd
import numpy as np


class Simulator:
    def __init__(self, params: SimulationParameters):
        self.params = params
        self.me = MasterEquation(t=params.t, r=params.r, e=params.e, d0=params.d)
        self.time_steps_save_distribution = np.arange(0, self.params.total_time_span + 1)

    def run_simulation(self) -> None:
        current_t = 0
        current_d = self.params.d
        while current_t < self.params.total_time_span:
            res_scipy = self.solve_block(current_t=current_t, current_d=current_d)
            self.save_partial_result(res_scipy=res_scipy, current_t=current_t)
            current_t += self.params.block_time_span
            current_d = self.get_current_d(res_scipy=res_scipy)

    def solve_block(self, current_t: int, current_d: Distribution):
        me = MasterEquation(t=params.t, r=params.r, e=params.e, d0=current_d)
        time_steps_save_distribution_block = self.get_time_steps_save_distributions_block(current_t=current_t)
        res_scipy = me.solve(time_span=current_t + self.params.block_time_span,
                             time_steps_save=time_steps_save_distribution_block,
                             total_density_threshold=self.params.total_density_threshold, method=self.params.method)
        return res_scipy

    def get_current_d(self, res_scipy):
        bin_probs = res_scipy.y[:, -1]
        bin_edges = DistributionGenerator.get_bins(bound=self.params.bound, bin_size=self.params.bin_size)
        return Distribution(bin_probs=bin_probs, bin_edges=bin_edges)

    def save_partial_result(self, res_scipy, current_t: int):
        distributions_df = self.get_distributions_df(res_scipy=res_scipy, t_start=current_t)
        sim_result = SimulationResult(params=self.params, distributions_df=distributions_df)
        DB.insert_simulation_result_in_distribution_table(simulation_result=sim_result)

    def get_distributions_df(self, res_scipy, t_start: int) -> pd.DataFrame:
        dfs = []
        for i in range(len(res_scipy.t)):
            time = t_start + int(res_scipy.t[i])
            bin_probs = res_scipy.y[:, i]
            bin_edges = DistributionGenerator.get_bins(bound=self.params.bound, bin_size=self.params.bin_size)
            data = np.vstack((time*np.ones(len(bin_probs)), bin_edges[:-1], bin_probs)).T
            df_time = pd.DataFrame(data=data, columns=['time', 'left_bin', 'dist_value'])
            dfs.append(df_time)

        distributions_df = pd.concat(dfs, ignore_index=True)
        return distributions_df

    def get_time_steps_save_distributions_block(self, current_t):
        a = self.time_steps_save_distribution[self.time_steps_save_distribution > current_t]
        time_steps_save_distribution_block = a[a <= current_t + self.params.block_time_span]
        if current_t == 0:
            time_steps_save_distribution_block = np.insert(time_steps_save_distribution_block, 0, 0.0)
        return time_steps_save_distribution_block - current_t



if __name__ == '__main__':
    from Simulation.Distribution import DistributionGenerator, DistributionParameters
    from Database.DB import DB

    bound = 10
    bin_size = 0.1
    dist_params = DistributionParameters(name='normal', params={'loc': 0, 'scale': 0.2})
    total_time_span = 10
    n_save_distributions_block = 5
    block_time_span = 5
    total_density_threshold = 0.8
    method = 'DOP853'
    params = SimulationParameters(sim_id=1, t=0.2, r=1, e=0.5, bound=bound, bin_size=bin_size,
                                  d0_parameters=dist_params,
                                  total_time_span=total_time_span, n_save_distributions_block=n_save_distributions_block,
                                  block_time_span=block_time_span,
                                  total_density_threshold=total_density_threshold, method=method)
    s = Simulator(params=params)
    res = s.run_simulation()

