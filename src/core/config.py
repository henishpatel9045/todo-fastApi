from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str
    JWT_TOKEN_EXPIRE_SECONDS: int = 90 * 24 * 60 * 60  # 90 DAYS
    JWT_ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=r".././.env"
    )


settings = Settings()
