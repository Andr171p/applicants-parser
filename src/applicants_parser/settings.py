from pathlib import Path
from dotenv import load_dotenv

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)


class GigaChatSettings(BaseSettings):
    api_key: str = ""
    scope: str = ""

    model_config = SettingsConfigDict(env_prefix="GIGACHAT_")


class Settings(BaseSettings):
    gigachat: GigaChatSettings = GigaChatSettings()


settings = Settings()
