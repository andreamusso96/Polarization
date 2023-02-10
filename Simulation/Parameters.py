from Simulation.Distribution import DistributionGenerator, DistributionParameters


class SimulationParameters:
    def __init__(self, sim_id: int, t: float, r: float, e: float, support: float, bin_size: float, boundary: float or None, d0_parameters: DistributionParameters, total_time_span: int, block_time_span: int, n_save_distributions_block: int, method: str, num_processes: int):
        self.sim_id = sim_id
        self.t = t
        self.r = r
        self.e = e
        self.support = support
        self.bin_size = bin_size
        self.boundary = boundary
        self.d = DistributionGenerator.get_distribution(support=support, bin_size=bin_size, dist_params=d0_parameters, boundary=boundary)
        self.d0_parameters = d0_parameters
        self.total_time_span = total_time_span
        self.block_time_span = block_time_span
        self.n_save_distributions_block = n_save_distributions_block
        self.method = method
        self.num_processes = num_processes

    def __str__(self):
        return f'(sim_id={self.sim_id}, t={self.t}, r={self.r}, e={self.e}, support={self.support}, bin_size={self.bin_size}, boundary={self.boundary}, d0={self.d0_parameters.to_string()}, t_span={self.total_time_span},  block_t_span={self.block_time_span}, n_save={self.n_save_distributions_block}, method={self.method})'

    def __repr__(self):
        return self.__str__()