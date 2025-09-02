from bot_config import dp
from handlers.private_handlers import private_routers
from handlers.group_handlers import group_routers
import logging

logger = logging.getLogger(__name__)

def register_routers():
    """
    Подключает все приватные и групповые роутеры к Dispatcher.

    Логирует подключение каждого роутера.
    """
    for router in private_routers:
        dp.include_router(router)
        logger.info(f"Подключён приватный роутер: {router.name}")
    for router in group_routers:
        dp.include_router(router)
        logger.info(f"Подключён групповой роутер: {router.name}")
