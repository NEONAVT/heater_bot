import pandas as pd
from io import BytesIO
from aiogram import types
from aiogram.types import BufferedInputFile


async def send_users_excel(message: types.Message, db_engine):
    """
    Отправляет пользователю Excel-файл со всеми пользователями базы данных.

    Args:
        message (types.Message): Сообщение Telegram для ответа.
        db_engine: SQLAlchemy engine для чтения из базы.
    """
    df = pd.read_sql("SELECT * FROM users", db_engine)
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)

    await message.answer("Таблица всех пользователей из базы данных:")
    await message.answer_document(
        BufferedInputFile(output.getvalue(), filename="all_users.xlsx")
    )


async def send_guest_users_excel(message: types.Message, db_engine):
    """
    Отправляет Excel-файл с пользователями, имеющими статус 'Guest'.

    Args:
        message (types.Message): Сообщение Telegram.
        db_engine: SQLAlchemy engine для чтения из базы.
    """
    df = pd.read_sql("SELECT * FROM users WHERE status = 'Guest'", db_engine)
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)

    await message.answer("Таблица клиентов с статусом Guest:")
    await message.answer_document(
        BufferedInputFile(output.getvalue(), filename="guests.xlsx")
    )


async def send_client_users_excel(message: types.Message, db_engine):
    """
    Отправляет Excel-файл с пользователями, имеющими статус 'Client'.

    Args:
        message (types.Message): Сообщение Telegram.
        db_engine: SQLAlchemy engine для чтения из базы.
    """
    df = pd.read_sql("SELECT * FROM users WHERE status = 'Client'", db_engine)
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)

    await message.answer("Таблица клиентов с статусом Client:")
    await message.answer_document(
        BufferedInputFile(output.getvalue(), filename="clients.xlsx")
    )


async def send_inactive_client_list(message: types.Message, db_engine):
    """
    Отправляет Excel-файл с клиентами, которые не обновляли данные более 7 дней.

    Args:
        message (types.Message): Сообщение Telegram.
        db_engine: SQLAlchemy engine для чтения из базы.
    """
    df = pd.read_sql(
        "SELECT * FROM users WHERE status = 'Client' AND last_updated_date < NOW() - interval '7 days'",
        db_engine
    )
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)

    await message.answer_document(
        BufferedInputFile(output.getvalue(), filename="inactive.xlsx")
    )
