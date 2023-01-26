from Plotting.HeatMap import HeatMapPlotter, HeatMap
from Plotting.SingleSimulation import SingleSimulationPlot
from Database.DB import DB, ParameterRange
from typing import List


class SimulationStatisticPlotter:
    @staticmethod
    def plot_heat_map_sim_statistic(heat_maps: List[HeatMap]) -> None:
        sim_ids = list(range(1,1000))
        heat_maps_dfs = [DB.get_heat_map_sim_statistics(x_axis=heat_map.x_axis, y_axis=heat_map.y_axis, z_val=heat_map.z_val, f_name=heat_map.f_name, sim_ids=sim_ids) for heat_map in heat_maps]
        HeatMapPlotter.plot_heat_maps(heat_maps=heat_maps_dfs)


class StabilityPlotter:
    @staticmethod
    def plot_heat_map_sim_statistic(heat_maps: List[HeatMap]) -> None:
        heat_maps_dfs = [DB.get_heat_map_stability(x_axis=heat_map.x_axis, y_axis=heat_map.y_axis, z_val=heat_map.z_val,
                                           f_name=heat_map.f_name) for heat_map in heat_maps]
        HeatMapPlotter.plot_heat_maps(heat_maps=heat_maps_dfs)


class SingleSimulationPlotter:
    @staticmethod
    def plot_result(sim_id: int):
        result = DB.get_simulation_result(sim_id=sim_id)
        plot = SingleSimulationPlot(result=result)
        plot.plot_simulation()


def plot_heat_maps_sim_statistics():
    heat_maps = [HeatMap(x_axis='t', y_axis='r', z_val='l2_norm_diff', f_name='avg'),
                 HeatMap(x_axis='t', y_axis='e', z_val='l2_norm_diff', f_name='avg'),
                 HeatMap(x_axis='e', y_axis='r', z_val='l2_norm_diff', f_name='avg'),
                 HeatMap(x_axis='t', y_axis='r', z_val='l2_norm_end', f_name='avg'),
                 HeatMap(x_axis='t', y_axis='r', z_val='l2_norm_end', f_name='max')]
    SimulationStatisticPlotter.plot_heat_map_sim_statistic(heat_maps=heat_maps)


def plot_heat_maps_stability():
    heat_maps = [HeatMap(x_axis='t', y_axis='r', z_val='stable', f_name='avg'),
                 HeatMap(x_axis='t', y_axis='e', z_val='stable', f_name='avg'),
                 HeatMap(x_axis='e', y_axis='r', z_val='stable', f_name='avg')]
    StabilityPlotter.plot_heat_map_sim_statistic(heat_maps=heat_maps)

def get_sids_to_plot():
    ts = [0.1, 0.3, 0.5, 0.8, 1]
    rs = [0.1, 0.3, 0.6, 1]
    es = [0.1, 0.5, 1]
    epsilon = 0.01

    sids_plot = []
    for t in ts:
        param_range_t = ParameterRange(name='t', min_val=t, max_val=t + epsilon)
        for r in rs:
            param_range_r = ParameterRange(name='r', min_val=r, max_val=r + epsilon)
            for e in es:
                param_range_e = ParameterRange(name='e', min_val=e, max_val=e + epsilon)
                sids = DB.get_ids_in_parameter_ranges(param_ranges=[param_range_e, param_range_r, param_range_t], method='intersection')
                sids_plot += list(sids)

    return sids_plot

def plot_results():
    sim_ids = DB.get_all_sim_ids()
    for sid in sim_ids:
        SingleSimulationPlotter.plot_result(sim_id=sid)

if __name__ == '__main__':
    plot_heat_maps_stability()