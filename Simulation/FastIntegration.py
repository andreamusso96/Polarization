import numpy as np
from numba import jit


@jit(nopython=True)
def pdf(bin_probs: np.ndarray, bin_edges: np.ndarray, xs: np.ndarray) -> np.ndarray:
    bin_indices = np.searchsorted(bin_edges, xs, side='left')
    lb = np.searchsorted(bin_indices, 1, 'left')
    ub = np.searchsorted(bin_indices, bin_probs.shape[0], 'left')
    return np.hstack((np.zeros(lb), bin_probs[bin_indices[lb:ub]], np.zeros(bin_indices.shape[0] - ub)))


@jit(nopython=True)
def integrand_attraction(a: np.ndarray, bin_probs: np.ndarray, bin_edges: np.ndarray, x: np.ndarray, e: float, r: float) -> np.ndarray:
    t1 = pdf(bin_probs=bin_probs, bin_edges=bin_edges, xs=x + a) * pdf(bin_probs=bin_probs, bin_edges=bin_edges, xs=x + a - a / r)
    t2 = pdf(bin_probs=bin_probs, bin_edges=bin_edges, xs=x) * pdf(bin_probs=bin_probs, bin_edges=bin_edges, xs=x + a / r)
    return np.power(2, -1 * np.abs(a) / r * e) * (t1 - t2)


@jit(nopython=True)
def integrand_repulsion(a: np.ndarray, bin_probs: np.ndarray, bin_edges: np.ndarray, x: np.ndarray, e: float, r: float) -> np.ndarray:
    t1 = pdf(bin_probs=bin_probs, bin_edges=bin_edges, xs=x + a) * pdf(bin_probs=bin_probs, bin_edges=bin_edges, xs=x + a + a / r)
    t2 = pdf(bin_probs=bin_probs, bin_edges=bin_edges, xs=x) * pdf(bin_probs=bin_probs, bin_edges=bin_edges, xs=x - a / r)
    return np.power(2, -1 * np.abs(a) / r * e) * (t1 - t2)


@jit(nopython=True)
def evaluate_integral(x: np.ndarray, bin_probs: np.ndarray, bin_edges: np.ndarray, bin_size: float, support_a: np.ndarray, support_r: np.ndarray, e: float, r: float) -> float:
    result0 = np.sum(integrand_attraction(a=support_a, bin_probs=bin_probs, bin_edges=bin_edges, x=x, e=e, r=r) * bin_size)
    result1 = np.sum(integrand_repulsion(a=support_r, bin_probs=bin_probs, bin_edges=bin_edges, x=x, e=e, r=r) * bin_size)
    return result0 + result1


@jit(nopython=True)
def vectorized_integral(x: np.ndarray, bin_probs: np.ndarray, bin_edges: np.ndarray, bin_size: float, support_a: np.ndarray, support_r: np.ndarray, e: float, r: float) -> np.ndarray:
    res = np.array([evaluate_integral(x=np.array([x_i]), bin_probs=bin_probs, bin_edges=bin_edges, bin_size=bin_size, support_a=support_a, support_r=support_r, e=e, r=r) for x_i in x])
    return res