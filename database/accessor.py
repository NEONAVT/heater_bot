from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from settings import settings

# Синхронный движок SQLAlchemy
sync_engine: create_engine = create_engine(settings.sync_db_url)

# Асинхронный движок SQLAlchemy
engine = create_async_engine(
    settings.async_db_url,
    future=True,
    echo=True,
    pool_pre_ping=True,
)

# Фабрика асинхронных сессий
AsyncSessionFactory: sessionmaker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)
