from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str 
    DB_NAME: str
    BOT_TOKEN: str
    REDIS_URL: str = "redis://localhost:6379/0"

    @property
    def DATABASE_URL_asyncpg(self) ->str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding="utf-8",
        extra="ignore",
    )
settings = Settings()
