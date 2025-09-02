import logging
from aiogram.filters import Command
from aiogram import Router, F
from filters import ChatTypeFilter
from aiogram import types

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("c"), ChatTypeFilter(allowed=["group", "supergroup"]))
async def commands(message: types.Message):
    commands_text = (
        "/c — Список команд\n"
        "/start_group — Запуск\n"
        "/all_user — Выгрузить всех пользователей из базы\n"
        "/guests — Выгрузить всех посетителей из базы\n"
        "/clients — Выгрузить всех клиентов из базы\n"
        "/inactive — Выгрузить неактивных клиентов"
    )
    await message.answer(commands_text)
