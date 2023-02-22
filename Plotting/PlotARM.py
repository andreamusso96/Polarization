from Database.DB import DB
import pandas as pd
import numpy as np
import plotly.graph_objects as go


class PlotARM:
    @staticmethod
    def plot_arm_result(sim_id: int):
        arm_result = DB.get_arm_result(sim_id=sim_id)
        bin_size = 0.05
        bins = PlotARM.get_bins(states=arm_result.states, bin_size=bin_size)
        df = PlotARM.get_histogram_df(states=arm_result.states, bins=bins, steps=arm_result.time_steps)
        fig = go.Figure()
        trace = PlotARM.get_plotly_heat_map_trace(heat_map_df=df)

        fig.add_trace(trace)
        fig.update_layout(PlotARM.figure_layout())
        fig.show()

    @staticmethod
    def figure_layout():
        layout = go.Layout(
            width=2000, height=1200,
            font=dict(size=30, color='black'),
            xaxis=dict(title='Time'),
            yaxis=dict(title='Opinion'),
        )
        return layout

    @staticmethod
    def get_plotly_heat_map_trace(heat_map_df: pd.DataFrame):
        trace = go.Heatmap(x=[str(int(np.round(c/1000, decimals=0))) for c in heat_map_df.columns],
                           y=[str(np.round(i, decimals=2)) for i in heat_map_df.index],
                           z=heat_map_df.values,
                           colorbar=dict(title=dict(text="Number of individuals", side="right")))
        return trace

    @staticmethod
    def get_bins(states: np.ndarray, bin_size: float):
        max_state = np.ceil(np.max(states))
        min_state = np.floor(np.min(states))
        bins = np.arange(min_state, max_state + bin_size, bin_size)
        return bins

    @staticmethod
    def get_histogram_df(states: np.ndarray, bins: np.ndarray, steps: np.ndarray):
        hist_np = np.zeros(shape=(states.shape[0], bins.shape[0]-1))
        for i, state in enumerate(states):
            hist_np[i] = np.histogram(state, bins=bins)[0]

        df = pd.DataFrame(hist_np.T, columns=steps, index=bins[:-1])
        return df

    @staticmethod
    def plot_arm_heat_map():
        pass


if __name__ == '__main__':
    PlotARM.plot_arm_result(sim_id=965)