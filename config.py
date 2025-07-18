from dotenv import dotenv_values, find_dotenv

env_path = find_dotenv()


def load_config() -> dict:
    env_path = find_dotenv(".env")

    if not env_path:
        env_path = find_dotenv(".test.env")

    return dotenv_values(env_path)


config = load_config()


class Settings:
    POSTGRES_HOST: str = config["POSTGRES_HOST"]
    POSTGRES_PORT: str = config["POSTGRES_PORT"]
    POSTGRES_PASSWORD: str = config["POSTGRES_PASSWORD"]
    POSTGRES_USER: str = config["POSTGRES_USER"]
    POSTGRES_DB: str = config["POSTGRES_DB"]


settings = Settings()


def get_db_url() -> str:
    return f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
