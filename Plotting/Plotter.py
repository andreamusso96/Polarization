from Plotting.SimulationStatisticsPlotter import SimulationStatisticPlotter, SimulationStatisticsHeatMap
from Plotting.SingleSimulation import SingleSimulationPlotter
import pandas as pd

from Plotting.HeatMap import HeatMapPlotter, HeatMap
from Plotting.SingleSimulation import SingleSimulationPlot
from Database.DB import DB, ParameterRange, ParameterValue
from typing import List


class StabilityPlotter:
    @staticmethod
    def plot_heat_map_sim_statistic(heat_maps: List[HeatMap]) -> None:
        heat_maps_dfs = [DB.get_heat_map_stability(x_axis=heat_map.x_axis, y_axis=heat_map.y_axis, z_val=heat_map.z_val,
                                           f_name=heat_map.f_name) for heat_map in heat_maps]
        HeatMapPlotter.plot_heat_maps(heat_maps=heat_maps_dfs)


def plot_heat_maps_sim_statistics():
    heat_maps = [SimulationStatisticsHeatMap(x_axis='t', y_axis='e', z_val='l2_norm_diff', f_name='avg', param_values=[ParameterValue(name='r', value=0.5)]),
                 SimulationStatisticsHeatMap(x_axis='t', y_axis='e', z_val='l2_norm_diff', f_name='avg', param_values=[ParameterValue(name='r', value=0.39999999999999997)]),
                 SimulationStatisticsHeatMap(x_axis='t', y_axis='e', z_val='l2_norm_diff', f_name='avg', param_values=[ParameterValue(name='r', value=0.3)])]
    SimulationStatisticPlotter.plot_heat_map(heat_maps=heat_maps)


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
    from Database.Parameters import ParameterValue
    import numpy as np
    ids = DB.get_ids_with_parameter_value(param_value=ParameterValue(name='complete', value=True))
    np_ids = np.array(ids)
    a1 = np.array([18, 27, 31, 32, 33, 34, 52, 53, 81, 96, 109, 111, 119, 127, 128, 129, 130, 133, 135, 136, 143, 144])
    a2temp = np_ids[np_ids < 2000]
    a2 = a2temp[a2temp > 1000] - 1000
    a3 = np_ids[2000 < np_ids] - 3000
    a12 = np.intersect1d(a1, a2)
    a13 = np.intersect1d(a1, a3)
    a123 = np.intersect1d(a12, a3)
    special_ids = [int(a) for a in a13]
    for sid in special_ids:
        SingleSimulationPlotter.plot_result(sim_id=sid)
        #SingleSimulationPlotter.plot_result(sim_id=sid + 1000)
        SingleSimulationPlotter.plot_result(sim_id=sid + 3000)

def plot_test():
    from Database.Parameters import ParameterValue
    ids = DB.get_ids_with_parameter_value(param_value=ParameterValue(name='complete', value=True))
    for sid in ids:
        SingleSimulationPlotter.plot_result(sim_id=sid)


def plot_high_order_integrator():
    ids = DB.get_all_sim_ids()
    for sid in ids:
        SingleSimulationPlotter.plot_result(sim_id=sid)

def high_variance_simulations():
    ids = DB.get_all_sim_ids()
    high_variance = []
    for sid in ids:
        res = DB.get_simulation_result(sim_id=sid)
        l2_norm = res.get_l2_norm_df()
        if l2_norm['l2_norm'].max() > 5:
            high_variance.append(sid)
            SingleSimulationPlotter.plot_result(sim_id=sid)
    return high_variance

def low_r():
    ids = DB.get_sim_ids(param_values=[ParameterValue(name='r', value=0.5)])
    for i in ids:
        SingleSimulationPlotter.plot_result(sim_id=i)

if __name__ == '__main__':
    SingleSimulationPlotter.plot_result(sim_id=1)
