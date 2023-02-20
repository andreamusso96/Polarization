from ARMSimulation.ARMParameters import ARMSimulationParameters
from Database.DB import DB
from typing import List
import numpy as np


class ARMInitializer:
    @staticmethod
    def get_sim_ids(n_sims: int) -> List[int]:
        sim_ids = DB.get_arm_sim_ids()
        next_id = sorted(sim_ids)[-1] + 1
        return list(range(next_id, next_id + n_sims))

    @staticmethod
    def get_parameters() -> List[ARMSimulationParameters]:
        n = 1000
        ts = np.linspace(0.05, 1, 20)
        rs = np.linspace(0.05, 1, 20)
        es = np.linspace(0.01, 1, 10)
        mean = 0
        std = 0.2
        n_steps = 1000000
        bs = np.array([1, None])
        frequency_save = 100
        parameter_list = ARMInitializer.make_parameter_list(n=n, ts=ts, rs=rs, es=es, mean=mean, std=std, n_steps=n_steps, bs=bs, frequency_save=frequency_save)
        return parameter_list

    @staticmethod
    def make_parameter_list(n: int, ts: np.ndarray, rs: np.ndarray, es: np.ndarray, mean: float, std: float, n_steps: int, bs: np.ndarray, frequency_save: int) -> List[ARMSimulationParameters]:
        n_sims = len(ts) * len(rs) * len(es) * len(bs)
        sim_ids = ARMInitializer.get_sim_ids(n_sims=n_sims)

        c = 0
        parameter_list = []
        for t in ts:
            for r in rs:
                for e in es:
                    for b in bs:
                        p = ARMSimulationParameters(sim_id=sim_ids[c], n=n, t=t, r=r, e=e, mean=mean, std=std,
                                                    n_steps=n_steps, b=b, frequency_save=frequency_save)
                        parameter_list.append(p)

        return parameter_list

    @staticmethod
    def get_test_parameters() -> List[ARMSimulationParameters]:
        n = 100
        t = 0.1
        r = 0.25
        e = 0.1
        mean = 0
        std = 0.2
        n_steps = 1000000
        b = 1
        frequency_save = 1000
        arm_params = ARMSimulationParameters(sim_id=1, n=n, t=t, r=r, e=e, mean=mean, std=std, n_steps=n_steps, b=b, frequency_save=frequency_save)
        return [arm_params]

    @staticmethod
    def initialize_simulations(test: bool):
        if test:
            parameter_sims = ARMInitializer.get_test_parameters()
        else:
            parameter_sims = ARMInitializer.get_parameters()

        for p in parameter_sims:
            DB.insert_arm_parameters(params=p)


if __name__ == '__main__':
    from Database.Tables import CreateTable
    CreateTable.create_arm_simulation_table()
    ARMInitializer.initialize_simulations(test=True)
