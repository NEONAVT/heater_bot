from datetime import datetime
from typing import Any, Dict, Optional

import aiohttp
from aiogram import Bot
from settings import settings


class TelegramRawClient:
    """
    Асинхронный клиент для работы с Telegram Bot API через HTTP-запросы.

    Attributes:
        token (str): Токен бота Telegram.
        base_url (str): Базовый URL API Telegram.
        session (Optional[aiohttp.ClientSession]): HTTP-сессия для запросов.
    """

    def __init__(
        self, token: str, base_url: str = "https://api.telegram.org"
    ) -> None:
        """
        Инициализация TelegramRawClient.

        Args:
            token (str): Токен бота Telegram.
            base_url (str, optional): Базовый URL API. По умолчанию
                "https://api.telegram.org".
        """
        self.token: str = token
        self.base_url: str = base_url.rstrip("/")
        self.session: Optional[aiohttp.ClientSession] = None

    async def ensure_session(self) -> aiohttp.ClientSession:
        """
        Создает HTTP-сессию, если она отсутствует или закрыта.

        Returns:
            aiohttp.ClientSession: Активная сессия для запросов.
        """
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

    async def prepare_url(self, method: Optional[str]) -> str:
        """
        Формирует полный URL для запроса к Telegram API.

        Args:
            method (Optional[str]): Метод API Telegram.

        Returns:
            str: Полный URL для запроса.
        """
        result_url = f"{self.base_url}/bot{self.token}/"
        if method is not None:
            result_url += method
        return result_url

    async def post(self, method: str, **payload: Any) -> Dict[str, Any]:
        """
        Выполняет POST-запрос к Telegram API.

        Args:
            method (str): Метод API Telegram.
            **payload (Any): JSON-данные для запроса.

        Returns:
            Dict[str, Any]: Ответ от Telegram API. В случае ошибки
            {"ok": False, "error": str}.
        """
        url = await self.prepare_url(method)
        session = await self.ensure_session()
        try:
            async with session.post(url, json=payload) as resp:
                return await resp.json()
        except Exception as e:
            print(
                f"Error calling Telegram API: {e}"
            )
            return {"ok": False, "error": str(e)}

    def create_err_message(self, err: Exception) -> str:
        """
        Формирует строку ошибки с текущим временем и типом исключения.

        Args:
            err (Exception): Исключение.

        Returns:
            str: Строка ошибки.
        """
        return f"{datetime.now()} :: {err.__class__} :: {err}"

    async def close(self) -> None:
        """
        Закрывает HTTP-сессию.
        """
        if self.session and not self.session.closed:
            await self.session.close()


class CompanyBot(Bot):
    """
    Обертка над aiogram.Bot с возможностью прямого обращения
    к Telegram API через TelegramRawClient.
    """

    def __init__(
        self,
        token: str,
        telegram_client: Optional[TelegramRawClient] = None,
        **kwargs: Any
    ) -> None:
        """
        Инициализация CompanyBot.

        Args:
            token (str): Токен Telegram бота.
            telegram_client (Optional[TelegramRawClient]): Существующий
                raw-клиент. Если None, создается новый.
            **kwargs (Any): Дополнительные аргументы для aiogram.Bot.
        """
        super().__init__(token=token, **kwargs)
        self.raw_client: TelegramRawClient = (
            telegram_client or TelegramRawClient(token=token)
        )

    async def raw_call(self, method: str, **payload: Any) -> Dict[str, Any]:
        """
        Выполняет вызов метода Telegram API через raw-клиент.

        Args:
            method (str): Метод API Telegram.
            **payload (Any): JSON-данные для запроса.

        Returns:
            Dict[str, Any]: Ответ от Telegram API.
        """
        return await self.raw_client.post(method, **payload)

    async def close(self) -> None:
        """
        Закрывает бота и raw-клиент.
        """
        await super().close()
        await self.raw_client.close()


telegram_client: TelegramRawClient = TelegramRawClient(
    token=settings.bot_token
)
