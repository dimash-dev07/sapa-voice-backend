from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "voice-request-api"
    debug: bool = False
    database_url: str = "postgresql+asyncpg://sapa:sapa@localhost:5432/voicedb"
    redis_url: str = "redis://localhost:6379/0"
    queue_name: str = "voice_requests"
    worker_poll_timeout: int = 5

    jwt_secret: str = "change-me-in-prod"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60


settings = Settings()