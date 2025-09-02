"""
Пакет filters.

Содержит кастомные фильтры для обработки сообщений и команд в боте.
"""


from filters.filters import ChatTypeFilter, ChatAdminFilter

__all__ = ["ChatTypeFilter", "ChatAdminFilter"]