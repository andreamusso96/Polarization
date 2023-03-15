from Simulation.SimulationResult import SimulationResult
from Database.DB import DB
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.express.colors import sample_colorscale


class FigureNumericalIntegration:
    def __init__(self):
        self.fig = make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.06)
        self.colorscale = 'turbo'

    def make_plot(self, sim_id1: int, sim_id2: int):
        self._build_plot(sim_id=sim_id1, row=1, col=1, inset_axis_number=3)
        self._build_plot(sim_id=sim_id2, row=1, col=2, inset_axis_number=4)
        self._add_colorbar()
        self._add_annotations()
        self.fig.update_layout(self._layout())
        self.fig.show()
        self.save_fig(filename='Figures/FigureNumericalIntegration.pdf')

    def save_fig(self, filename: str):
        for i in range(2):
            self.fig.write_image(filename)

    def _layout(self):
        # Main plots
        font_size = 30
        line_width = 3

        # Inset
        inset_font_size = 20
        inset_line_width = 2

        #Xaxis
        xaxis = dict(title=dict(text='Opinion'), tickvals=[-5, 0, 4.95], ticktext=['-5', '0', '5'],  showgrid=False, showline=True, linecolor='black', linewidth=line_width)
        layout = go.Layout(
            width=1000,
            height=600,
            font=dict(size=font_size, color='black'),
            xaxis=xaxis,
            xaxis2=xaxis,
            yaxis=dict(title=dict(text='Density'), showgrid=True, showline=True, linecolor='black', linewidth=line_width),
            yaxis2=dict(showgrid=True, showline=False),
            xaxis3=dict(title=dict(text='Time', font=dict(size=inset_font_size), standoff=10), tickfont=dict(size=inset_font_size), tickvals=[], domain=[0.1, 0.2], anchor='y3', showgrid=False, showline=True, linecolor='black', linewidth=inset_line_width),
            yaxis3=dict(title=dict(text='Diversity', font=dict(size=inset_font_size), standoff=0), tickfont=dict(size=inset_font_size), range=[0,6], tickvals=[0, 6], domain=[0.73, 0.952], anchor='x3', showgrid=False, showline=True, linecolor='black', linewidth=inset_line_width),
            xaxis4=dict(title=dict(text='Time', font=dict(size=inset_font_size), standoff=10), tickfont=dict(size=inset_font_size), tickvals=[], domain=[0.64, 0.74], anchor='y4', showgrid=False, showline=True, linecolor='black', linewidth=inset_line_width),
            yaxis4=dict(title=dict(text='Diversity', font=dict(size=inset_font_size), standoff=0), tickfont=dict(size=inset_font_size), range=[0,6], tickvals=[0, 6], domain=[0.73, 0.952], anchor='x4', showgrid=False, showline=True, linecolor='black', linewidth=inset_line_width),
            showlegend=False)
        return layout

    def _add_colorbar(self):
        colorbar_trace = go.Scatter(x=[None], y=[None], mode='markers', marker=dict(colorscale=self.colorscale, showscale=True, cmin=-5, cmax=5, colorbar=dict(thickness=10, tickvals=[], ticktext=[], outlinewidth=0, title=dict(text="Time", side="right"))))
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
        print('MAX L2', l2_norm_df.max())
        trace = go.Scatter(x=l2_norm_df.time, y=l2_norm_df.l2_norm, mode='lines', xaxis=xaxis, yaxis=yaxis, line=dict(color='red'))
        self.fig.add_trace(trace)

    def _add_annotations(self):
        x1, x2 = -0.13, 0.499
        y1 = 1.04
        font = dict(size=50)
        self.fig.add_annotation(text="A", xref="paper", yref="paper", x=x1, y=y1, showarrow=False, font=font)
        self.fig.add_annotation(text="B", xref="paper", yref="paper", x=x2, y=y1, showarrow=False, font=font)





if __name__ == '__main__':
    f = FigureNumericalIntegration()
    f.make_plot(sim_id1=29, sim_id2=30)


