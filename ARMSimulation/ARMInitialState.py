import numpy as np


class ARMInitialState:
    def __init__(self, mean: float, std: float):
        self.mean = mean
        self.std = std

    def generate(self, n: int, b: float or None) -> np.ndarray:
        s = np.random.normal(loc=self.mean, scale=self.std, size=n)
        if b is not None:
            s = np.where(s > b, b, s)
            s = np.where(s < -b, -b, s)
        return s