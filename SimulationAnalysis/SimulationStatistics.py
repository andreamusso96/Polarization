
class SimulationStatistics:
    def __init__(self, sim_id: int, l2_norm_diff: float, l2_norm_end: float):
        self.sim_id = sim_id
        self.l2_norm_diff = l2_norm_diff
        self.l2_norm_end = l2_norm_end