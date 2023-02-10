from Simulation.Distribution import Distribution
from scipy.integrate import solve_ivp
import numpy as np
from Simulation.FastIntegration import vectorized_integral
from typing import List


class MasterEquation:
    def __init__(self, t: float, r: float, e: float, d0: Distribution):
        self.t = t
        self.r = r
        self.e = e
        self.d0 = d0

        rt = self.r * self.t
        lb, ub = tuple(np.searchsorted(d0.bin_edges, np.array([-rt, rt])))
        self.support_a = d0.bin_centers[lb:ub]
        support_r_side = d0.bin_centers[ub:]
        self.support_r = np.concatenate((-support_r_side[::-1], support_r_side))

    def solve(self, time_span: int, time_steps_save: List[int], method: str):
        def fun(time, p): return MasterEquation.f(time=time, p=p, support_a=self.support_a, support_r=self.support_r, e=self.e, r=self.r, d0=self.d0)
        res = solve_ivp(fun=fun, t_span=(0, time_span), y0=self.d0.bin_probs, t_eval=time_steps_save, method=method)
        return res

    @staticmethod
    def f(time: float, p: np.ndarray, support_a: np.ndarray, support_r: np.ndarray, e: float, r: float, d0: Distribution) -> np.ndarray:
        res = vectorized_integral(x=d0.bin_centers, bin_probs=p, bin_edges=d0.bin_edges, bin_size=d0.bin_size, support_a=support_a, support_r=support_r, e=e, r=r)
        if d0.boundary is not None:
            res = MasterEquation.implement_boundary_condition(res=res, left_boundary_bin_index=d0.left_boundary_bin_index, right_boundary_bin_index=d0.right_boundary_bin_index, bin_size=d0.bin_size)
        return np.round(res, decimals=16)

    @staticmethod
    def implement_boundary_condition(res: np.ndarray, left_boundary_bin_index: int, right_boundary_bin_index: int, bin_size: float) -> np.ndarray:
        res[left_boundary_bin_index] += np.sum(res[:left_boundary_bin_index] * bin_size)
        res[right_boundary_bin_index - 1] += np.sum(res[right_boundary_bin_index:] * bin_size)
        res[:left_boundary_bin_index] = 0
        res[right_boundary_bin_index:] = 0
        return res
