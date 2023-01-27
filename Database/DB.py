from Database.Engine import engine
from Database.Parameters import DBParameters, ParameterValue, ParameterRange
from Database.SimIds import DBSimId
from Database.Tables import CreateTable
from Database.SimulationStatistics import DBStatistics
from Database.Result import DBResult, Result
from Database.SimulationBookKeeping import BookKeeper
from Database.HeatMaps import DBHeatMaps
from Database.ResultStability import DBStability
from Simulation.Parameters import SimulationParameters
from Simulation.Simulator import SimulationResult
from Stability.StabilityAnalysis import StabilityResult
from SimulationAnalysis.SimulationStatistics import SimulationStatistics
from typing import List
import pandas as pd
from sqlalchemy import text
import time


class DB:
    busy_timeout = 120*1000  # Time before sqlalchemy throws timeout error in milliseconds

    # SimulationParameters
    @staticmethod
    def get_simulation_parameters(sim_id: int) -> SimulationParameters:
        with engine.begin() as conn:
            return DBParameters.get_simulation_parameters(conn=conn, sim_id=sim_id)

    @staticmethod
    def insert_simulation_parameters(simulation_parameters: SimulationParameters):
        with engine.begin() as conn:
            conn.execute(text(f"PRAGMA busy_timeout = {DB.busy_timeout}"))
            DBParameters.insert_parameters(conn=conn, params=simulation_parameters)

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
    def get_simulation_result(sim_id: int) -> Result:
        with engine.begin() as conn:
            return DBResult.get_simulation_result(conn=conn, sim_id=sim_id)

    @staticmethod
    def insert_simulation_result(simulation_result: SimulationResult):
        if not DB.is_database_locked():
            with engine.begin() as conn:
                CreateTable.create_l2_norm_table(sim_id=simulation_result.params.sim_id)
                CreateTable.create_distributions_table(simulation_result=simulation_result)
                DBResult.insert_simulation_result(conn=conn, sim_result=simulation_result)
                BookKeeper.set_simulation_complete_to_true(conn=conn, sim_id=simulation_result.params.sim_id)
                BookKeeper.set_simulation_success(conn=conn, sim_id=simulation_result.params.sim_id, success=simulation_result.res_scipy.success)
        else:
            time.sleep(10)
            DB.insert_simulation_result(simulation_result=simulation_result)

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