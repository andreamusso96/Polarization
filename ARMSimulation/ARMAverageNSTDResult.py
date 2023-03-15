from ARMSimulation.ARMAverageNSTDParams import ARMAverageNSTDParams


class ARMAverageNSTDResult:
    def __init__(self, params: ARMAverageNSTDParams,  nstd_mean: float, nstd_std: float):
        self.params = params
        self.nstd_mean = nstd_mean
        self.nstd_std = nstd_std
