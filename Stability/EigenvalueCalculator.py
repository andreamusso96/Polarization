import numpy as np


class EigenvalueCalculator:
    def __init__(self, t: float, r: float, e: float):
        self.t = t
        self.r = r
        self.e = e

    def get_eigenvalue(self, k: int):
        # Variable definition
        c = np.log(2)/(self.r*self.e)
        c2 = c**2
        eps = self.r*self.t
        v = (self.r - 1)/self.r
        w = (self.r + 1)/self.r
        kv = k*v
        kv2 = kv**2
        kw = k*w
        kw2 = kw**2

        # Eigenvalue computation
        eig_p1 = 1/(k**2 + c2) + 1/(kv2  + c2) - 1/c2 - 1/((k/self.r)**2 + c2)
        eig_p2 = np.exp(-c*eps)* (1/(kv2 + c2) * kv*np.sin(eps*kv) - np.cos(eps*kv))
        eig_p3 = np.exp(-c*eps)* (-1/(kw2 + c2) * kw*np.sin(eps*kw) - np.cos(eps*kw))
        eig = eig_p1 + eig_p2 + eig_p3
        return eig
