from Database.Tables import GetTable
from Database.Engine import engine
from sqlalchemy import update


class BookKeeper:
    @staticmethod
    def set_simulation_complete_to_true(sim_id: int):
        sim_table = GetTable.get_simulation_table()
        with engine.begin() as conn:
            stmt = update(sim_table).values(complete=True).where(sim_table.c.sim_id == sim_id)
            conn.execute(stmt)

    @staticmethod
    def set_simulation_success(sim_id: int, success: bool):
        sim_table = GetTable.get_simulation_table()
        with engine.begin() as conn:
            stmt = update(sim_table).values(success=success).where(sim_table.c.sim_id == sim_id)
            conn.execute(stmt)