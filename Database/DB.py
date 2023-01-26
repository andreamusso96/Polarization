from Database.Parameters import DBParameters, ParameterValue, ParameterRange
from Database.SimIds import DBSimId
from Database.Tables import CreateTable
from Database.SimulationStatistics import DBStatistics
from Database.Result import DBResult, Result
from Database.SimulationBookKeeping import BookKeeper
from Database.HeatMaps import DBHeatMaps
from Simulation.Parameters import SimulationParameters
from Simulation.Simulator import SimulationResult
from typing import Tuple, List
import pandas as pd


class DB:
    # SimulationParameters
    @staticmethod
    def get_simulation_parameters(sim_id: int) -> SimulationParameters:
        return DBParameters.get_simulation_parameters(sim_id=sim_id)

    @staticmethod
    def insert_simulation_parameters(simulation_parameters: SimulationParameters):
        DBParameters.insert_parameters(params=simulation_parameters)

    # Simulation statistics
    @staticmethod
    def get_simulation_statistics(sim_id: int):
        return DBStatistics.get_simulation_statistics(sim_id=sim_id)

    @staticmethod
    def insert_simulation_statistics(sim_id: int):
        DBStatistics.insert_simulation_statistics(simulation_statistics=DB.get_simulation_statistics(sim_id=sim_id))

    # Simulation Results
    @staticmethod
    def get_simulation_result(sim_id: int) -> Result:
        return DBResult.get_simulation_result(sim_id=sim_id)

    @staticmethod
    def insert_simulation_result(simulation_result: SimulationResult):
        CreateTable.create_l2_norm_table(sim_id=simulation_result.params.sim_id)
        CreateTable.create_distributions_table(simulation_result=simulation_result)
        DBResult.insert_simulation_result(sim_result=simulation_result)
        BookKeeper.set_simulation_complete_to_true(sim_id=simulation_result.params.sim_id)
        BookKeeper.set_simulation_success(sim_id=simulation_result.params.sim_id, success=simulation_result.res_scipy.success)

    # SimID
    @staticmethod
    def get_all_sim_ids() -> List[int]:
        return DBSimId.get_all_sim_ids()

    @staticmethod
    def get_last_sim_id() -> int:
        return DBSimId.get_last_sim_id()

    @staticmethod
    def get_ids_with_parameter_value(param_value: ParameterValue) -> List[int]:
        return DBSimId.get_ids_with_parameter_value(param_value=param_value)

    @staticmethod
    def get_ids_in_parameter_ranges(param_ranges: List[ParameterRange], method: str) -> List[int]:
        return DBSimId.get_ids_in_parameter_ranges(param_ranges=param_ranges, method=method)

    # Heat maps
    @staticmethod
    def get_heat_map_df(x_axis: str, y_axis: str, z_val: str, f_name: str, sim_ids: List[int]) -> pd.DataFrame:
        return DBHeatMaps.get_heat_map_df(x_axis=x_axis, y_axis=y_axis, z_val=z_val, f_name=f_name, sim_ids=sim_ids)