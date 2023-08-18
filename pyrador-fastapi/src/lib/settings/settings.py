from pydantic import BaseSettings
from typing import Union

from .database_settings import DatabaseSettings


class Settings(BaseSettings):
    database: DatabaseSettings
    
    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"