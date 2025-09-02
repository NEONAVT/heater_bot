"""
Пакет bot_config.

Содержит конфигурацию Telegram-бота, включая создание экземпляров bot и client.
"""

from bot_config.telegram_client import TelegramRawClient, telegram_client, CompanyBot
from bot_config.bot_instance import bot, dp


__all__ = ["TelegramRawClient", "CompanyBot", "telegram_client", "bot", "dp"]