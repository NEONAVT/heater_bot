from sqlalchemy import Column, Integer, String, BigInteger, DateTime
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base


class Reminder(Base):
    """
    Модель базы данных для хранения информации о напоминаниях в Telegram.

    Атрибуты:
        id (int): Уникальный идентификатор напоминания.
        chat_id (int): Идентификатор чата, куда отправлено напоминание.
        message_id (int): Идентификатор сообщения Telegram.
        type (str): Тип напоминания ('callback' или 'problem').
        username (str): Имя пользователя Telegram, связанного с напоминанием.
        created_at (datetime): Дата и время создания записи.
    """

    __tablename__ = "reminders"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    message_id: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[str] = mapped_column(String(10), nullable=False)
    username: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now())