from Database.Tables import GetTable
from sqlalchemy import select
from sqlalchemy.engine import Connection
from typing import List


class DBSimIdsARM:
    @staticmethod
    def get_sim_ids(conn: Connection, incomplete: bool) -> List[int]:
        arm_sim_table = GetTable.get_arm_simulation_table()
        if incomplete:
            stmt = select(arm_sim_table.c.sim_id).where(arm_sim_table.c.complete==False)
        else:
            stmt = select(arm_sim_table.c.sim_id)

        sim_ids = conn.execute(stmt).scalars().all()
        return sim_ids

