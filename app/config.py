import os

from pydantic import BaseSettings


# file_path = os.path.abspath(os.getcwd())+r"\API\app\db\database.db"

SECRET_KEY = 'CsJWl1OLyjkw8RJHEvAHoAtpnlbF/+fYd02D+lpAoOE='
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Settings(BaseSettings):

    DB_USER = "root"
    DB_PASSWORD = "88uUheEWfk3"
    DB_HOST = "localhost"
    DATABASE = "tmdb"

    SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DATABASE}' #"sqlite:///"+file_path
    server_host: str = '127.0.0.1'
    server_port: int = 8003

settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
