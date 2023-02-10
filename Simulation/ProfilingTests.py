from Simulation.FastIntegration import vectorized_integral
from Simulation.MasterEquation import MasterEquation
from Simulation.Distribution import DistributionGenerator, DistributionParameters
from Simulation.Parameters import SimulationParameters
from Simulation.Simulator import Simulator
import numpy as np


class ProfilingTest:
    @staticmethod
    def get_parameters():
        support = 3
        bin_size = 0.005
        t, r, e = 0.2, 0.5, 0.4
        dist_params = DistributionParameters(name='normal', params={'loc': 0, 'scale': 0.2})
        boundary = None
        total_time_span = 1
        n_save_distributions_block = 1
        block_time_span = 1
        method = 'DOP853'
        p = SimulationParameters(sim_id=1, t=t, r=r, e=e, support=support, bin_size=bin_size, boundary=boundary,
                                 d0_parameters=dist_params,
                                 total_time_span=total_time_span, n_save_distributions_block=n_save_distributions_block,
                                 block_time_span=block_time_span, method=method, num_processes=1)
        return p

    @staticmethod
    def get_distribution():
        p = ProfilingTest.get_parameters()
        d0 = DistributionGenerator.get_distribution(support=p.support, bin_size=p.bin_size, dist_params=p.d0_parameters, boundary=p.boundary)
        return d0

    @staticmethod
    def _speed_test():
        pass

    @staticmethod
    def profile():
        from pyinstrument import Profiler
        profiler = Profiler()
        profiler.start()
        ProfilingTest._speed_test()
        profiler.stop()
        profiler.open_in_browser()


class SimulatorTest(ProfilingTest):
    @staticmethod
    def _speed_test():
        p = SimulatorTest.get_parameters()
        sim = Simulator(p)
        sim.run_simulation()


class MasterEquationTest(ProfilingTest):
    @staticmethod
    def get_parameters():
        p = super().get_parameters()
        d0 = super().get_distribution()
        t_span = p.total_time_span
        time_step_save = [0, 1]
        return p, d0, t_span, time_step_save

    @staticmethod
    def _speed_test():
        p, d0, t_span, time_step_save = MasterEquationTest.get_parameters()
        me = MasterEquation(t=p.t, r=p.r, e=p.e, d0=d0)
        res = me.solve(time_span=t_span, time_steps_save=time_step_save, method=p.method)
        return res


class FastIntegrationTest(ProfilingTest):
    @staticmethod
    def get_parameters():
        p = super().get_parameters()
        d0 = super().get_distribution()
        rt = p.r * p.t
        lb, ub = tuple(np.searchsorted(d0.bin_edges, np.array([-rt, rt])))
        support_a = d0.bin_centers[lb:ub]
        support_r_side = d0.bin_centers[ub:]
        support_r = np.concatenate((-support_r_side[::-1], support_r_side))
        return d0, support_a, support_r, p.e, p.r

    @staticmethod
    def _speed_test():
        d0, support_a, support_r, e, r = FastIntegrationTest.get_parameters()
        p = d0.bin_probs
        for i in range(100):
            res1 = vectorized_integral(x=d0.bin_centers, bin_probs=p, bin_edges=d0.bin_edges, bin_size=d0.bin_size,
                                       support_a=support_a, support_r=support_r, e=e, r=r)
            p = res1


if __name__ == '__main__':
    FastIntegrationTest.profile()
    MasterEquationTest.profile()