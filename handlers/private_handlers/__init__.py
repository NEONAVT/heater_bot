"""
Пакет private_handlers.

Обрабатывает сообщения в приватных чатах пользователя.
Содержит обработчики стартовых команд, сервисов, проектов, ремонта и web_app форм.
"""


from handlers.private_handlers.prices_handler import router as prices_router
from handlers.private_handlers.start_hendler import router as start_router
from handlers.private_handlers.about import router as about_router
from handlers.private_handlers.web_app_data_handler import router as web_app_data_router
from handlers.private_handlers.installation_handler import router as services_router
from handlers.private_handlers.projects_handler import router as projects_router
from handlers.private_handlers.repair_handler import router as repair_router

private_routers = [
    start_router,
    about_router,
    prices_router,
    web_app_data_router,
    services_router,
    projects_router,
    repair_router
]
