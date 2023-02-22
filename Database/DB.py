from Database.Engine import engine
from Database.Tables import GetTable
from Database.Parameters import DBParameters, ParameterValue, ParameterRange
from Database.SimIds import DBSimId
from Database.SimulationStatistics import DBStatistics
from Database.Result import DBResult
from Database.SimulationBookKeeping import BookKeeper
from Database.HeatMaps import DBHeatMaps
from Database.ResultStability import DBStability
from Database.ParametersARM import DBParametersARM
from Database.ResultARM import DBResultARM
from Database.StatisticsARM import DBStatisticsARM
from Simulation.Parameters import SimulationParameters
from Simulation.SimulationResult import SimulationResult
from Stability.StabilityAnalysis import StabilityResult
from SimulationAnalysis.SimulationStatistics import SimulationStatistics
from ARMSimulation.ARMParameters import ARMSimulationParameters
from ARMSimulation.ARMResult import ARMSimulationResult
from ARMSimulation.ARMStatistics import ARMStatistics
from typing import List
import pandas as pd
from sqlalchemy import text


class DB:
    busy_timeout = 10*60*1000  # Time before sqlalchemy throws timeout error in milliseconds

    # Bookkeeping
    @staticmethod
    def setup_database_for_simulation(params: SimulationParameters):
        with engine.begin() as conn:
            BookKeeper.set_up_database_for_simulation(conn=conn, params=params)

    @staticmethod
    def set_flags_simulation_complete(sim_id: int, success: bool):
        with engine.begin() as conn:
            BookKeeper.set_flags_simulation_complete(conn=conn, sim_id=sim_id, success=success)

    # SimulationParameters
    @staticmethod
    def get_simulation_parameters(sim_ids: List[int]) -> List[SimulationParameters]:
        with engine.begin() as conn:
            return DBParameters.get_simulation_parameters(conn=conn, sim_ids=sim_ids)

    # Simulation statistics
    @staticmethod
    def get_simulation_statistics(sim_ids: List[int]) -> pd.DataFrame:
        with engine.begin() as conn:
            return DBStatistics.get_simulation_statistics(conn=conn, sim_ids=sim_ids)

    @staticmethod
    def insert_simulation_statistics(simulation_statistics: SimulationStatistics) -> None:
        with engine.begin() as conn:
            DBStatistics.insert_simulation_statistics(conn=conn, simulation_statistics=simulation_statistics)

    # Simulation Results
    @staticmethod
    def get_simulation_result(sim_id: int) -> SimulationResult:
        with engine.begin() as conn:
            return DBResult.get_simulation_result(conn=conn, sim_id=sim_id)

    @staticmethod
    def insert_simulation_result_in_distribution_table(simulation_result: SimulationResult) -> None:
        with engine.begin() as conn:
            conn.execute(text(f"PRAGMA busy_timeout = {DB.busy_timeout}"))
            DBResult.insert_result_in_distribution_table(conn=conn, simulation_result=simulation_result)

    # Stability Result
    @staticmethod
    def get_stability_results(param_values: List[ParameterValue] = None) -> List[StabilityResult]:
        with engine.begin() as conn:
            return DBStability.get_stability_results(conn=conn, param_values=param_values)

    @staticmethod
    def insert_stability_result(stability_result: StabilityResult) -> None:
        with engine.begin() as conn:
            DBStability.insert_stability_result(conn=conn, stability_result=stability_result)

    # SimID
    @staticmethod
    def get_sim_ids(arm: bool = False, param_ranges: List[ParameterRange] = None, param_values: List[ParameterValue] = None, method: str = 'intersection') -> List[int]:
        with engine.begin() as conn:
            conn.execute(text(f"PRAGMA busy_timeout = {DB.busy_timeout}"))
            return DBSimId.get_sim_ids(conn=conn, arm=arm, param_ranges=param_ranges, param_values=param_values, method=method)

    # Heat maps
    @staticmethod
    def get_heat_map_sim_statistics(x_axis: str, y_axis: str, z_val: str, f_name: str, sim_ids: List[int]) -> pd.DataFrame:
        with engine.begin() as conn:
            return DBHeatMaps.get_heat_map_sim_statistics(conn=conn, x_axis=x_axis, y_axis=y_axis, z_val=z_val, f_name=f_name, sim_ids=sim_ids)

    @staticmethod
    def get_heat_map_stability(x_axis: str, y_axis: str, z_val: str, f_name: str) -> pd.DataFrame:
        with engine.begin() as conn:
            return DBHeatMaps.get_heat_map_stability(conn=conn, x_axis=x_axis, y_axis=y_axis, z_val=z_val, f_name=f_name)

    # ARM Parameters
    @staticmethod
    def get_arm_parameters(sim_ids: List[int]) -> List[ARMSimulationParameters]:
        with engine.begin() as conn:
            return DBParametersARM.get_simulation_parameters(conn=conn, sim_ids=sim_ids)

    @staticmethod
    def insert_arm_parameters(params: ARMSimulationParameters):
        with engine.begin() as conn:
            DBParametersARM.insert_parameters(conn=conn, params=params)

    @staticmethod
    def delete_arm_params(sim_ids: List[int]) -> None:
        with engine.begin() as conn:
            DBParametersARM.delete_parameters(conn=conn, sim_ids=sim_ids)

    # ARM Results
    @staticmethod
    def get_arm_result(sim_id: int) -> ARMSimulationResult:
        with engine.begin() as conn:
            conn.execute(text(f"PRAGMA busy_timeout = {DB.busy_timeout}"))
            return DBResultARM.get_result(conn=conn, sim_id=sim_id)

    @staticmethod
    def insert_arm_result(arm_result: ARMSimulationResult):
        with engine.begin() as conn:
            conn.execute(text(f"PRAGMA busy_timeout = {DB.busy_timeout}"))
            DBResultARM.insert_arm_result_in_table(conn=conn, arm_simulation_result=arm_result)

    # ARM Statistics
    @staticmethod
    def get_arm_statistics(sim_ids: List[int]) -> pd.DataFrame:
        with engine.begin() as conn:
            return DBStatisticsARM.get_arm_statistics(conn=conn, sim_ids=sim_ids)

    @staticmethod
    def insert_arm_statistics(arm_statistics: ARMStatistics) -> None:
        with engine.begin() as conn:
            conn.execute(text(f"PRAGMA busy_timeout = {DB.busy_timeout}"))
            DBStatisticsARM.insert_arm_statistics(conn=conn, arm_statistics=arm_statistics)
    # Tables
    @staticmethod
    def get_all_table_names() -> List[str]:
        return GetTable.get_all_table_names()