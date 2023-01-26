from Simulation.Distribution import DistributionGenerator, DistributionParameters


class SimulationParameters:
    def __init__(self, sim_id: int, t: float, r: float, e: float, bound: float, bin_size: float, d0_parameters: DistributionParameters, s_max: int, n_save_distributions: int, total_density_threshold: float):
        self.sim_id = sim_id
        self.t = t
        self.r = r
        self.e = e
        self.bound = bound
        self.bin_size = bin_size
        self.d = DistributionGenerator.get_distribution(bound=bound, bin_size=bin_size, dist_params=d0_parameters)
        self.d0_parameters = d0_parameters
        self.s_max = s_max
        self.n_save_distributions = n_save_distributions
        self.total_density_threshold = total_density_threshold

    def __str__(self):
        return f'(sim_id={self.sim_id}, t={self.t}, r={self.r}, e={self.e}, bound={self.bound}, bin_size={self.bin_size}, d0={self.d0_parameters.to_string()}, s_max={self.s_max}, n_save={self.n_save_distributions}, density_thresh={self.density_threshold})'

    def __repr__(self):
        return self.__str__()