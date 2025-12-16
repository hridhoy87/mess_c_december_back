from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ENV: str = "dev"
    DATABASE_URL: str

    JWT_SECRET: str
    JWT_EXPIRES_MINUTES: int = 60 * 24 * 7

    JWT_COOKIE_NAME: str = "messc_session"
    JWT_COOKIE_SECURE: bool = False  # True in production behind HTTPS

settings = Settings()