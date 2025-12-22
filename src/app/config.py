import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 5432
    DB_NAME: str = "fastapi"
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )

    def get_db_url(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
