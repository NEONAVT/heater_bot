from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Базовый класс для всех моделей SQLAlchemy.
    Наследует DeclarativeBase, чтобы создавать ORM-модели.
    """
    pass
