import logging
from aiogram import Router, types
from aiogram.filters import Command
from filters import ChatTypeFilter, ChatAdminFilter
from services import send_users_excel, users_service
from services.excel_export import (
    send_guest_users_excel,
    send_client_users_excel,
    send_inactive_client_list,
)
from database.accessor import sync_engine

logger = logging.getLogger(__name__)

router = Router()


@router.message(
    Command("all_users"),
    ChatTypeFilter(allowed=["group", "supergroup"]),
    ChatAdminFilter(),
)
async def db_export_users(message: types.Message) -> None:
    """
    Экспорт всех пользователей в Excel и отправка файла в чат.

    Args:
        message (types.Message): Сообщение Telegram.
    """
    logger.info(
        f"Команда /all_users получена от пользователя {message.from_user.id}"
    )
    logger.info(f"Тип чата: {message.chat.type}")

    if message.chat.type in ["group", "supergroup"]:
        try:
            member = await message.chat.get_member(message.from_user.id)
            is_admin: bool = member.status in ["administrator", "creator"]
            logger.info(
                f"Пользователь является админом или владельцем: {is_admin}"
            )
        except Exception as e:
            logger.error(f"Ошибка при проверке прав: {e}")

    await send_users_excel(message=message, db_engine=sync_engine)


@router.message(
    Command("guests"),
    ChatTypeFilter(allowed=["group", "supergroup"]),
    ChatAdminFilter(),
)
async def db_guests_export_users(message: types.Message) -> None:
    """
    Экспорт гостей в Excel и отправка файла в чат.

    Args:
        message (types.Message): Сообщение Telegram.
    """
    logger.info(
        f"Команда /guests получена от пользователя {message.from_user.id}"
    )
    logger.info(f"Тип чата: {message.chat.type}")

    if message.chat.type in ["group", "supergroup"]:
        try:
            member = await message.chat.get_member(message.from_user.id)
            is_admin: bool = member.status in ["administrator", "creator"]
            logger.info(
                f"Пользователь является админом или владельцем: {is_admin}"
            )
        except Exception as e:
            logger.error(f"Ошибка при проверке прав: {e}")

    await send_guest_users_excel(message=message, db_engine=sync_engine)


@router.message(
    Command("clients"),
    ChatTypeFilter(allowed=["group", "supergroup"]),
    ChatAdminFilter(),
)
async def db_clients_export_users(message: types.Message) -> None:
    """
    Экспорт клиентов в Excel и отправка файла в чат.

    Args:
        message (types.Message): Сообщение Telegram.
    """
    logger.info(
        f"Команда /clients получена от пользователя {message.from_user.id}"
    )
    logger.info(f"Тип чата: {message.chat.type}")

    if message.chat.type in ["group", "supergroup"]:
        try:
            member = await message.chat.get_member(message.from_user.id)
            is_admin: bool = member.status in ["administrator", "creator"]
            logger.info(
                f"Пользователь является админом или владельцем: {is_admin}"
            )
        except Exception as e:
            logger.error(f"Ошибка при проверке прав: {e}")

    await send_client_users_excel(message=message, db_engine=sync_engine)


@router.message(
    Command("inactive"),
    ChatTypeFilter(allowed=["group", "supergroup"]),
    ChatAdminFilter(),
)
async def get_inactive_client_list(message: types.Message) -> None:
    """
    Отправляет список неактивных клиентов за последние 7 дней и
    Excel-файл с ними.

    Args:
        message (types.Message): Сообщение Telegram.
    """
    logger.info(
        f"Команда /inactive получена от пользователя {message.from_user.id}"
    )
    logger.info(f"Тип чата: {message.chat.type}")

    if message.chat.type in ["group", "supergroup"]:
        try:
            member = await message.chat.get_member(message.from_user.id)
            is_admin: bool = member.status in ["administrator", "creator"]
            logger.info(
                f"Пользователь является админом или владельцем: {is_admin}"
            )
        except Exception as e:
            logger.error(f"Ошибка при проверке прав: {e}")

        clients = await users_service.get_inactive_clients()
        if not clients:
            await message.answer("Клиентов нет")
            return

        text = (
            "Клиенты, которые воспользовались функцией обратной связи "
            "7 дней назад:\n\n"
        )
        for u in clients:
            phone = u.phone_number or "Номера нет"
            text += (
                f"Имя пользователя: @{u.username} — Имя: {u.first_name} — "
                f"Номер: {phone},  последняя дата обращения: "
                f"{u.last_updated_date:%Y-%m-%d}\n\n"
            )

        await message.answer(text)
        await send_inactive_client_list(message=message, db_engine=sync_engine)
