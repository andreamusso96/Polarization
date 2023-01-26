import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from typing import List


class HeatMap:
    def __init__(self, x_axis: str, y_axis: str, z_val: str, f_name: str):
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.z_val = z_val
        self.f_name = f_name


class HeatMapPlotter:
    @staticmethod
    def plot_heat_maps(heat_maps: List[pd.DataFrame]):
        n_plots_per_row = min(6, len(heat_maps))
        rows, cols = HeatMapPlotter._get_rows_and_cols(n_plots=len(heat_maps),
                                                                   n_plots_per_row=n_plots_per_row)
        fig = make_subplots(rows=rows, cols=cols)

        row = 1
        col = 1
        for heat_map_df in heat_maps:
            fig.add_trace(HeatMapPlotter._get_heat_map_trace(heat_map_df=heat_map_df), row=row, col=col)
            fig.update_xaxes(title_text=heat_map_df.columns.name, row=row, col=col)
            fig.update_yaxes(title_text=heat_map_df.index.name, row=row, col=col)

            if col == n_plots_per_row:
                row += 1
                col = 1
            col += 1

        fig.update_traces(showscale=False)
        fig.show(renderer='browser')

    @staticmethod
    def _get_heat_map_trace(heat_map_df):
        trace = go.Heatmap(x=[str(np.round(c, decimals=10)) for c in heat_map_df.columns],
                           y=[str(np.round(i, decimals=10)) for i in heat_map_df.index],
                           z=heat_map_df.values,
                           hovertemplate=heat_map_df.columns.name + ': %{x}<br>' + heat_map_df.index.name + ': %{y}<br>' + heat_map_df.name + ': %{z}<extra></extra>')

        return trace

    @staticmethod
    def _get_rows_and_cols(n_plots, n_plots_per_row):
        rows = int(np.ceil(n_plots / n_plots_per_row))
        cols = n_plots_per_row
        return rows, cols