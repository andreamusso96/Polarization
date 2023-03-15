from Database.DB import DB
import numpy as np
import plotly.graph_objects as go
import pandas as pd


class FigureStability:
    def __init__(self):
        self.fig = go.Figure()

    def make_plot(self):
        heat_map_df = self._get_stability_result_heat_map_df(z_value='max_eig')
        trace = self._get_plotly_heat_map_trace(heat_map_df=heat_map_df)
        self.fig.add_trace(trace)
        self.fig.update_layout(self._layout())
        self.fig.show()
        self.save_fig(filename='Figures/FigureStability.pdf')

    def save_fig(self, filename: str):
        for i in range(4):
            self.fig.write_image(filename)

    @staticmethod
    def _layout():
        tick_vals = np.round(np.linspace(0.02, 0.98, 6), decimals=2)
        tick_text = [str(i) for i in np.round(np.linspace(0.02, 0.98, 6), decimals=1)]
        layout = go.Layout(
            width=1000, height=870,
            font=dict(size=30, color='black'),
            xaxis=dict(title='T', tickvals=tick_vals, ticktext=tick_text),
            yaxis=dict(title='E', tickvals=tick_vals, ticktext=tick_text),
            )
        return layout

    @staticmethod
    def _get_plotly_heat_map_trace(heat_map_df: pd.DataFrame):
        trace = go.Heatmap(x=[str(np.round(c, decimals=2)) for c in heat_map_df.columns],
                           y=[str(np.round(i, decimals=2)) for i in heat_map_df.index],
                           z=heat_map_df.values,
                           colorbar=dict(title=dict(text="Maximum Eigenvalue", side="right")),
                           colorscale='turbo')
        return trace

    @staticmethod
    def _get_stability_result_heat_map_df(z_value: str) -> pd.DataFrame:
        results = DB.get_stability_results()
        ds = []
        for result in results:
            d = {'t': result.t, 'e': result.e, z_value: getattr(result, z_value)}
            ds.append(d)

        df = pd.DataFrame(ds)
        df = df.pivot(index='e', columns='t', values=z_value)
        return df


if __name__ == '__main__':
    fig = FigureStability()
    fig.make_plot()