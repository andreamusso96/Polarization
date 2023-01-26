from Simulation.Simulator import SimulationResult
from Database.Engine import engine, metadata_obj
from sqlalchemy import Column, Table, Float, Integer, String, Boolean


class GetTable:
    @staticmethod
    def get_simulation_table() -> Table:
        sim_table = Table("sim_table", metadata_obj, autoload_with=engine)
        return sim_table

    @staticmethod
    def get_simulation_statistics_table():
        sim_stats = Table("sim_statistics", metadata_obj, autoload_with=engine)
        return sim_stats

    @staticmethod
    def get_l2_norm_table(sim_id: int):
        l2_norm = Table(f"l2_norm_{sim_id}", metadata_obj, autoload_with=engine)
        return l2_norm

    @staticmethod
    def get_distributions_table(sim_id: int):
        distributions = Table(f"distributions_{sim_id}", metadata_obj, autoload_with=engine)
        return distributions


class CreateTable:
    @staticmethod
    def create_simulation_table() -> Table:
        simulation_table = Table("sim_table", metadata_obj,
                                 Column("sim_id", Integer, primary_key=True),
                                 Column("t", Float),
                                 Column("r", Float),
                                 Column("e", Float),
                                 Column("s_max", Integer),
                                 Column("n_save_distributions", Integer),
                                 Column("bound", Float),
                                 Column("bin_size", Float),
                                 Column("total_density_threshold", Float),
                                 Column("d0_parameters", String),
                                 Column("complete", Boolean),
                                 Column("success", Boolean))
        metadata_obj.create_all(bind=engine, tables=[simulation_table])
        return simulation_table

    @staticmethod
    def create_simulation_statistics_table() -> Table:
        simulation_statistics_table = Table("sim_statistics", metadata_obj,
                                            Column("sim_id", Integer, primary_key=True),
                                            Column("l2_norm_end", Float),
                                            Column("l2_norm_diff", Float))
        metadata_obj.create_all(bind=engine, tables=[simulation_statistics_table])
        return simulation_statistics_table

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