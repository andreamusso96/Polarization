from config import DB_URL

from sqlalchemy.engine import create_engine
from sqlalchemy import MetaData

engine = create_engine(url=DB_URL, future=True)
metadata_obj = MetaData()