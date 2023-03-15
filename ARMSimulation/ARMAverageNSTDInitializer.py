from ARMSimulation.ARMAverageNSTDParams import ARMAverageNSTDParams
from ARMSimulation.ARMParameters import ARMSimulationParameters
from Database.DB import DB
from typing import List
import numpy as np


class ARMAverageNSTDInitializer:
    @staticmethod
    def get_sim_ids(n_sims: int) -> List[int]:
        try:
            last_sim_id = sorted(DB.get_sim_ids(arm=True))[-1]
        except IndexError as e:
            last_sim_id = 0

        return list(range(last_sim_id+1, last_sim_id+1+n_sims))

    @staticmethod
    def get_parameters() -> List[ARMAverageNSTDParams]:
        n = 1000
        ts = np.linspace(0.05, 1, 20)
        rs = np.linspace(0.05, 1, 20)
        es = np.array([0.1])
        mean = 0
        std = 0.2
        n_steps = 1000000
        bs = np.array([1, None])
        frequency_save = 1000
        n_runs = 50
        parameter_list = ARMAverageNSTDInitializer.make_parameter_list(n=n, ts=ts, rs=rs, es=es, mean=mean, std=std, n_steps=n_steps, bs=bs, frequency_save=frequency_save, n_runs=n_runs)
        return parameter_list

    @staticmethod
    def make_parameter_list(n: int, ts: np.ndarray, rs: np.ndarray, es: np.ndarray, mean: float, std: float, n_steps: int, bs: np.ndarray, frequency_save: int, n_runs: int) -> List[ARMAverageNSTDParams]:
        n_sims = len(ts) * len(rs) * len(es) * len(bs)
        sim_ids = ARMAverageNSTDInitializer.get_sim_ids(n_sims=n_sims)

        c = 0
        parameter_list = []
        for t in ts:
            for r in rs:
                for e in es:
                    for b in bs:
                        arm_params = ARMSimulationParameters(sim_id=sim_ids[c], n=n, t=t, r=r, e=e, mean=mean, std=std,
                                                    n_steps=n_steps, b=b, frequency_save=frequency_save)
                        arm_avg_nstd_params = ARMAverageNSTDParams(arm_params=arm_params, n_runs=n_runs)

                        parameter_list.append(arm_avg_nstd_params)
                        c += 1

        return parameter_list

    @staticmethod
    def get_test_parameters() -> List[ARMAverageNSTDParams]:
        n = 100
        t = 0.1
        r = 0.25
        e = 0.1
        mean = 0
        std = 0.2
        n_steps = 1000000
        b = 1
        frequency_save = 1000
        n_runs = 5
        arm_params = ARMSimulationParameters(sim_id=1, n=n, t=t, r=r, e=e, mean=mean, std=std, n_steps=n_steps, b=b, frequency_save=frequency_save)
        arm_avg_nstd_params = ARMAverageNSTDParams(arm_params=arm_params, n_runs=n_runs)
        return [arm_avg_nstd_params]

    @staticmethod
    def initialize_simulations(test: bool):
        if test:
            parameter_sims = ARMAverageNSTDInitializer.get_test_parameters()
        else:
            parameter_sims = ARMAverageNSTDInitializer.get_parameters()

        for p in parameter_sims:
            DB.insert_average_nstd_params(average_nstd_params=p)


if __name__ == '__main__':
    from Database.Tables import CreateTable
    CreateTable.create_average_nstd_table()
    ARMAverageNSTDInitializer.initialize_simulations(test=False)