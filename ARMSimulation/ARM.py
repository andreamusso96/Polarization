from ARMSimulation.ARMInitialState import ARMInitialState
from ARMSimulation.ARMParameters import ARMSimulationParameters
from ARMSimulation.ARMResult import ARMSimulationResult
import numpy as np
from typing import Tuple


class ARM:
    def __init__(self, sim_params: ARMSimulationParameters):
        self.sim_params = sim_params
        self.n = sim_params.n
        self.t = sim_params.t
        self.r = sim_params.r
        self.e = sim_params.e
        self.s = ARMInitialState(mean=sim_params.mean, std=sim_params.std).generate(n=sim_params.n, b=sim_params.b)
        self.b = sim_params.b
        self.n_steps = sim_params.n_steps
        self.result = ARMSimulationResult(sim_params=sim_params)

    def run_simulation(self) -> ARMSimulationResult:
        for step in range(self.n_steps + 1):
            i, j = self.sample()
            d = self.distance(i, j)
            if np.random.uniform() < np.power(2, -d / self.e):
                self.update(i=i, j=j, d=d)

            self.result.save_state(step=step, s=self.s)

        return self.result

    def sample(self) -> Tuple[int, int]:
        i, j = np.random.choice(a=np.arange(self.n), size=2, replace=False)
        return i, j

    def update(self, i: int, j: int, d: float) -> None:
        if d < self.t:
            self.s[i] = self.s[i] + self.r * (self.s[j] - self.s[i])
        else:
            self.s[i] = self.s[i] - self.r * (self.s[j] - self.s[i])

        if self.b is not None:
            self.s[i] = max(-self.b, min(self.s[i], self.b))

    def distance(self, i: int, j: int) -> float:
        return np.abs(self.s[i] - self.s[j])