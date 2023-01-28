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
        eig_p2 = np.exp(-c*eps) * (1/(kv2 + c2) * kv*np.sin(eps*kv) - np.cos(eps*kv))
        eig_p3 = np.exp(-c*eps)* (-1/(kw2 + c2) * kw*np.sin(eps*kw) - np.cos(eps*kw))
        eig = eig_p1 + eig_p2 + eig_p3
        return eig

    def get_eigenvalue2(self, k: int, diam: float):
        c = np.log(2) / (self.r * self.e)
        eps = self.r * self.t
        def gamma(f): return EigenvalueCalculator.cos_integral(k=k, f=f, c=c, l=0, m=eps)
        def beta(f): return EigenvalueCalculator.cos_integral(k=k, f=f, c=c, l=eps, m=diam)
        p1 = gamma(f=1) + gamma(f=1 - 1/self.r) - gamma(f=0) - gamma(f=1/self.r)
        p2 = beta(f=1) + beta(f=1 + 1/self.r) - beta(f=0) - beta(f=-1/self.r)
        eig = 1/diam*(p1 + p2)
        return np.round(eig, decimals=15)

    @staticmethod
    def cos_integral(k, f, c, l, m):
        if f != 0 and k != 0:
            c2 = c**2
            kf = k*f
            kf2 = kf**2

            p1 = 1/(1 + c2/kf2)
            p2 = 1/kf * (np.exp(-c*m)*np.sin(kf*m) - np.exp(-c*l)*np.sin(kf*l))
            p3 = c/kf2 * (np.exp(-c*m)*np.cos(kf*m) - np.exp(-c*l)*np.cos(kf*l))
            return 2 * p1 * (p2 - p3)
        else:
            p = -1/c * (np.exp(-c*m) - np.exp(-c*l))
            return p


