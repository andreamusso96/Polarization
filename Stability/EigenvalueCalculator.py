import numpy as np


class EigenvalueCalculator:
    def __init__(self, t: float, r: float, e: float):
        self.t = t
        self.r = r
        self.e = e

    def get_eigenvalue(self, k: int, diam: float):
        c = np.log(2) / (self.r * self.e)
        eps = self.r * self.t
        def gamma(f): return EigenvalueCalculator.cos_integral(k=k, f=f, c=c, l=0, m=eps)
        def beta(f): return EigenvalueCalculator.cos_integral(k=k, f=f, c=c, l=eps, m=diam)
        p1 = gamma(f=1) + gamma(f=1 - 1/self.r) - gamma(f=0) - gamma(f=1/self.r)
        p2 = beta(f=1) + beta(f=1 + 1/self.r) - beta(f=0) - beta(f=-1/self.r)
        eig = 1/diam*(p1 + p2)
        return np.round(eig, decimals=15)

    def get_eigenvalue_simple(self, k: int, diam: float):
        c = np.log(2) / self.e
        eps = self.t
        def beta(f): return EigenvalueCalculator.cos_integral(k=k, f=f, c=c, l=eps, m=diam)
        eig = 1/diam* (beta(f=2) - beta(f=0))
        return np.round(eig, decimals=15)

    def get_eigenvalue2(self, k: int, diam: float):
        c = np.log(2) / (self.r * self.e)
        eps = self.r * self.t
        def h1(beta): return EigenvalueCalculator.h(eps=0, phi=eps, beta=beta, c=c, omega=2*np.pi*k/diam)
        def h2(beta): return EigenvalueCalculator.h(eps=eps, phi=diam/2, beta=beta, c=c, omega=2 * np.pi * k / diam)

        p1 = h1(beta=1) + h1(beta=1 - 1/self.r) - h1(beta=0) - h1(beta=1/self.r)
        p2 = h2(beta=1) + h2(beta=1 + 1/self.r) - h2(beta=0) - h2(beta=-1/self.r)
        eig = 1/diam * (p1 + p2)
        return eig
        pass

    @staticmethod
    def h(eps: float, phi: float, beta: float, c: float, omega: float) -> float:
        c2 = c**2
        bo = beta*omega
        bo2 = bo**2
        def f1(x): return np.cos(bo*x) * np.exp(-c*x)
        return 2 * c/(bo2 + c2) * (f1(eps) - f1(phi))

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


