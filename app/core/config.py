from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "tracker"
    SQLALCHEMY_DATABASE_URI: str = f'postgresql+psycopg2://{os.environ.get("POSTGRES_USER", "postgres")}:{os.environ.get("POSTGRES_PASSWORD", "")}@{os.environ.get("POSTGRES_SERVER", "127.0.0.1")}:5432/{os.environ.get("POSTGRES_DB", "tracker")}'
    SQLALCHEMY_TEST_DATABASE_URI: str = f'postgresql+psycopg2://{os.environ.get("POSTGRES_USER", "postgres")}:{os.environ.get("POSTGRES_PASSWORD", "")}@{os.environ.get("POSTGRES_SERVER", "127.0.0.1")}:5432/{os.environ.get("POSTGRES_TEST_DB", "tracker_test")}'
    REDIS_HOST: str = os.environ.get("REDIS_HOST", 'localhost')
    REDIS_PORT: int = os.environ.get("REDIS_PORT", 6379)
    WEATHER_PROVIDER_BASE_API: str = os.environ.get("WEATHER_PROVIDER_BASE_API", "")
    WEATHER_PROVIDER_API_KEY: str = os.environ.get("WEATHER_PROVIDER_API_KEY", "")
    WEATHER_UPDATE_INTERVAL_IN_SECONDS: int = os.environ.get("WEATHER_UPDATE_INTERVAL_IN_SECONDS", 7200)
    POPULATE_DATABASE: int = os.environ.get("POPULATE_DATABASE", 0)


settings = Settings()
