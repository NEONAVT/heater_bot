import logging

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from services import (
    send_users_excel,
    send_guest_users_excel,
    send_client_users_excel,
    send_inactive_client_list,
    users_service,
)
from handlers.group_handlers.db_export import get_inactive_client_list
from filters import ChatTypeFilter
from keyboards import start_group_kb
from database.accessor import sync_engine

logger = logging.getLogger(__name__)

router = Router()


@router.message(
    Command("start_group"),
    ChatTypeFilter(allowed=["group", "supergroup"]),
)
async def start_group(message: types.Message) -> None:
    """
    Приветственное сообщение для группового чата и описание возможностей бота.

    Args:
        message (types.Message): Сообщение Telegram.
    """
    print(message.chat.id)
    await message.answer(
        text=(
            "Привет. Этот чат получает уведомления о новых заказах, "
            "обратных звонках и заявках.\n"
            "Здесь можно:\n"
            "- Смотреть и выгружать клиентов по статусу или условиям\n"
            "- Получать уведомления о новых заявках и заказах\n"
            "- Работать с базой данных клиентов через команды бота\n\n"
            "Доступные команды:\n"
        ),
        reply_markup=start_group_kb,
    )


@router.callback_query(F.data == "all_users")
async def get_all_users(callback: CallbackQuery) -> None:
    """
    Выгрузка всех пользователей в Excel через callback.

    Args:
        callback (CallbackQuery): Callback от Telegram.
    """
    await send_users_excel(callback.message, db_engine=sync_engine)


@router.callback_query(F.data == "all_clients")
async def get_all_clients(callback: CallbackQuery) -> None:
    """
    Выгрузка всех клиентов в Excel через callback.

    Args:
        callback (CallbackQuery): Callback от Telegram.
    """
    await send_client_users_excel(callback.message, db_engine=sync_engine)


@router.callback_query(F.data == "all_guests")
async def get_all_guests(callback: CallbackQuery) -> None:
    """
    Выгрузка всех гостей в Excel через callback.

    Args:
        callback (CallbackQuery): Callback от Telegram.
    """
    await send_guest_users_excel(callback.message, db_engine=sync_engine)


@router.callback_query(F.data == "inactive_clients")
async def get_all_inactive(callback: CallbackQuery) -> None:
    """
    Выгрузка неактивных клиентов через callback.

    Args:
        callback (CallbackQuery): Callback от Telegram.
    """
    await get_inactive_client_list(callback.message)
