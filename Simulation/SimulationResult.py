from Simulation.Parameters import SimulationParameters
import pandas as pd
import numpy as np


class SimulationResult:
    def __init__(self, params: SimulationParameters, distributions_df: pd.DataFrame):
        self.params = params
        self.distributions_df = distributions_df

    def get_l2_norm_df(self) -> pd.DataFrame:
        l2_norms = self.distributions_df.groupby('time').apply(lambda df: np.sum(np.square(df['dist_value'])*self.params.bin_size)).values
        times = np.unique(self.distributions_df['time'].values)
        l2_norm_df = pd.DataFrame({'time': times, 'l2_norm': l2_norms})
        return l2_norm_df