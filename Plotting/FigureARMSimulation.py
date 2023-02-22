from Database.DB import DB, ParameterValue
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import List, Dict


class FigureARMSimulation:
    def __init__(self, e):
        self.fig = make_subplots(rows=2, cols=2)
        self.e = e

    def make_plot(self):
        colorbar = dict(title=dict(text='Variance', side='right'))
        self._build_heat_map(boundary=None, showscale=False, colorbar=colorbar, row=1, col=1)
        self._build_heat_map(boundary=1, showscale=True, colorbar=None, row=1, col=2)
        self.fig.update_layout(self._layout())
        self.fig.show()

    def _layout(self):
        # Main plots
        font_size = 30
        line_width = 3

        layout = go.Layout(
            width=1000,
            height=1000,
            font=dict(size=font_size, color='black'),
            xaxis=dict(title=dict(text='T'), showgrid=False, showline=True, linecolor='black', linewidth=line_width),
            yaxis=dict(title=dict(text='E'), showgrid=True, showline=True, linecolor='black', linewidth=line_width),
            xaxis2=dict(title=dict(text='T'), showgrid=False, showline=True, linecolor='black', linewidth=line_width),
            yaxis2=dict(title=dict(text='E'), showgrid=True, showline=True, linecolor='black', linewidth=line_width),
            showlegend=False)
        return layout

    def _build_heat_map(self, boundary: float or None, showscale: bool, colorbar: Dict or None, row: int, col: int):
        xaxis, yaxis = 't', 'r'
        sim_ids = DB.get_sim_ids(arm=True, param_values=[ParameterValue(name='e', value=self.e), ParameterValue(name='b', value=boundary)])
        arm_stats_df = DB.get_arm_statistics(sim_ids=sim_ids)
        arm_stats_df_e = arm_stats_df[arm_stats_df['e'] == self.e]
        heat_map_df = arm_stats_df_e.pivot(index=yaxis, columns=xaxis, values='end_variance')
        trace = self._get_plotly_heat_map_trace(heat_map_df=heat_map_df, showscale=showscale, colorbar=colorbar)
        self.fig.add_trace(trace, row=row, col=col)

    @staticmethod
    def _get_plotly_heat_map_trace(heat_map_df: pd.DataFrame, showscale: bool, colorbar: Dict):
        trace = go.Heatmap(x=[str(np.round(c, decimals=2)) for c in heat_map_df.columns],
                           y=[str(np.round(i, decimals=2)) for i in heat_map_df.index],
                           z=heat_map_df.values,
                           zmin=0,
                           zmax=1,
                           showscale=showscale,
                           colorbar=colorbar)
        return trace

    @staticmethod
    def get_heat_map_df(sim_ids: List[int], x_axis: str, y_axis: str):
        dicts = []
        for sim_id in sim_ids:
            result = DB.get_arm_result(sim_id=sim_id)
            normalized_variance = result.get_normalized_variance_last_step()
            d = {x_axis: getattr(result.sim_params, x_axis), y_axis: getattr(result.sim_params, y_axis), 'var': normalized_variance}
            dicts.append(d)

        df = pd.DataFrame(dicts)
        df = df.pivot(index=y_axis, columns=x_axis, values='var')
        return df


if __name__ == '__main__':
    fig = FigureARMSimulation(e=0.3)
    fig.make_plot()