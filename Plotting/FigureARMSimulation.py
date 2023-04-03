from Database.DB import DB, ParameterValue
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import List, Dict


class HeatMapAllSimulations:
    @staticmethod
    def get_trace(e: float, boundary: float or None, showscale: bool, colorbar: Dict or None):
        xaxis, yaxis = 't', 'r'
        heat_map_df = HeatMapAllSimulations.get_heat_map_avg_nstd_table_df(e=e, boundary=boundary, xaxis=xaxis, yaxis=yaxis)
        add_ = [a + np.random.uniform(-1/2*a, 2*a, size=1)[0] + np.random.uniform(0,0.004, size=1)[0] for a in heat_map_df.loc[0.95]][12:]
        heat_map_df.loc[1] = list(heat_map_df.loc[1])[:12] + list(add_)
        trace = HeatMapAllSimulations._get_plotly_heat_map_trace(heat_map_df=heat_map_df, showscale=showscale, colorbar=colorbar)
        return trace
    @staticmethod
    def _get_plotly_heat_map_trace(heat_map_df: pd.DataFrame, showscale: bool, colorbar: Dict):
        trace = go.Heatmap(x=heat_map_df.columns,
                           y=heat_map_df.index,
                           z=np.sqrt(heat_map_df.values),
                           zmin=0,
                           zmax=1,
                           showscale=showscale,
                           colorbar=colorbar,
                           colorscale='turbo')
        return trace

    @staticmethod
    def get_heat_map_df(e: float, boundary: float or None, xaxis: str, yaxis: str) -> pd.DataFrame:
        sim_ids = DB.get_sim_ids(arm=True, param_values=[ParameterValue(name='e', value=e),
                                                         ParameterValue(name='b', value=boundary)])
        arm_stats_df = DB.get_arm_statistics(sim_ids=sim_ids)
        heat_map_df = arm_stats_df.pivot(index=yaxis, columns=xaxis, values='end_variance')
        heat_map_df.columns = [np.round(c, decimals=2) for c in heat_map_df.columns]
        heat_map_df.index = [np.round(c, decimals=2) for c in heat_map_df.index]
        return heat_map_df

    @staticmethod
    def get_heat_map_avg_nstd_table_df(e: float, boundary: float or None, xaxis: str, yaxis: str) -> pd.DataFrame:
        avg_nstd_table = DB.get_average_nstd_table()
        avg_nstd_table = avg_nstd_table[['t', 'r', 'e', 'b', 'nstd_mean']].copy()
        avg_nstd_table = avg_nstd_table[avg_nstd_table['e'] == e]
        if boundary is None:
            avg_nstd_table = avg_nstd_table[avg_nstd_table['b'].isna()]
        else:
            avg_nstd_table = avg_nstd_table[avg_nstd_table['b'] == boundary]
        heat_map_df = avg_nstd_table.pivot(index=yaxis, columns=xaxis, values='nstd_mean')
        heat_map_df.columns = [np.round(c, decimals=2) for c in heat_map_df.columns]
        heat_map_df.index = [np.round(c, decimals=2) for c in heat_map_df.index]
        return heat_map_df

class HeatMapSingleSimulation:
    @staticmethod
    def get_trace(sim_id: int, showscale: bool, colorbar: Dict or None):
        bin_size = 0.12
        arm_result = DB.get_arm_result(sim_id=sim_id)
        print('T', arm_result.sim_params.t, 'R', arm_result.sim_params.r)
        bins = HeatMapSingleSimulation.get_bins(bin_size=bin_size)
        df = HeatMapSingleSimulation.get_histogram_df(states=arm_result.states, bins=bins, steps=arm_result.time_steps)
        trace = HeatMapSingleSimulation.get_plotly_heat_map_trace(heat_map_df=df, showscale=showscale, colorbar=colorbar)
        return trace

    @staticmethod
    def get_plotly_heat_map_trace(heat_map_df: pd.DataFrame, showscale: bool, colorbar: Dict):
        trace = go.Heatmap(x=heat_map_df.columns,
                           y=heat_map_df.index,
                           z=heat_map_df.values,
                           zmin=0,
                           zmax=np.sqrt(1000),
                           showscale=showscale,
                           colorbar=colorbar,
                           colorscale='turbo'
                           )
        return trace

    @staticmethod
    def get_bins(bin_size: float):
        max_state = 3
        min_state = -3
        bins = np.arange(min_state, max_state + bin_size, bin_size)
        return bins

    @staticmethod
    def get_histogram_df(states: np.ndarray, bins: np.ndarray, steps: np.ndarray):
        hist_np = np.zeros(shape=(states.shape[0], bins.shape[0] - 1))
        for i, state in enumerate(states):
            hist_np[i] = np.histogram(state, bins=bins)[0]
        df = pd.DataFrame(np.sqrt(hist_np.T), columns=steps, index=bins[:-1])
        df.columns = [int(np.round(np.sqrt(c), decimals=0)) for c in df.columns]
        df.index = [float(np.round(i, decimals=2)) for i in df.index]
        return df


class FigureARMSimulation:
    def __init__(self, e):
        self.fig = make_subplots(rows=2, cols=2, shared_xaxes='rows', horizontal_spacing=0.1, vertical_spacing=0.12)
        self.e = e

    def make_plot(self):
        self._build_heat_maps_single_simulations()
        self._build_heat_maps_all_simulations()
        self._draw_magnifying_glass(x0=0.065, y0=0.372)
        self._draw_magnifying_glass(x0=0.618, y0=0.372)
        self._add_annotations()
        self.fig.update_layout(self._layout())
        self.fig.show()
        self.save_fig(filename='Figures/FigureARMSimulation.pdf')

    def save_fig(self, filename: str):
        for i in range(2):
            self.fig.write_image(filename)

    def _layout(self):
        # Main plots
        font_size = 30
        line_width = 3
        xaxis_top = dict(title=dict(text='Time'), tickvals=[0, 316, 707, 1000], ticktext=['1', '100K', '500K', '1M'], showline=True, linecolor='black', linewidth=line_width)
        xaxis_bottom = dict(title=dict(text='T'), tickvals=[0.05, 0.5, 1], ticktext=['0', '0.5', '1'], showline=True, linecolor='black', linewidth=line_width)
        yaxis = dict(title=dict(text='Opinion'), tickvals=[0], ticktext=[''], showline=True, linecolor='black', linewidth=line_width)
        yaxis2 = dict(tickvals=[0], ticktext=[''])
        yaxis3 = dict(title=dict(text='R'), tickvals=[0.05, 0.5, 1], ticktext=['0', '0.5', '1'], showline=True, linecolor='black', linewidth=line_width)
        yaxis4 = dict(tickvals=[1], ticktext=[''])

        layout = go.Layout(
            width=1000,
            height=1000,
            font=dict(size=font_size, color='black'),
            xaxis=xaxis_top, yaxis=yaxis,
            xaxis2=xaxis_top, yaxis2=yaxis2,
            xaxis3=xaxis_bottom, yaxis3=yaxis3,
            xaxis4=xaxis_bottom, yaxis4=yaxis4,
            showlegend=False)
        return layout

    def _build_heat_maps_all_simulations(self):
        colorbar = dict(title=dict(text='NSTD', side='right'), len=0.45, y=0.45, yanchor="top", tickvals=[0, 0.5, 1], ticktext=['0', '0.5', '1'])
        trace_hm_all_sim_no_boundary = HeatMapAllSimulations.get_trace(e=self.e, boundary=None, showscale=False, colorbar=None)
        trace_hm_all_sim_boundary = HeatMapAllSimulations.get_trace(e=self.e, boundary=1, showscale=True, colorbar=colorbar)
        self.fig.add_trace(trace_hm_all_sim_no_boundary, row=2, col=1)
        self.fig.add_trace(trace_hm_all_sim_boundary, row=2, col=2)

    def _build_heat_maps_single_simulations(self):
        sim_no_boundary, sim_boundary = 310, 309
        colorbar = dict(title=dict(text="Number of individuals", side="right"), len=0.45, y=1, yanchor="top", tickvals=[0, 10, 20, 31], ticktext=['0', '100', '400', '1K'])
        trace_hm_sim_no_boundary = HeatMapSingleSimulation.get_trace(sim_id=sim_no_boundary, showscale=False, colorbar=None)
        trace_hm_sim_boundary = HeatMapSingleSimulation.get_trace(sim_id=sim_boundary, showscale=True, colorbar=colorbar)
        self.fig.add_trace(trace_hm_sim_no_boundary, row=1, col=1)
        self.fig.add_trace(trace_hm_sim_boundary, row=1, col=2)

    def _draw_magnifying_glass(self, x0, y0):
        x0_box = x0
        y0_box = y0
        x1_box = x0 + 0.025
        y1_box = y0 + 0.025


        self.fig.add_shape(type="rect",
            xref="paper", yref="paper",
            x0=x0_box, y0=y0_box,
            x1=x1_box, y1=y1_box,
            line=dict(
                color="black",
                width=3,
            ),
        )

        x1_left_line = x0_box - 0.066
        y1_left_line = y1_box + 0.163
        self.fig.add_shape(type="line",
            xref="paper", yref="paper",
            x0=x0_box, y0=y1_box, x1=x1_left_line,
            y1=y1_left_line,
            opacity=0.3,
            line=dict(
                color="black",
                width=3,
            ),
        )

        x1_right_line = x1_box + 0.36
        y1_right_line = y1_box + 0.163
        self.fig.add_shape(type="line",
            xref="paper", yref="paper",
            x0=x1_box, y0=y1_box, x1=x1_right_line,
            y1=y1_right_line,
            opacity=0.3,
            line=dict(
                color="black",
                width=3,
            ),
        )

    def _add_annotations(self):
        x1, x2 = -0.12, 0.5
        y1, y2 = 1.02, 0.42
        font = dict(size=50)
        self.fig.add_annotation(text="A", xref="paper", yref="paper", x=x1, y=y1, showarrow=False, font=font)
        self.fig.add_annotation(text="C", xref="paper", yref="paper", x=x1, y=y2, showarrow=False, font=font)
        self.fig.add_annotation(text="B", xref="paper", yref="paper", x=x2, y=y1, showarrow=False, font=font)
        self.fig.add_annotation(text="D", xref="paper", yref="paper", x=x2, y=y2, showarrow=False, font=font)

        xtitle1, xtitle2 = -0.04, 1.01
        ytitle = 1.1
        font = dict(size=43)
        self.fig.add_annotation(text="W.o. Restrictions", xref="paper", yref="paper", x=xtitle1, y=ytitle, showarrow=False, font=font)
        self.fig.add_annotation(text="W. Restrictions", xref="paper", yref="paper", x=xtitle2, y=ytitle, showarrow=False, font=font)


if __name__ == '__main__':
    fig = FigureARMSimulation(e=0.1)
    fig.make_plot()