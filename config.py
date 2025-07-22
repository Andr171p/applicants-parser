from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class GigaChatSettings(BaseSettings):
    api_key: str = ""
    scope: str = ""

    model_config = SettingsConfigDict(env_prefix="GIGACHAT_")


class SqlSettings(BaseSettings):
    postgres_host: str = ""
    postgres_port: int = 5432
    postgres_password: str = ""
    postgres_user: str = ""
    postgres_db: str = ""

    @property
    def get_db_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


class RabbitSettings(BaseSettings):
    rabbit_host: str = ""
    rabbit_port: int = 5672

    @property
    def get_rabbit_url(self) -> str:
        return f"amqp://guest:guest@{self.rabbit_host}:{self.rabbit_port}/"


class Settings(BaseSettings):
    gigachat: GigaChatSettings = GigaChatSettings()
    sql_settings: SqlSettings = SqlSettings()
    rabbit_settings: RabbitSettings = RabbitSettings()


settings = Settings()
