from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_group_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text="Выгрузить всех пользователей",
            callback_data="all_users")],
        [InlineKeyboardButton(
            text="Выгрузить всех клиентов",
            callback_data="all_clients")],
        [InlineKeyboardButton(
            text="Выгрузить всех гостей",
            callback_data="all_guests")],
        [InlineKeyboardButton(
            text="Клиенты: Обратная связь 7 дней",
            callback_data="inactive_clients")],
    ]
)
