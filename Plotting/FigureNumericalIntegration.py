from Simulation.SimulationResult import SimulationResult
from Database.DB import DB
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.express.colors import sample_colorscale


class FigureNumericalIntegration:
    def __init__(self):
        self.fig = make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.03)
        self.colorscale = 'Plasma'

    def make_plot(self, sim_id1: int, sim_id2: int):
        self._build_plot(sim_id=sim_id1, row=1, col=1, inset_axis_number=3)
        self._build_plot(sim_id=sim_id2, row=1, col=2, inset_axis_number=4)
        self._add_colorbar()
        self.fig.update_layout(self._layout())
        self.fig.show()

    def _layout(self):
        # Main plots
        font_size = 30
        line_width = 3

        # Inset
        inset_font_size = 23
        inset_line_width = 2

        layout = go.Layout(
            width=2000,
            height=1000,
            font=dict(size=font_size, color='black'),
            xaxis=dict(title=dict(text='Opinion'), showgrid=False, showline=True, linecolor='black', linewidth=line_width),
            xaxis2=dict(title=dict(text='Opinion'), showgrid=False, showline=True, linecolor='black', linewidth=line_width),
            yaxis=dict(title=dict(text='Density'), showgrid=True, showline=True, linecolor='black', linewidth=line_width),
            yaxis2=dict(showgrid=True, showline=False),
            xaxis3=dict(title=dict(text='Time', font=dict(size=inset_font_size)), tickfont=dict(size=inset_font_size), domain=[0.081, 0.178], anchor='y3', showgrid=False, showline=True, linecolor='black', linewidth=inset_line_width),
            yaxis3=dict(title=dict(text='HHI', font=dict(size=inset_font_size)), tickfont=dict(size=inset_font_size), domain=[0.65, 0.9], anchor='x3', showgrid=False, showline=True, linecolor='black', linewidth=inset_line_width),
            xaxis4=dict(title=dict(text='Time', font=dict(size=inset_font_size)), tickfont=dict(size=inset_font_size), domain=[0.597, 0.7], anchor='y4', showgrid=False, showline=True, linecolor='black', linewidth=inset_line_width),
            yaxis4=dict(title=dict(text='HHI', font=dict(size=inset_font_size)), tickfont=dict(size=inset_font_size), domain=[0.65, 0.9], anchor='x4', showgrid=False, showline=True, linecolor='black', linewidth=inset_line_width),
            showlegend=False)
        return layout

    def _add_colorbar(self):
        colorbar_trace = go.Scatter(x=[None], y=[None], mode='markers', marker=dict(colorscale=self.colorscale, showscale=True, cmin=-5, cmax=5, colorbar=dict(thickness=10, tickvals=[-5, 5], ticktext=['0', '20'], outlinewidth=0, title=dict(text="Time", side="right"))))
        self.fig.add_trace(colorbar_trace, row=1, col=2)

    def _build_plot(self, sim_id: int, row: int, col: int, inset_axis_number: int):
        result = DB.get_simulation_result(sim_id=sim_id)
        print('PARAMS', 'E', result.params.e, 'T', result.params.t)
        self._plot_distribution_evolution(result=result,  row=row, col=col)
        self._plot_l2_norm_in_inset(result=result, xaxis=f'x{inset_axis_number}', yaxis=f'y{inset_axis_number}')

    def _plot_distribution_evolution(self, result: SimulationResult, row: int, col: int):
        times = np.unique(result.distributions_df.time.values)
        x = np.linspace(0, 1, len(times))
        colors = sample_colorscale(self.colorscale, list(x))
        for i, t in enumerate(times):
            df_plot = result.distributions_df[result.distributions_df.time == t]
            trace = go.Scatter(x=df_plot.left_bin, y=df_plot.dist_value, mode='lines', line=dict(color=colors[i]),
                               name=str(t))
            self.fig.add_trace(trace, row=row, col=col)

    def _plot_l2_norm_in_inset(self, result: SimulationResult, xaxis: str, yaxis: str):
        l2_norm_df = result.get_l2_norm_df()
        trace = go.Scatter(x=l2_norm_df.time, y=l2_norm_df.l2_norm, mode='lines', xaxis=xaxis, yaxis=yaxis, line=dict(color='red'))
        self.fig.add_trace(trace)


if __name__ == '__main__':
    f = FigureNumericalIntegration()
    f.make_plot(sim_id1=2, sim_id2=3)


