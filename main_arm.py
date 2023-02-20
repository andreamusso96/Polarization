from ARMSimulation.ARM import ARM
from Database.DB import DB

import sys

if __name__ == '__main__':
    sim_id = int(sys.argv[1])
    print('SIM ID', sim_id)
    params = DB.get_arm_parameters(sim_ids=[sim_id])[0]
    arm = ARM(sim_params=params)
    result = arm.run_simulation()
    print('INSERTING')
    DB.insert_arm_result(arm_result=result)
    print('DONE', sim_id)