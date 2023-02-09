from Simulation.Distribution import Distribution
from scipy.integrate import quad, fixed_quad, solve_ivp
from scipy.stats import rv_histogram
import numpy as np
from typing import Callable, List


class MasterEquation:
    def __init__(self, t: float, r: float, e: float, d0: Distribution):
        self.t = t
        self.r = r
        self.e = e
        self.d0 = d0

    def solve(self, time_span: int, time_steps_save: int, method: str):
        vectorized_integral = np.vectorize(MasterEquation.integral, excluded=set('q'))
        def fun(time, p): return MasterEquation.f(time=time, p=p, t=self.t, e=self.e, r=self.r, d0=self.d0, vectorized_integral=vectorized_integral)
        # solve_ivp complains it wants an Optional, but it works without a List too
        res = solve_ivp(fun=fun, t_span=(0, time_span), y0=self.d0.bin_probs, t_eval=time_steps_save, method=method)
        return res

    @staticmethod
    def integrand_simple(a: float, p: np.ndarray, x: float, e: float, r: float, d0: Distribution):
        q = rv_histogram((p, d0.bin_edges), density=True)
        return np.power(2, -1 * np.abs(a) / e) * q.pdf(x + a) * (q.pdf(x + 2 * a) - q.pdf(x))

    @staticmethod
    def integrand_attraction(a: float, q: rv_histogram, x: float, e: float, r: float) -> float:
        return np.power(2, -1 * np.abs(a) / r * e) * (q.pdf(x + a) * q.pdf(x + a - a / r) - q.pdf(x) * q.pdf(x + a / r))

    @staticmethod
    def integrand_repulsion(a: float, q: rv_histogram, x: float, e: float, r: float) -> float:
        return np.power(2, -1 * np.abs(a) / r * e) * (q.pdf(x + a) * q.pdf(x + a + a / r) - q.pdf(x) * q.pdf(x - a / r))

    @staticmethod
    def integral(x: float, q: rv_histogram, t: float, e: float, r: float, support: float) -> float:
        rt = r*t
        result0, abserr = fixed_quad(MasterEquation.integrand_attraction, a=-rt, b=rt, args=(q, x, e, r))
        result1, abserr = fixed_quad(MasterEquation.integrand_repulsion, a=rt, b=support, args=(q, x, e, r))
        result2, abserr = fixed_quad(MasterEquation.integrand_repulsion, a=-support, b=-rt, args=(q, x, e, r))
        return result0 + result1 + result2

    @staticmethod
    def f(time: float, p: np.ndarray, t: float, e: float, r: float, d0: Distribution, vectorized_integral: callable) -> np.ndarray:
        q = rv_histogram((p, d0.bin_edges), density=True)
        res = vectorized_integral(x=d0.bin_centers, q=q, t=t, e=e, r=r, support=d0.support)
        if d0.boundary is not None:
            res = MasterEquation.implement_boundary_condition(res=res, left_boundary_bin_index=d0.left_boundary_bin_index, right_boundary_bin_index=d0.right_boundary_bin_index, bin_size=d0.bin_size)
        return res

    @staticmethod
    def implement_boundary_condition(res: np.ndarray, left_boundary_bin_index: int, right_boundary_bin_index: int, bin_size: float) -> np.ndarray:
        res[left_boundary_bin_index] += np.sum(res[:left_boundary_bin_index] * bin_size)
        res[right_boundary_bin_index - 1] += np.sum(res[right_boundary_bin_index:] * bin_size)
        res[:left_boundary_bin_index] = 0
        res[right_boundary_bin_index:] = 0
        return res
