from Stability.EigenvalueCalculator import EigenvalueCalculator
import numpy as np


class StabilityResult:
    def __init__(self, t: float, r: float, e: float, max_eig: float, stable: bool, max_frequency: int, max_eigs_far_from_max_frequency: bool):
        self.t = t
        self.r = r
        self.e = e
        self.max_eig = max_eig
        self.stable = stable
        self.max_frequency = max_frequency
        self.max_eigs_far_from_max_frequency = max_eigs_far_from_max_frequency


class StabilityAnalysis:
    def __init__(self, t: float, r: float, e: float):
        self.t = t
        self.r = r
        self.e = e
        self.eigenvalue_calculator = EigenvalueCalculator(t=self.t, r=self.r, e=self.e)

    def get_stability_analysis(self, max_frequency):
        eigs = self.get_eigs(max_frequency=max_frequency)
        max_eig = np.max(eigs)
        stable = self.is_stable(max_eig=max_eig)
        max_eigs_far_from_max_frequency = self.max_eigs_far_from_max_frequency(eigs=eigs)
        return StabilityResult(t=self.t, r=self.r, e=self.e, max_eig=max_eig, stable=stable,
                               max_frequency=max_frequency,
                               max_eigs_far_from_max_frequency=max_eigs_far_from_max_frequency)

    def get_eigs(self, max_frequency: int) -> np.ndarray:
        ks = range(0, max_frequency)
        eigs = []
        for k in ks:
            eig = self.eigenvalue_calculator.get_eigenvalue(k=k)
            eigs.append(eig)

        return np.array(eigs)

    @staticmethod
    def is_stable(max_eig: float):
        return not np.round(max_eig, decimals=12) > 0

    @staticmethod
    def max_eigs_far_from_max_frequency(eigs: np.ndarray):
        return len(eigs) - np.argmax(eigs) > 0.1*len(eigs)



