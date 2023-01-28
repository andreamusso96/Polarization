from Database.Tables import GetTable, CreateTable
from Database.Parameters import DBParameters
from Simulation.Parameters import SimulationParameters
from sqlalchemy import update
from sqlalchemy.engine import Connection


class BookKeeper:
    @staticmethod
    def set_up_database_for_simulation(conn: Connection, params: SimulationParameters):
        DBParameters.insert_parameters(conn=conn, params=params)
        conn.commit()
        CreateTable.create_distributions_table(sim_id=params.sim_id)

    @staticmethod
    def set_flags_simulation_complete(conn: Connection, sim_id: int, success: bool):
        BookKeeper.set_simulation_complete_to_true(conn=conn, sim_id=sim_id)
        BookKeeper.set_simulation_success(conn=conn, sim_id=sim_id, success=success)

    @staticmethod
    def set_simulation_complete_to_true(conn: Connection, sim_id: int):
        sim_table = GetTable.get_simulation_table()
        stmt = update(sim_table).values(complete=True).where(sim_table.c.sim_id == sim_id)
        conn.execute(stmt)

    @staticmethod
    def set_simulation_success(conn: Connection, sim_id: int, success: bool):
        sim_table = GetTable.get_simulation_table()
        stmt = update(sim_table).values(success=success).where(sim_table.c.sim_id == sim_id)
        conn.execute(stmt)