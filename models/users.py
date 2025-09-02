from datetime import date
from typing import Optional

from sqlalchemy import Integer, String, Date, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class Users(Base):
    """
    Модель базы данных для хранения информации о пользователях Telegram.

    Атрибуты:
        user_id (int): Уникальный идентификатор пользователя.
        chat_id (int): Идентификатор чата Telegram, связанный с пользователем.
        username (str | None): Имя пользователя в Telegram.
        first_name (str | None): Имя пользователя.
        last_name (str | None): Фамилия пользователя.
        phone_number (str | None): Номер телефона пользователя.
        last_updated_date (date | None): Дата последнего обновления данных пользователя.
        status (str | None): Статус пользователя, по умолчанию "Guest".
    """

    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    username: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_updated_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[Optional[str]] = mapped_column(String, nullable=True, default="Guest")

    def __repr__(self):
        return f"<User(user_id={self.user_id}, chat_id={self.chat_id}, username='{self.username}')>"
