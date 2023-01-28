from Database.Engine import engine
from Database.Parameters import DBParameters, ParameterValue, ParameterRange
from Database.SimIds import DBSimId
from Database.SimulationStatistics import DBStatistics
from Database.Result import DBResult
from Database.SimulationBookKeeping import BookKeeper
from Database.HeatMaps import DBHeatMaps
from Database.ResultStability import DBStability
from Simulation.Parameters import SimulationParameters
from Simulation.SimulationResult import SimulationResult
from Stability.StabilityAnalysis import StabilityResult
from SimulationAnalysis.SimulationStatistics import SimulationStatistics
from typing import List
import pandas as pd
from sqlalchemy import text


class DB:
    busy_timeout = 120*1000  # Time before sqlalchemy throws timeout error in milliseconds
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
    def get_simulation_parameters(sim_id: int) -> SimulationParameters:
        with engine.begin() as conn:
            return DBParameters.get_simulation_parameters(conn=conn, sim_id=sim_id)

    # Simulation statistics
    @staticmethod
    def get_simulation_statistics(sim_id: int):
        with engine.begin() as conn:
            return DBStatistics.get_simulation_statistics(conn=conn, sim_id=sim_id)

    @staticmethod
    def insert_simulation_statistics(simulation_statistics: SimulationStatistics):
        with engine.begin() as conn:
            DBStatistics.insert_simulation_statistics(conn=conn, simulation_statistics=simulation_statistics)

    # Simulation Results
    @staticmethod
    def get_simulation_result(sim_id: int) -> SimulationResult:
        with engine.begin() as conn:
            return DBResult.get_simulation_result(conn=conn, sim_id=sim_id)

    @staticmethod
    def insert_simulation_result_in_distribution_table(simulation_result: SimulationResult):
        with engine.begin() as conn:
            conn.execute(text(f"PRAGMA busy_timeout = {DB.busy_timeout}"))
            DBResult.insert_result_in_distribution_table(conn=conn, simulation_result=simulation_result)

    # Stability Result
    @staticmethod
    def get_stability_result(t: float, r: float, e: float) -> StabilityResult:
        with engine.begin() as conn:
            return DBStability.get_stability_result(conn=conn, t=t, r=r, e=e)

    @staticmethod
    def get_all_stability_results() -> List[StabilityResult]:
        with engine.begin() as conn:
            return DBStability.get_all_stability_results(conn=conn)

    @staticmethod
    def insert_stability_result(stability_result: StabilityResult) -> None:
        with engine.begin() as conn:
            DBStability.insert_stability_result(conn=conn, stability_result=stability_result)

    # SimID
    @staticmethod
    def get_all_sim_ids() -> List[int]:
        with engine.begin() as conn:
            return DBSimId.get_all_sim_ids(conn=conn)

    @staticmethod
    def get_last_sim_id() -> int:
        with engine.begin() as conn:
            return DBSimId.get_last_sim_id(conn=conn)

    @staticmethod
    def get_ids_with_parameter_value(param_value: ParameterValue) -> List[int]:
        with engine.begin() as conn:
            return DBSimId.get_ids_with_parameter_value(conn=conn, param_value=param_value)

    @staticmethod
    def get_ids_in_parameter_ranges(param_ranges: List[ParameterRange], method: str) -> List[int]:
        with engine.begin() as conn:
            return DBSimId.get_ids_in_parameter_ranges(conn=conn, param_ranges=param_ranges, method=method)

    # Heat maps
    @staticmethod
    def get_heat_map_sim_statistics(x_axis: str, y_axis: str, z_val: str, f_name: str, sim_ids: List[int]) -> pd.DataFrame:
        with engine.begin() as conn:
            return DBHeatMaps.get_heat_map_sim_statistics(conn=conn, x_axis=x_axis, y_axis=y_axis, z_val=z_val, f_name=f_name, sim_ids=sim_ids)

    @staticmethod
    def get_heat_map_stability(x_axis: str, y_axis: str, z_val: str, f_name: str) -> pd.DataFrame:
        with engine.begin() as conn:
            return DBHeatMaps.get_heat_map_stability(conn=conn, x_axis=x_axis, y_axis=y_axis, z_val=z_val, f_name=f_name)
    # Check if database is locked

    @staticmethod
    def is_database_locked() -> bool:
        try:
            with engine.connect() as conn:
                # Try to insert a row with sim_id = -1 and see if it works, if it does not it will throw an error
                # If the error contains the string 'database is locked' then the database is locked
                conn.execute(text(f"PRAGMA busy_timeout = {300}"))
                p = DBParameters.get_simulation_parameters(conn=conn, sim_id=1)
                p.sim_id = -1
                DBParameters.insert_parameters(conn=conn, params=p)
                conn.rollback()
        except Exception as e:
            if 'database is locked' in str(e):
                print('DB is locked')
                return True
        return False