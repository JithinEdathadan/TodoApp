from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY:str
    ALGORITHM:str
    JWT_TOKEN_EXPIRY:int # in minute
    DB_USER_NAME:str
    DB_PASSWORD:str
    DB_HOST:str
    DB_PORT:str
    DB_NAME:str
    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    return Settings()