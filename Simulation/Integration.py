import numpy as np
from scipy.integrate import fixed_quad
from scipy.stats import rv_histogram


def integrand(a: float, q: rv_histogram, x: float, e: float):
    return np.power(2, -1 * np.abs(a) / e) * q.pdf(x + a) * (q.pdf(x + 2 * a) - q.pdf(x))


def evaluate_integral(x: float, q: rv_histogram, support: float, t: float, e: float) -> float:
    result0, abserr = fixed_quad(integrand, a=-support, b=-t, args=(q, x, e), n=20)
    result1, abserr = fixed_quad(integrand, a=t, b=support, args=(q, x, e), n=20)
    return result0 + result1


def vectorized_integral(x: np.ndarray, bin_probs: np.ndarray, bin_edges: np.ndarray, support: float, t: float, e: float) -> np.ndarray:
    q = rv_histogram((bin_probs, bin_edges), density=True)
    res = np.array([evaluate_integral(x=x_i, q=q, t=t, support=support, e=e) for x_i in x])
    return res