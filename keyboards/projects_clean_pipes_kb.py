from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

projects_clean_pipes_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Загрязнения труб", callback_data="dirty_pipes")

        ],
        [
            InlineKeyboardButton(text="Принято в работу", callback_data="accepted"),
            InlineKeyboardButton(text="Отклонено", callback_data="declined")
        ]
    ]
)
