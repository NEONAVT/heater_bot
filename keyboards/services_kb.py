from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

services_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="💬 Хочу консультацию",
                web_app=WebAppInfo(
                    url="https://teplovodabot.github.io/bot_htmls/request-callback.html"
                )
            )
        ],
        [
            KeyboardButton(text="⚙️ Монтаж оборудования"),
            KeyboardButton(text="🔧 Ремонт оборудования"),
        ],
        [
            KeyboardButton(text="🧾 Стоимость"),
            KeyboardButton(text="👨‍🔧 О нас")
        ],
        [
            KeyboardButton(text="✅ Проекты")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)
