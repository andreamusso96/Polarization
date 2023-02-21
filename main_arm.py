from ARMSimulation.ARM import ARM
from Database.DB import DB, ParameterRange
import time
import sys

if __name__ == '__main__':
    sim_id_low = int(sys.argv[1])
    sim_id_high = int(sys.argv[2])
    print('SIM IDs', sim_id_low, sim_id_high)
    ids_to_simulates = DB.get_sim_ids(param_ranges=[ParameterRange(name='sim_id', min_val=sim_id_low, max_val=sim_id_high)])
    params = DB.get_arm_parameters(sim_ids=ids_to_simulates)
    for p in params:
        print('SIM ID', p.sim_id)
        arm = ARM(sim_params=p)
        result = arm.run_simulation()
        print('INSERTING')
        DB.insert_arm_result(arm_result=result)
        print('DONE')

