from Database.DB import DB, ParameterRange, ParameterValue
from ARMSimulation.ARMStatisticsCalculator import ARMStatisticsCalculator
import sys


if __name__ == '__main__':
    sim_id_low = int(sys.argv[1])
    sim_id_high = int(sys.argv[2])
    print('SIM IDs', sim_id_low, sim_id_high)
    ids_to_compute_statistics = DB.get_sim_ids(arm=True, param_ranges=[ParameterRange(name='sim_id', min_val=sim_id_low, max_val=sim_id_high)])
    ARMStatisticsCalculator.save_arm_stats(sim_ids=ids_to_compute_statistics)
    print('DONE')