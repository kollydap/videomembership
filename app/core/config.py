from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
import os

os.environ["CQLENG_ALLOW_SCHEMA_MANAGEMENT"] = "1"


class Settings(BaseSettings):
    keyspace: str = Field(..., env="ASTRADB_KEYSPACE")
    secret_key: str = Field(..., env='SECRET_KEY')

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
