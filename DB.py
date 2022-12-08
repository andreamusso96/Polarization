from Simulation import SimulationResult, Parameters
from DistributionGenerator import DistributionParameters
from config import DB_URL

from sqlalchemy.engine import create_engine
from sqlalchemy import Column, Table, MetaData, Float, Integer, String, Boolean, insert, select, update
import pandas as pd
from typing import Tuple, List

engine = create_engine(url=DB_URL, future=True)
metadata_obj = MetaData()


class DBGet:
    @staticmethod
    def get_simulation_result(sim_id: int) -> Tuple[pd.DataFrame, pd.DataFrame, Parameters]:
        params = DBGet.get_parameters_simulation(sim_id=sim_id)
        l2_norm_table = Table(f"l2_norm_{sim_id}", metadata_obj, autoload_with=engine)
        distributions_table = Table(f"distributions_{sim_id}", metadata_obj, autoload_with=engine)

        # Convert to DataFrame
        with engine.begin() as conn:
            stmt_l2_norm = select(l2_norm_table)
            l2_norm_df = pd.read_sql_query(sql=stmt_l2_norm, con=conn)

            stmt_distributions = select(distributions_table)
            distributions_df = pd.read_sql_query(sql=stmt_distributions, con=conn)

        return l2_norm_df, distributions_df, params

    @staticmethod
    def get_last_sim_id() -> int:
        sim_table = Table("sim_table", metadata_obj, autoload_with=engine)
        with engine.begin() as conn:
            stmt = select(sim_table.c.sim_id)
            res = conn.execute(stmt).scalars().all()
            last_sim_id = sorted(res)[-1]

        return last_sim_id

    @staticmethod
    def get_ids_incomplete_simulations() -> List[int]:
        sim_table = Table("sim_table", metadata_obj, autoload_with=engine)
        with engine.begin() as conn:
            stmt = select(sim_table.c.sim_id).where(sim_table.c.complete == False)
            sim_ids = conn.execute(stmt).scalars().all()

        return sim_ids

    @staticmethod
    def get_ids_complete_simulations() -> List[int]:
        sim_table = Table("sim_table", metadata_obj, autoload_with=engine)
        with engine.begin() as conn:
            stmt = select(sim_table.c.sim_id).where(sim_table.c.complete == True)
            sim_ids = conn.execute(stmt).scalars().all()

        return sim_ids

    @staticmethod
    def get_parameters_incomplete_simulations() -> List[Parameters]:
        sim_table = Table("sim_table", metadata_obj, autoload_with=engine)
        with engine.begin() as conn:
            stmt = select(sim_table).where(sim_table.c.complete == False)
            res = conn.execute(stmt).all()
            parameters_incomplete_simulations = []
            for row in res:
                p = DBGet._sim_table_row_to_parameters(row=row)
                parameters_incomplete_simulations.append(p)

        return parameters_incomplete_simulations

    @staticmethod
    def get_parameters_simulation(sim_id: int) -> Parameters:
        sim_table = Table("sim_table", metadata_obj, autoload_with=engine)
        with engine.begin() as conn:
            stmt = select(sim_table).where(sim_table.c.sim_id == sim_id)
            res = conn.execute(stmt).all()
            p = DBGet._sim_table_row_to_parameters(row=res[0])

        return p

    @staticmethod
    def _sim_table_row_to_parameters(row) -> Parameters:
        p = Parameters(sim_id=row.sim_id, t=row.t, r=row.r, e=row.e,
                   d0_parameters=DistributionParameters.from_string(row.d0_parameters), s_max=row.s_max,
                   n_save_distributions=row.n_save_distributions)
        return p


class DBCreateTable:
    @staticmethod
    def create_simulation_table() -> Table:
        simulation_table = Table("sim_table", metadata_obj,
                                 Column("sim_id", Integer, primary_key=True),
                                 Column("t", Float),
                                 Column("r", Float),
                                 Column("e", Float),
                                 Column("s_max", Integer),
                                 Column("n_save_distributions", Integer),
                                 Column("d0_parameters", String),
                                 Column("complete", Boolean))
        metadata_obj.create_all(bind=engine, tables=[simulation_table])
        return simulation_table

    @staticmethod
    def create_l2_norm_table(sim_id: int) -> Table:
        l2_norm_table = Table(f"l2_norm_{sim_id}",
                              metadata_obj,
                              Column("time", Integer, primary_key=True),
                              Column("l2_norm", Float))
        metadata_obj.create_all(bind=engine, tables=[l2_norm_table])
        return l2_norm_table

    @staticmethod
    def create_distributions_table(simulation_result: SimulationResult) -> Table:
        distributions_table = Table(f"distributions_{simulation_result.params.sim_id}",
                                    metadata_obj,
                                    Column("index", Integer, primary_key=True),
                                    Column("time", Integer),
                                    Column("left_bin", Float),
                                    Column("dist_value", Float))
        metadata_obj.create_all(bind=engine, tables=[distributions_table])
        return distributions_table


class DBSet:
    @staticmethod
    def insert_simulation_in_simulation_table(params: Parameters):
        sim_table = Table("sim_table", metadata_obj, autoload_with=engine)
        with engine.begin() as conn:
            stmt = insert(sim_table).values(sim_id=params.sim_id, t=params.t, r=params.r, e=params.e, s_max=params.s_max,
                                            n_save_distributions=params.n_save_distributions, d0_parameters=params.d0_parameters.to_string(), complete=False)
            conn.execute(stmt)

    @staticmethod
    def set_simulation_complete_to_true(sim_id: int):
        sim_table = Table("sim_table", metadata_obj, autoload_with=engine)
        with engine.begin() as conn:
            stmt = update(sim_table).values(complete=True).where(sim_table.c.sim_id == sim_id)
            conn.execute(stmt)

    @staticmethod
    def insert_result_in_l2_norm_table(simulation_result: SimulationResult, l2_norm_table: Table):
        with engine.begin() as conn:
            for s in range(len(simulation_result.l2_norm)):
                stmt = insert(l2_norm_table).values(time=s, l2_norm=simulation_result.l2_norm[s])
                conn.execute(stmt)

    @staticmethod
    def insert_result_in_distribution_table(simulation_result: SimulationResult, distributions_table: Table):
        with engine.begin() as conn:
            for s in simulation_result.distributions:
                left_bins = simulation_result.distributions[s].get_left_bins()
                dist_values = simulation_result.distributions[s].d
                for i in range(left_bins.shape[0]):
                    stmt = insert(distributions_table).values(time=s, left_bin=left_bins[i], dist_value=dist_values[i])
                    conn.execute(stmt)


class DB:
    @staticmethod
    def insert_simulation_parameters(simulation_parameters: Parameters):
        DBSet.insert_simulation_in_simulation_table(params=simulation_parameters)

    @staticmethod
    def insert_simulation_result(simulation_result: SimulationResult):
        l2_norm_table = DBCreateTable.create_l2_norm_table(sim_id=simulation_result.params.sim_id)
        DBSet.insert_result_in_l2_norm_table(simulation_result=simulation_result, l2_norm_table=l2_norm_table)
        distributions_table = DBCreateTable.create_distributions_table(simulation_result=simulation_result)
        DBSet.insert_result_in_distribution_table(simulation_result=simulation_result, distributions_table=distributions_table)
        DBSet.set_simulation_complete_to_true(sim_id=simulation_result.params.sim_id)

    @staticmethod
    def get_simulation_result(sim_id: int) -> Tuple[pd.DataFrame, pd.DataFrame, Parameters]:
        return DBGet.get_simulation_result(sim_id=sim_id)

    @staticmethod
    def get_last_sim_id() -> int:
        return DBGet.get_last_sim_id()

    @staticmethod
    def get_ids_incomplete_simulations() -> List[int]:
        return DBGet.get_ids_incomplete_simulations()

    @staticmethod
    def get_parameters_incomplete_simulations() -> List[Parameters]:
        return DBGet.get_parameters_incomplete_simulations()

    @staticmethod
    def get_parameters_simulation(sim_id: int) -> Parameters:
        return DBGet.get_parameters_simulation(sim_id=sim_id)

    @staticmethod
    def get_complete_jobs() -> List[int]:
        return DBGet.get_ids_complete_simulations()



if __name__ == '__main__':
    #DBCreateTable.create_simulation_table()
    print(DB.get_complete_jobs())
