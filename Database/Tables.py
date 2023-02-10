from Database.Engine import engine, metadata_obj
from sqlalchemy import Column, Table, Float, Integer, String, Boolean


class TableNames:
    sim_table = "sim_table"
    sim_statistics = "sim_statistics"
    stability = "stability"


class GetTable:
    @staticmethod
    def get_simulation_table() -> Table:
        sim_table = Table("sim_table", metadata_obj, autoload_with=engine)
        return sim_table

    @staticmethod
    def get_simulation_statistics_table() -> Table:
        sim_stats = Table("sim_statistics", metadata_obj, autoload_with=engine)
        return sim_stats

    @staticmethod
    def get_stability_stable() -> Table:
        stability_table = Table("stability", metadata_obj, autoload_with=engine)
        return stability_table

    @staticmethod
    def get_distributions_table(sim_id: int) -> Table:
        distributions = Table(f"distributions_{sim_id}", metadata_obj, autoload_with=engine)
        return distributions

    @staticmethod
    def get_table(table_name: str) -> Table:
        table = Table(table_name, metadata_obj, autoload_with=engine)
        return table


class CreateTable:
    @staticmethod
    def create_simulation_table() -> Table:
        simulation_table = Table("sim_table", metadata_obj,
                                 Column("sim_id", Integer, primary_key=True),
                                 Column("t", Float),
                                 Column("r", Float),
                                 Column("e", Float),
                                 Column("total_time_span", Integer),
                                 Column("block_time_span", Integer),
                                 Column("n_save_distributions_block", Integer),
                                 Column("support", Float),
                                 Column("bin_size", Float),
                                 Column("boundary", Float),
                                 Column("method", String),
                                 Column("num_processes", Integer),
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
    def create_stability_table() -> Table:
        stability_table = Table("stability", metadata_obj,
                                Column("pk", Integer, primary_key=True),
                                Column("t", Float),
                                Column("r", Float),
                                Column("e", Float),
                                Column("max_eig", Float),
                                Column("stable", Boolean),
                                Column("max_frequency", Integer),
                                Column("max_eigs_far_from_max_frequency", Boolean))
        metadata_obj.create_all(bind=engine, tables=[stability_table])
        return stability_table

    @staticmethod
    def create_distributions_table(sim_id: int) -> Table:
        distributions_table = Table(f"distributions_{sim_id}",
                                    metadata_obj,
                                    Column("index", Integer, primary_key=True),
                                    Column("time", Integer),
                                    Column("left_bin", Float),
                                    Column("dist_value", Float))
        metadata_obj.create_all(bind=engine, tables=[distributions_table])
        return distributions_table


if __name__ == '__main__':
    CreateTable.create_stability_table()