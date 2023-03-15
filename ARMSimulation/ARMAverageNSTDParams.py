from ARMSimulation.ARMParameters import ARMSimulationParameters
import pandas as pd


class ARMAverageNSTDParams:
    def __init__(self, arm_params: ARMSimulationParameters, n_runs: int):
        self.sim_id = arm_params.sim_id
        self.arm_params = arm_params
        self.n_runs = n_runs