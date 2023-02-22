from ARMSimulation.ARMParameters import ARMSimulationParameters
import numpy as np
import pandas as pd


class ARMSimulationResult:
    def __init__(self, sim_params: ARMSimulationParameters, states: np.ndarray = None):
        self.sim_params = sim_params
        if states is None:
            n_save = int(sim_params.n_steps/sim_params.frequency_save) + 1
            self.states = np.zeros(shape=(n_save, sim_params.n))
            self.time_steps = np.arange(0, sim_params.n_steps + 1, sim_params.frequency_save)
        else:
            self.states = states[:, :-1]
            self.time_steps = states[:, -1]
        self.counter = 0

    def save_state(self, step: int, s: np.ndarray) -> None:
        if step % self.sim_params.frequency_save == 0:
            self.states[self.counter, :] = s.copy()
            self.counter += 1

    def result_as_df(self):
        result = pd.DataFrame(self.states, columns=list(range(0, self.sim_params.n)))
        result['step'] = self.time_steps
        return result

    def get_normalized_variance_last_step(self):
        last_step = self.states[-1]
        min_last_step = np.min(last_step)
        max_last_step = np.max(last_step)
        max_possible_variance = (max_last_step - min_last_step) ** 2
        var_last_step = np.var(last_step)
        if np.round(var_last_step, decimals=1) == 0:
            return 0
        else:
            return var_last_step / max_possible_variance
