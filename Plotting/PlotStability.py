from Database.DB import DB
import pandas as pd
import plotly.graph_objects as go
import numpy as np


class StabilityPlotter:
    @staticmethod
    def plot_stability_heatmap():
        heat_map_df = StabilityPlotter.get_stability_result_heat_map_df(z_value='max_eig')
        fig = go.Figure()
        trace = StabilityPlotter.get_plotly_heat_map_trace(heat_map_df=heat_map_df)

        fig.add_trace(trace)
        fig.update_layout(StabilityPlotter.figure_layout())
        fig.show()
        fig.write_image('stability_heatmap.png')

    @staticmethod
    def figure_layout():
        tick_vals = np.round(np.linspace(0.02, 0.98, 6), decimals=2)
        tick_text = [str(i) for i in np.round(np.linspace(0.02, 0.98, 6), decimals=1)]
        layout = go.Layout(
            width=900, height=800,
            font=dict(size=30, color='black'),
            xaxis=dict(title='T', tickvals=tick_vals, ticktext=tick_text),
            yaxis=dict(title='E', tickvals=tick_vals, ticktext=tick_text),
            )
        return layout
    @staticmethod
    def get_plotly_heat_map_trace(heat_map_df: pd.DataFrame):
        trace = go.Heatmap(x=[str(np.round(c, decimals=2)) for c in heat_map_df.columns],
                           y=[str(np.round(i, decimals=2)) for i in heat_map_df.index],
                           z=heat_map_df.values,
                           colorbar=dict(title=dict(text="Maximum Eigenvalue", side="right")))
        return trace

    @staticmethod
    def get_stability_result_heat_map_df(z_value: str):
        results = DB.get_stability_results()
        ds = []
        for result in results:
            d = {'t': result.t, 'e': result.e, z_value: getattr(result, z_value)}
            ds.append(d)

        df = pd.DataFrame(ds)
        df = df.pivot(index='e', columns='t', values=z_value)
        return df

if __name__ == '__main__':
    StabilityPlotter.plot_stability_heatmap()