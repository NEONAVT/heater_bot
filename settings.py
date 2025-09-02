import os
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    admin_chat_id: str
    base_dir: Path = os.path.dirname(os.path.dirname(__file__))

    ADMIN_CHAT_ID: int

    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_DRIVER: str = "postgresql+asyncpg"
    DB_SYNC_DRIVER: str = "postgresql + psycopg2"

    APP_NAME: str = "neonavt_tg_bot"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

    @property
    def async_db_url(self) -> str:
        return (f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASS}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

    @property
    def sync_db_url(self) -> str:
        return f"{self.DB_SYNC_DRIVER}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    def send_msg_url(self, text: str) -> str:
        return (f"https://api.telegram.org/bot{self.bot_token}/"
                f"sendMessage?chat_id={self.admin_chat_id}&text={text}")

    class Config:
        env_file = ".env"


settings = Settings()
