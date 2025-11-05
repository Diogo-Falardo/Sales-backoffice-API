from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    API_PREFIX:str
    DB_URL: str 
    JWT_SECRET: str
    ISSUER: str
    AUDIENCE: str
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
    