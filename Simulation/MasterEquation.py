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
        setattr(MasterEquation, 'bin_size', self.d0.bin_size)

    def solve(self, s_max: int, n_save_distributions: int, total_density_threshold: float, method: str):
        vectorized_integral = np.vectorize(MasterEquation.integral, excluded=set('p'))
        t_eval = np.round(np.linspace(0, s_max, n_save_distributions), decimals=0)
        def fun(time, p): return MasterEquation.f(time=time, p=p, t=self.t, e=self.e, r=self.r, d0=self.d0, vectorized_integral=vectorized_integral)
        events = self.get_events(total_density_threshold=total_density_threshold, max_density_threshold=0.2)
        # solve_ivp complains it wants an Optional but it works without a List too
        res = solve_ivp(fun=fun, t_span=(0, s_max), y0=self.d0.bin_probs, t_eval=t_eval, events=events, method=method)
        return res

    def get_events(self, total_density_threshold: float, max_density_threshold: float) -> List[Callable]:
        def event_total_density(time, p): return MasterEquation.low_total_density_event(time=time, p=p, bin_size=self.d0.bin_size, threshold=total_density_threshold)
        def event_max_density(time, p): return MasterEquation.low_max_density_event(time=time, p=p, threshold=max_density_threshold)
        event_total_density.terminal = True
        event_max_density.terminal = True
        events = [event_total_density, event_max_density]

        return events
    @staticmethod
    def integrand_simple(a: float, p: np.ndarray, x: float, e: float, r: float, d0: Distribution):
        q = rv_histogram((p, d0.bin_edges), density=True)
        return np.power(2, -1 * np.abs(a) / e) * q.pdf(x + a) * (q.pdf(x + 2 * a) - q.pdf(x))

    @staticmethod
    def integrand(a: float, p: np.ndarray, x: float, e: float, r: float, d0: Distribution) -> float:
        q = rv_histogram((p, d0.bin_edges), density=True)
        attraction = np.power(2, -1 * np.abs(a) / r*e) * (q.pdf(x + a) * q.pdf(x + a - a/r) - q.pdf(x)*q.pdf(x + a/r))
        repulsion = np.power(2, -1 * np.abs(a) / r*e) * (q.pdf(x + a) * q.pdf(x + a + a/r) - q.pdf(x)*q.pdf(x - a/r))
        return attraction + repulsion

    @staticmethod
    def integral(x: float, p: np.ndarray, t: float, e: float, r: float, d0: Distribution) -> float:
        rt = r*t
        result0, abserr = fixed_quad(MasterEquation.integrand, a=-rt, b=rt, args=(p, x, e, r, d0))
        result1, abserr = fixed_quad(MasterEquation.integrand, a=rt, b=d0.bound, args=(p, x, e, r, d0))
        result2, abserr = fixed_quad(MasterEquation.integrand, a=-d0.bound, b=-rt, args=(p, x, e, r, d0))
        return result0 + result1 + result2

    @staticmethod
    def f(time: float, p: np.ndarray, t: float, e: float, r: float, d0: Distribution, vectorized_integral: callable) -> np.ndarray:
        res = vectorized_integral(x=d0.bin_centers, p=p, t=t, e=e, r=r, d0=d0)
        return res

    @staticmethod
    def low_total_density_event(time: float, p: np.ndarray, bin_size: float, threshold: float) -> float:
        total_density = np.sum(p*bin_size)
        return total_density - threshold

    @staticmethod
    def low_max_density_event(time: float, p: np.ndarray, threshold: float) -> float:
        max_density = np.max(p)
        return max_density - threshold


