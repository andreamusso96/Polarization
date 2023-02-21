import os
import numpy as np
import pandas as pd

from Database.DB import DB
def run():
    fnames = np.load('fnames.npy')
    for fname in fnames:
        os.system(f'sacct --format=JobID,Elapsed,State --job {fname}')

# Get all table names in the database

def get_table_names():
    table_names = DB.get_all_table_names()
    print(table_names)


def refactor_db():
    from Database.DB import DBResultARM, engine
    table_names = DB.get_all_table_names()
    for table_name in table_names:
        if 'arm_result' in table_name:
            sim_id = int(table_name.split('_')[-1])
            with engine.begin() as conn:
                DBResultARM._set_arm_simulation_complete_flag(conn, sim_id)


def refactor_db2():
    sim_ids = DB.get_sim_ids(arm=True)
    params = DB.get_arm_parameters(sim_ids)
    ids_to_delete = []
    for p in params:
        if 0.09 < p.e < 0.11 or 0.29 < p.e < 0.31:
            continue
        else:
            ids_to_delete.append(p.sim_id)

    DB.delete_arm_params(sim_ids=ids_to_delete)


def get_complete_sims():
    table_names = DB.get_all_table_names()
    complete_sims = []
    for table_name in table_names:
        if 'arm_result' in table_name:
            sim_id = int(table_name.split('_')[-1])
            complete_sims.append(sim_id)
    return complete_sims


def refactor_db3():
    from Database.DB import engine, GetTable
    from sqlalchemy import update, select
    sim_ids = DB.get_sim_ids(arm=True)
    arm_sim_table = GetTable.get_arm_simulation_table()
    complete_sims = get_complete_sims()
    for new_sim_id, old_sim_id in enumerate(sim_ids):
        with engine.begin() as conn:
            if old_sim_id in complete_sims:
                table = GetTable.get_table(table_name=f'arm_result_{old_sim_id}')
                stmt = select(table)
                df = pd.read_sql(con=conn, sql=stmt)
                df.to_sql(con=conn, name=f'arm_result_{new_sim_id}', index=False)
                table.drop(bind=engine)

            stmt = update(arm_sim_table).where(arm_sim_table.c.sim_id == old_sim_id).values(sim_id=new_sim_id)
            conn.execute(stmt)


def refactor_db4():
    from Database.DB import engine, GetTable
    from sqlalchemy import update, select
    with engine.begin() as conn:
        table = GetTable.get_arm_simulation_table()
        stmt = select(table)
        df = pd.read_sql(con=conn, sql=stmt)

    return df

def refactor_db6():
    from Database.DB import engine, GetTable
    with engine.begin() as conn:
        table_names = DB.get_all_table_names()
        for table_name in table_names:
            if 'arm_result' in table_name:
                table = GetTable.get_table(table_name=table_name)
                table.drop(bind=engine)
            if 'arm_sim' in table_name:
                table = GetTable.get_table(table_name=table_name)
                table.drop(bind=engine)

        conn.commit()



if __name__ == '__main__':
    run()