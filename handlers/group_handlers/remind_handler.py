import asyncio
import logging
from typing import Optional

from aiogram import Router, types
from filters import ChatTypeFilter
from bot_config import bot
from services import reminders_service

logger = logging.getLogger(__name__)

router = Router()


@router.message(ChatTypeFilter(["group", "supergroup"]))
async def remind_keyboard_handler(message: types.Message):
    """
    Обрабатывает сообщения с указанием времени в минутах и создаёт
    отложенное напоминание.

    Args:
        message (types.Message): Сообщение Telegram.
    """
    if message.text.endswith("минут") or message.text.endswith("минуты"):
        try:
            minutes: int = int("".join(filter(str.isdigit, message.text)))
        except ValueError:
            return

        delay: int = minutes * 60
        msg: types.Message = await message.answer("Напоминание установлено")

        record = await (reminders_service.
                        get_last_reminder_by_chat(message.chat.id))
        if not record:
            return

        asyncio.create_task(
            remind_user_later(
                chat_id=message.chat.id,
                message_id=record.message_id,
                delay=delay,
                user=message.from_user.username,
                msg_del=msg,
                message=message,
            )
        )


async def remind_user_later(
    chat_id: int,
    message_id: int,
    delay: int,
    user: Optional[str],
    msg_del: types.Message,
    message: types.Message,
) -> None:
    """
    Отправляет напоминание пользователю через указанное время.

    Args:
        chat_id (int): ID чата Telegram.
        message_id (int): ID исходного сообщения.
        delay (int): Задержка в секундах.
        user (Optional[str]): Имя пользователя Telegram.
        msg_del (types.Message): Сообщение с подтверждением установки
            напоминания, которое нужно удалить.
        message (types.Message): Исходное сообщение, которое нужно удалить.
    """
    await asyncio.sleep(delay)
    await message.delete()
    await msg_del.delete()
    await bot.send_message(
        chat_id=chat_id,
        text=(
            f"⏰@{user or message.from_user.first_name}, напоминаю "
            "об отложенном обращении клиента!"
        ),
        reply_to_message_id=message_id,
    )
    await reminders_service.delete_reminder(message_id)
