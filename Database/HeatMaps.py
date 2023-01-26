from Database.Engine import engine
from Database.Tables import GetTable
from sqlalchemy import func, select
import pandas as pd
from typing import List


class DBHeatMaps:
    @staticmethod
    def get_heat_map_df(x_axis: str, y_axis: str, z_val: str, f_name: str, sim_ids: List[int]) -> pd.DataFrame:
        sim_statistics_table = GetTable.get_simulation_statistics_table()
        sim_table = GetTable.get_simulation_table()

        # f is a sqlalchemy generated function via func.FUNCTION_NAME
        f = getattr(func, f_name)
        with engine.begin() as conn:
            stmt = select(f(getattr(sim_statistics_table.c, z_val)), getattr(sim_table.c, x_axis), getattr(sim_table.c, y_axis)).join(sim_table, sim_table.c.sim_id==sim_statistics_table.c.sim_id).filter(sim_statistics_table.c.sim_id.in_(sim_ids)).group_by(getattr(sim_table.c, x_axis), getattr(sim_table.c, y_axis))
            res = conn.execute(stmt).all()
            df = pd.DataFrame(data=res, columns=['z', 'x', 'y']).pivot(index='y', columns='x', values='z').rename_axis(
                y_axis).rename_axis(x_axis, axis='columns')
            df.name = z_val + f' ({f_name})'
        return df