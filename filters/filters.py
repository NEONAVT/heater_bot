from typing import List
from aiogram import types
from aiogram.filters import BaseFilter


class ChatTypeFilter(BaseFilter):
    """
    Фильтр сообщений по типу чата.
    """

    def __init__(self, allowed: List[str]) -> None:
        """
        Инициализация фильтра.

        Args:
            allowed (List[str]): Список разрешенных типов чатов.
        """
        self.allowed: List[str] = allowed

    async def __call__(self, message: types.Message) -> bool:
        """
        Проверка типа чата сообщения.

        Args:
            message (types.Message): Сообщение Telegram.

        Returns:
            bool: True, если тип чата разрешен, иначе False.
        """
        return message.chat.type in self.allowed


class ChatAdminFilter(BaseFilter):
    """
    Фильтр сообщений по правам администратора.
    """

    def __init__(self, require_admin: bool = True) -> None:
        """
        Инициализация фильтра.

        Args:
            require_admin (bool): Если True, проверяется наличие
                прав администратора.
        """
        self.require_admin: bool = require_admin

    async def __call__(self, message: types.Message) -> bool:
        """
        Проверка, является ли пользователь администратором.

        Args:
            message (types.Message): Сообщение Telegram.

        Returns:
            bool: True, если пользователь админ (или проверка не
            требуется), иначе False.
        """
        if message.chat.type not in ["group", "supergroup"]:
            return False

        member = await message.chat.get_member(message.from_user.id)
        is_admin: bool = member.status in ("administrator", "creator")
        return is_admin if self.require_admin else True
