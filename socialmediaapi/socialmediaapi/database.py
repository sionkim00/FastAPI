import databases
import sqlalchemy
from config import config

# Store information about tables & columns
metadata = sqlalchemy.MetaData()

# Allow sqlalchemy to connect to sqlite
engine = sqlalchemy.create_engine(
    config.DATABASE_URL, connect_args={"check_same_thread": False}
)

# Tell engine to use the metadata to create tables and columns
metadata.create_all(engine)

# Database object we can interact
database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK
)
