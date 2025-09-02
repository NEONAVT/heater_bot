from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

task_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Я перезвоню", callback_data="take_call")

        ],
        [
            InlineKeyboardButton(text="Принято в работу", callback_data="accepted"),
            InlineKeyboardButton(text="Отклонено", callback_data="declined")
        ]
    ]
)
