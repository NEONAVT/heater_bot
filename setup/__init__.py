"""
Пакет setup.

Содержит функции для инициализации бота:
регистрацию команд (commands.py) и подключение роутеров (routers.py).
"""


from setup.routers import register_routers
from setup.commands import register_commands

__all__ = ["register_commands", "register_routers"]