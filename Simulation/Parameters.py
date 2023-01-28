from Simulation.Distribution import DistributionGenerator, DistributionParameters


class SimulationParameters:
    def __init__(self, sim_id: int, t: float, r: float, e: float, bound: float, bin_size: float, d0_parameters: DistributionParameters, total_time_span: int, block_time_span: int, n_save_distributions_block: int, total_density_threshold: float, method: str):
        self.sim_id = sim_id
        self.t = t
        self.r = r
        self.e = e
        self.bound = bound
        self.bin_size = bin_size
        self.d = DistributionGenerator.get_distribution(bound=bound, bin_size=bin_size, dist_params=d0_parameters)
        self.d0_parameters = d0_parameters
        self.total_time_span = total_time_span
        self.block_time_span = block_time_span
        self.n_save_distributions_block = n_save_distributions_block
        self.total_density_threshold = total_density_threshold
        self.method = method

    def __str__(self):
        return f'(sim_id={self.sim_id}, t={self.t}, r={self.r}, e={self.e}, bound={self.bound}, bin_size={self.bin_size}, d0={self.d0_parameters.to_string()}, t_span={self.total_time_span},  block_t_span={self.block_time_span}, n_save={self.n_save_distributions_block}, density_thresh={self.total_density_threshold}, method={self.method})'

    def __repr__(self):
        return self.__str__()