from ARMSimulation.ARMAverageNSTD import ARMAverageNSTD
from Database.DB import DB
import sys
import time

if __name__ == '__main__':
    sim_id = int(sys.argv[1])
    t_start = time.time()
    print('SIM ID', sim_id)
    params = DB.get_average_nstd_params(sim_id=sim_id)
    arm = ARMAverageNSTD(params=params)
    result = arm.run()
    DB.insert_average_nstd_result(average_nstd_result=result)
    print('DONE')
    print('TIME', time.time() - t_start)