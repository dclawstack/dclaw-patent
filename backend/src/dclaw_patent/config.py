from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "DClaw Patent"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/dclaw_patent"
    cors_origins: str = "*"

    class Config:
        env_prefix = "PATENT_"

settings = Settings()
