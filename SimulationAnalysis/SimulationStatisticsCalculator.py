from Database.Result import Result
from Database.DB import DB
from SimulationAnalysis.SimulationStatistics import SimulationStatistics

class SimulationStatisticsCalculator:
    def __init__(self, sim_result: Result):
        self.sim_result = sim_result
        self.sim_id = sim_result.params.sim_id

    def compute_l2_norm_end(self) -> float:
        return self.sim_result.l2_norm_df.values[-1]

    def compute_l2_norm_diff(self) -> float:
        return self.sim_result.l2_norm_df.values[0] - self.sim_result.l2_norm_df.values[-1]

    def get_simulation_statistics(self) -> SimulationStatistics:
        return SimulationStatistics(sim_id=self.sim_id,
                                    l2_norm_diff=self.compute_l2_norm_diff(),
                                    l2_norm_end=self.compute_l2_norm_end())


class ComputeSimulationStatistics:
    @staticmethod
    def compute_simulation_statistics(sim_id: int) -> SimulationStatistics:
        sim_result = DB.get_simulation_result(sim_id=sim_id)
        sim_stats_calculator = SimulationStatisticsCalculator(sim_result=sim_result)
        sim_stats = sim_stats_calculator.get_simulation_statistics()
        return sim_stats

    @staticmethod
    def compute_and_save_simulation_statistics(sim_id: int):
        sim_stats = ComputeSimulationStatistics.compute_simulation_statistics(sim_id=sim_id)
        DB.insert_simulation_statistics(simulation_statistics=sim_stats)
