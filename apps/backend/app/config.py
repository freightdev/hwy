from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://hwy:hwy@db:5432/hwytms"
    cors_origin: str = "http://localhost:5173,https://hwytms.com,https://app.hwytms.com"
    codriver_runtime_url: str = "http://codriver:8010"
    debug: bool = True

    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    class Config:
        env_file = "configs/env/hwy.dev.env"
        extra = "ignore"


settings = Settings()
