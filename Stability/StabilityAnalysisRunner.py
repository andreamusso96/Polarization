from Database.DB import DB
from Stability.StabilityAnalysis import StabilityAnalysis, StabilityResult
import numpy as np
from typing import Tuple, List


class StabilityAnalysisRunner:
    @staticmethod
    def get_parameters_stability_analysis() -> Tuple[np.ndarray, np.ndarray, np.ndarray, int, float]:
        num = 10
        ts = np.linspace(0.1, 1, num=num)
        rs = np.array([1]) # np.linspace(0.1, 1, num=num)
        es = np.linspace(0.1, 1, num=num)
        max_frequency = 1000
        diam = 10
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


def plot_stability():
    import pandas as pd
    import plotly.graph_objects as go
    results = StabilityAnalysisRunner.run_stability_analysis()
    ds = []
    for result in results:
        d = {'t': result.t, 'e': result.e, 'max_eig': result.max_eig}
        ds.append(d)

    df = pd.DataFrame(ds)
    df = df.pivot(index='t', columns='e', values='max_eig')

    fig = go.Figure()
    trace = go.Heatmap(z=df.values, x=df.columns, y=df.index)
    fig.add_trace(trace)
    fig.update_xaxes(title_text='e')
    fig.update_yaxes(title_text='t')
    fig.show()


if __name__ == '__main__':
    plot_stability()