
class ARMSimulationParameters:
    def __init__(self, sim_id: int, n: int, t: float, r: float, e: float, mean: float, std: float, n_steps: int, b: float or None, frequency_save: int):
        self.sim_id = sim_id
        self.n = n
        self.t = t
        self.r = r
        self.e = e
        self.mean = mean
        self.std = std
        self.n_steps = n_steps
        self.b = b
        self.frequency_save = frequency_save