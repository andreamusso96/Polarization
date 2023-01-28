from Simulation.SimulationResult import SimulationResult
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.express.colors import sample_colorscale


class SingleSimulationPlot:
    def __init__(self, result: SimulationResult):
        self.result = result
        self.n_cols = 3
        self.n_rows = 1
        self.fig = make_subplots(rows=self.n_rows, cols=self.n_cols)
        self.sums = self.get_sums()

    def plot_simulation(self):
        #self.plot_l2_norm_evolution()
        self.plot_sum_evolution()
        self.plot_distribution_evolution()
        self.plot_parameters()
        self.fig.update_layout(dict(title=f'{self.result.params.sim_id}_{self.result.params.method}',
            updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=list([
                    dict(
                        args=["visible", "legendonly"],
                        label="Deselect All",
                        method="restyle"
                    ),
                    dict(
                        args=["visible", True],
                        label="Select All",
                        method="restyle"
                    )
                ]),
                pad={"r": 10, "t": 10},
                showactive=False,
                x=1,
                xanchor="right",
                y=1.1,
                yanchor="top"
            ),
        ]
        ))
        self.fig.show(renderer='browser')

    def plot_l2_norm_evolution(self):
        row, col = 1, 1
        l2_norm_df = self.result.get_l2_norm_df()
        trace = go.Scatter(x=l2_norm_df.time, y=l2_norm_df.l2_norm, mode='lines')
        self.fig.add_trace(trace, row=row, col=col)
        self.fig.update_xaxes(title_text='time', row=row, col=col)
        self.fig.update_yaxes(title_text='value', row=row, col=col)

    def plot_sum_evolution(self):
        row, col = 1, 1
        sums = self.get_sums()
        trace = go.Scatter(x=list(range(len(sums))), y=sums, mode='lines')
        self.fig.add_trace(trace, row=row, col=col)

    def plot_distribution_evolution(self):
        times = range(len(self.sums)) #np.unique(self.result.distributions_df.time.values)
        x = np.linspace(0, 1, len(times))
        colors = sample_colorscale('jet', list(x))
        row, col = 1, 2
        for i, t in enumerate(times):
            df_plot = self.result.distributions_df[self.result.distributions_df.time == t]
            trace = go.Scatter(x=df_plot.left_bin, y=df_plot.dist_value, mode='lines', line=dict(color=colors[i]), name=str(t))
            self.fig.add_trace(trace, row=row, col=col)

        self.fig.update_xaxes(title_text='opinions', row=row, col=col)
        self.fig.update_yaxes(title_text='density', row=row, col=col)

    def plot_parameters(self):
        row, col = 1, 3
        trace = go.Bar(x=['t', 'r', 'e'], y=[self.result.params.t, self.result.params.r, self.result.params.e])
        self.fig.add_trace(trace, row=row, col=col)
        self.fig.update_yaxes(title_text=f'{self.result.params.d0_parameters.to_string()}', row=row, col=col, range=[0,1])

    def get_sums(self):
        times = np.unique(self.result.distributions_df.time.values)
        sums = []
        for i, t in enumerate(times):
            df_plot = self.result.distributions_df[self.result.distributions_df.time == t]
            sum_t = np.sum(df_plot.dist_value*self.result.params.bin_size)
            if np.abs(sum_t) < 2 and np.abs(sum_t) > 0.7:
                sums.append(sum_t)

        return np.array(sums)
