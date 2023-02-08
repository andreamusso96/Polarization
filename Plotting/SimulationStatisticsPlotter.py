from Database.DB import DB, ParameterValue
from typing import List
from Plotting.HeatMap import HeatMapPlotter, HeatMap


class SimulationStatisticsHeatMap(HeatMap):
    def __init__(self, x_axis: str, y_axis: str, z_val: str, f_name: str, param_values: List[ParameterValue]):
        super().__init__(x_axis=x_axis, y_axis=y_axis, z_val=z_val, f_name=f_name)
        self.param_values = param_values


class SimulationStatisticPlotter:
    oscillating_sim_ids = [13, 14, 15, 151]

    @staticmethod
    def plot_heat_map(heat_maps: List[SimulationStatisticsHeatMap]):
        hm_dfs = []
        for heat_map in heat_maps:
            sim_ids = SimulationStatisticPlotter._get_sim_ids(param_values=heat_map.param_values)
            hm_df = DB.get_heat_map_sim_statistics(x_axis=heat_map.x_axis, y_axis=heat_map.y_axis, z_val=heat_map.z_val,
                                                   f_name=heat_map.f_name, sim_ids=sim_ids)
            hm_dfs.append(hm_df)

        HeatMapPlotter.plot_heat_maps(heat_maps=hm_dfs)

    @staticmethod
    def _get_sim_ids(param_values: List[ParameterValue]):
        sim_ids = DB.get_sim_ids(param_values=param_values)
        sim_ids = list(set(sim_ids) - set(SimulationStatisticPlotter.oscillating_sim_ids))
        return sim_ids
