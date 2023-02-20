from Database.DB import DB
from Stability.StabilityAnalysis import StabilityAnalysis, StabilityResult
import numpy as np
from typing import Tuple, List


class StabilityAnalysisRunner:
    @staticmethod
    def get_parameters_stability_analysis() -> Tuple[np.ndarray, np.ndarray, np.ndarray, int, float]:
        num = 100
        diam = 10
        ts = np.linspace(0.01, 1, num=num)
        rs = np.array([1])
        es = np.linspace(0.01, 1, num=num)
        max_frequency = 1000
        return ts, rs, es, max_frequency, diam

    @staticmethod
    def run_stability_analysis() -> List[StabilityResult]:
        ts, rs, es, max_frequency, diam = StabilityAnalysisRunner.get_parameters_stability_analysis()

        results = []
        for t in ts:
            for r in rs:
                for e in es:
                    analysis = StabilityAnalysis(t=t, r=r, e=e)
                    result = analysis.get_stability_analysis(max_frequency=max_frequency, diam=diam)
                    results.append(result)

        return results

    @staticmethod
    def save_stability_analysis(results: List[StabilityResult]):
        for result in results:
            DB.insert_stability_result(stability_result=result)


if __name__ == '__main__':
    from Database.Tables import CreateTable
    CreateTable.create_stability_table()
    results = StabilityAnalysisRunner.run_stability_analysis()
    StabilityAnalysisRunner.save_stability_analysis(results=results)
