import os

is_cluster = False
CODE_PATH = os.path.dirname(os.path.realpath(__file__))
if "cluster" in CODE_PATH:
    is_cluster = True

if is_cluster:
    absolute_path_to_db = '/cluster/scratch/anmusso/PolarizationDB/cluster_sim_db_v6_with_nstd.db'
else:
    absolute_path_to_db = '/Users/anmusso/Desktop/PhD/Polarization/DB/sim_db_v8.db'

DB_URL = f'sqlite:////{absolute_path_to_db}'