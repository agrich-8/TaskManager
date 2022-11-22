import os

from pydantic import BaseSettings


file_path = os.path.abspath(os.getcwd())+"\database.db"

SECRET_KEY = 'CsJWl1OLyjkw8RJHEvAHoAtpnlbF/+fYd02D+lpAoOE='
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Settings(BaseSettings):

    SQLALCHEMY_DATABASE_URL = "sqlite:///"+file_path

    server_host: str = '127.0.0.1'
    server_port: int = 8003

settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
