
is_cluster = False
if is_cluster:
    absolute_path_to_db = 'PATH IN THE CLUSTER BETTER'
else:
    absolute_path_to_db = '/Users/anmusso/Desktop/PhD/Polarization/DB/sim_db.db'

DB_URL = f'sqlite:////{absolute_path_to_db}'
