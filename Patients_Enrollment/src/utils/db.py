from sqlalchemy import create_engine
from config.config import DB_URL

engine = create_engine(
    DB_URL,
    pool_pre_ping=True
)

def get_engine():
    return engine