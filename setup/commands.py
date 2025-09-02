from aiogram.types import BotCommand, BotCommandScopeChat
from bot_config import bot
from settings import settings


async def register_commands():
    """
    Регистрирует команды бота в указанном чате Telegram.

    Использует scope BotCommandScopeChat для ограничения команды определенным чатам.
    """
    await bot.set_my_commands(
        commands=[
            BotCommand(command="start_group", description="Запуск")
        ],
        scope=BotCommandScopeChat(chat_id=settings.ADMIN_CHAT_ID)
    )
