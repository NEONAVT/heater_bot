"""
Пакет database.

Обеспечивает подключение к базе данных и управление сессиями.
Содержит базовый класс для моделей SQLAlchemy.
"""


from database.accessor import AsyncSessionFactory, sync_engine

__all__ = ["AsyncSessionFactory", "sync_engine"]