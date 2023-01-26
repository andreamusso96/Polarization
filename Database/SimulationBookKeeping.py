from Database.Tables import GetTable
from sqlalchemy import update
from sqlalchemy.engine import Connection


class BookKeeper:
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