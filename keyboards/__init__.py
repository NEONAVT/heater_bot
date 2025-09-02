"""
Пакет keyboards.

Содержит наборы клавиатур для различных разделов бота:
стартовые клавиатуры, сервисы, проекты, стоимость, напоминания и т.д.
"""


from keyboards.start_kb import start_kb
from keyboards.services_kb import services_kb
from keyboards.prices_kb import prices_kb
from keyboards.projects_kb import projects_kb
from keyboards.remind_kb import remind_kb
from keyboards.start_group_kb import start_group_kb
__all__ = ["start_kb", "services_kb", "prices_kb", "remind_kb"]