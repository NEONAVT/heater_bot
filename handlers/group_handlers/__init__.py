"""
Пакет group_handlers.

Обрабатывает сообщения в групповых чатах.
Включает обработку экспорта данных, напоминаний и стартовых команд для групп.
"""


from handlers.group_handlers.start_handler import router as group_start_handler
from handlers.group_handlers.remind_handler import router as remind_router
from handlers.group_handlers.db_export import router as db_export_users_router

group_routers = [group_start_handler, db_export_users_router, remind_router]
