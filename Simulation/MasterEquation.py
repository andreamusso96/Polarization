from Simulation.Distribution import Distribution
from scipy.integrate import solve_ivp
import numpy as np
from Simulation.FastIntegration import parallelized_integral


class MasterEquation:
    def __init__(self, t: float, r: float, e: float, d0: Distribution):
        self.t = t
        self.r = r
        self.e = e
        self.d0 = d0

    def solve(self, time_span: int, time_steps_save: int, method: str, num_processes: int):
        def fun(time, p): return MasterEquation.f(time=time, p=p, t=self.t, e=self.e, r=self.r, d0=self.d0, num_processes=num_processes)
        # solve_ivp complains it wants an Optional, but it works without a List too
        res = solve_ivp(fun=fun, t_span=(0, time_span), y0=self.d0.bin_probs, t_eval=time_steps_save, method=method)
        return res

    @staticmethod
    def f(time: float, p: np.ndarray, t: float, e: float, r: float, d0: Distribution, num_processes: int) -> np.ndarray:
        res = parallelized_integral(x=d0.bin_centers, bin_probs=p, bin_edges=d0.bin_edges, t=t, e=e, r=r, support=d0.support, num_processes=num_processes)
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
