import databases
import sqlalchemy


metadata = sqlalchemy.MetaData()
database = databases.Database("sqlite:///API/sql/sqlite.db")
engine = sqlalchemy.create_engine("sqlite:///API/sql/sqlite.db")