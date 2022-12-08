import numpy as np


class Distribution:
    def __init__(self, d0: np.ndarray, bin_size: float):
        self.d = d0
        self.bin_size = bin_size

        self.d_new_half = None
        self.d_ext_half = None

    def update(self, d_new: np.ndarray):
        self.d = self.cut_out_zeros(a=d_new)

    def init_d_new(self):
        d_new_half = 3 * int(np.round(self.d.shape[0] / 2, decimals=0))
        d_new = np.zeros(2 * d_new_half)
        self.d_new_half = d_new_half
        return d_new

    def init_d_ext(self, r: float):
        d_half = int(np.round(self.d.shape[0] / 2, decimals=0))
        d_ext_half = 3 * self.d.shape[0] + int(np.round(1 + 1 / r, decimals=0)) * self.d.shape[0]
        d_ext = np.zeros(2 * d_ext_half)
        d_indices = d_ext_half - d_half + np.arange(0, self.d.shape[0])
        d_ext[d_indices] = self.d
        self.d_ext_half = d_ext_half
        return d_ext

    def cut_out_zeros(self, a: np.ndarray):
        min_non_zero_index = (a != 0).argmax()
        max_non_zero_index = (a[::-1] != 0).argmax()
        cut_out_size = min(min_non_zero_index, max_non_zero_index)
        up_cut_out_index = a.shape[0] - cut_out_size + 1
        down_cut_out_index = cut_out_size - 1
        a_cut_out = a[down_cut_out_index:up_cut_out_index]
        return a_cut_out

    def get_left_bins(self):
        d_half = int(np.round(self.d.shape[0] / 2, decimals=0))
        left_bins = np.arange(-d_half, d_half) * self.bin_size
        return left_bins


class MasterEquation:
    def __init__(self, t: float, r: float, e: float, d: Distribution):
        self.t = t
        self.r = r
        self.e = e
        self.d = d

        # indices
        self._rt = int(np.round((self.r * self.t) / self.d.bin_size, decimals=0))
        self._1_over_re = int(np.round(1 / (self.r * self.e), decimals=0))
        self._1_minus_1_over_r = int(np.round(1 - 1 / self.r, decimals=0))
        self._1_over_r = int(np.round(1 / self.r, decimals=0))
        self._1_plus_1_over_r = int(np.round(1 + 1 / self.r, decimals=0))

    def step(self):
        d_new = self.d.init_d_new()
        d_ext = self.d.init_d_ext(r=self.r)
        a1, a1_times_1_over_r, a1_times_1_minus_1_over_r, e_ca1 = self.get_a1_indices()
        a2, a2_times_1_over_r, a2_times_1_plus_1_over_r, e_ca2 = self.get_a2_indices()

        for x in range(d_new.shape[0]):
            x_ext = self.d.d_ext_half - self.d.d_new_half + x
            val_f1 = self.f1(d_ext=d_ext, x=x_ext, a1=a1, a1_times_1_over_r=a1_times_1_over_r,
                             a1_times_1_minus_1_over_r=a1_times_1_minus_1_over_r, e_ca1=e_ca1)
            val_f2 = self.f2(d_ext=d_ext, x=x_ext, a2=a2, a2_times_1_over_r=a2_times_1_over_r,
                             a2_times_1_plus_1_over_r=a2_times_1_plus_1_over_r, e_ca2=e_ca2)
            d_new[x] = d_ext[x_ext] + (val_f1 + val_f2)

        self.d.update(d_new=d_new)
        return self.d

    def get_a1_indices(self):
        a1 = np.arange(-1 * self._rt, self._rt + 1)
        a1_times_1_minus_1_over_r = self._1_minus_1_over_r * a1
        a1_times_1_over_r = self._1_over_r * a1
        a1_times_1_over_re = self._1_over_re * a1
        e_ca1 = np.exp(-1 * np.abs(a1_times_1_over_re * self.d.bin_size))
        return a1, a1_times_1_over_r, a1_times_1_minus_1_over_r, e_ca1

    def get_a2_indices(self):
        d_length = int(np.round(self.d.d.shape[0], decimals=0))
        a2_up = np.arange(self._rt + 1, d_length)
        a2 = np.append(-1 * a2_up[::-1], a2_up)
        a2_times_1_plus_1_over_r = self._1_plus_1_over_r * a2
        a2_times_1_over_r = self._1_over_r * a2
        a2_times_1_over_re = self._1_over_re * a2
        e_ca2 = np.exp(-1 * np.abs(a2_times_1_over_re * self.d.bin_size))
        return a2, a2_times_1_over_r, a2_times_1_plus_1_over_r, e_ca2

    @staticmethod
    def f1(d_ext: np.ndarray, x: int, a1: np.ndarray, a1_times_1_over_r: np.ndarray,
           a1_times_1_minus_1_over_r: np.ndarray, e_ca1: np.ndarray) -> float:
        d_new_x = np.sum(
            e_ca1 * (d_ext[x + a1] * d_ext[x + a1_times_1_minus_1_over_r] - d_ext[x] * d_ext[x + a1_times_1_over_r]))
        return np.round(d_new_x, decimals=15)

    @staticmethod
    def f2(d_ext: np.ndarray, x: int, a2: np.ndarray, a2_times_1_over_r: np.ndarray,
           a2_times_1_plus_1_over_r: np.ndarray, e_ca2: np.ndarray):
        d_new_x = np.sum(
            e_ca2 * (d_ext[x + a2] * d_ext[x + a2_times_1_plus_1_over_r] - d_ext[x] * d_ext[x - a2_times_1_over_r]))
        return np.round(d_new_x, decimals=15)