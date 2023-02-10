import numpy as np
from scipy.integrate import quad_vec, quadrature
from numba import jit
from multiprocessing import Pool


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


def evaluate_integral(x: np.ndarray, bin_probs: np.ndarray, bin_edges: np.ndarray, t: float, e: float, r: float,
                      support: float) -> float:
    rt = r * t
    def i1(a: np.ndarray): return integrand_attraction(a=np.atleast_1d(a), bin_probs=bin_probs, bin_edges=bin_edges, x=x, e=e, r=r)
    def i2(a: np.ndarray): return integrand_repulsion(a=np.atleast_1d(a), bin_probs=bin_probs, bin_edges=bin_edges, x=x, e=e, r=r)
    result0, abserr0 = quad_vec(i1, a=-rt, b=rt)
    result1, abserr1 = quad_vec(i2, a=rt, b=support)
    result2, abserr2 = quad_vec(i2, a=-support, b=-rt)
    return result0 + result1 + result2


def vectorized_integral(x: np.ndarray, bin_probs: np.ndarray, bin_edges: np.ndarray, t: float, e: float, r: float, support: float) -> np.ndarray:
    res = np.array([evaluate_integral(x=np.array([x_i]), bin_probs=bin_probs, bin_edges=bin_edges, t=t, e=e, r=r, support=support) for x_i in x])
    return res


def parallelized_integral(x: np.ndarray, bin_probs: np.ndarray, bin_edges: np.ndarray, t: float, e: float, r: float, support: float, num_processes: int) -> np.ndarray:
    chunk_size = int(np.ceil(len(x) / num_processes))
    chunks = [x[i:i + chunk_size] for i in range(0, len(x), chunk_size)]
    with Pool(processes=num_processes) as pool:
        res = pool.starmap(vectorized_integral, [(chunk, bin_probs, bin_edges, t, e, r, support) for chunk in chunks])
    return np.concatenate(res)