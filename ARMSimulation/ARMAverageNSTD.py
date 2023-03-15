from ARMSimulation.ARM import ARM
from ARMSimulation.ARMAverageNSTDParams import ARMAverageNSTDParams
from ARMSimulation.ARMAverageNSTDResult import ARMAverageNSTDResult
import numpy as np


class ARMAverageNSTD:
    def __init__(self, params: ARMAverageNSTDParams):
        self.params = params
        self.result = None

    def run(self) -> ARMAverageNSTDResult:
        nstds = []
        for i in range(self.params.n_runs):
            arm = ARM(sim_params=self.params.arm_params)
            result = arm.run_simulation()
            nvar = result.get_normalized_variance_final_opinion_distribution()
            nstds.append(np.sqrt(nvar))

        self.result = ARMAverageNSTDResult(params=self.params, nstd_mean=float(np.mean(nstds)), nstd_std=float(np.std(nstds)))
        return self.result

    def save_result(self):
        pass