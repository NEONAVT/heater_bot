import logging
from aiogram import types, Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest
from keyboards import services_kb

# Настройка логирования для этого модуля
logger = logging.getLogger(__name__)

router = Router()


@router.message(F.text == "🔧 Услуги")
async def services_callback(message: Message):
    try:
        # Логируем информацию о пользователе
        user_info = f"ID: {message.from_user.id}, "
        if message.from_user.username:
            user_info += f"Username: @{message.from_user.username}, "
        user_info += f"Name: {message.from_user.first_name}"
        if message.from_user.last_name:
            user_info += f" {message.from_user.last_name}"

        logger.info(f"Services callback received from user: {user_info}")

        await message.delete()

        await message.answer(
            "*Услуги:*\n"
            "*Ремонт и установка котлов, газового оборудования:*\n"
            "Меняем, устанавливаем и ремонтируем газовые котлы, колонки, бойлеры и другое газовое оборудование. "
            "_Гарантируем безопасную и надёжную работу оборудования._\n\n"
            "*Системы отопления:*\n"
            "Проектируем и монтируем системы отопления с нуля. "
            "_Эффективно, долговечно, с учётом всех норм._\n\n"
            "*Сантехника:*\n"
            "Устанавливаем и ремонтируем водоснабжение, трубы и сантехническое оборудование. "
            "_Работа без протечек и с долгим сроком службы._\n\n"
            "*Если хотите получить консультацию или точную оценку, нажмите кнопку «Хочу консультацию».*",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=services_kb
        )

        logger.info(f"Services message successfully updated for user {message.from_user.id}")

    except Exception as e:
        # Логируем другие ошибки с полной информацией
        logger.error(
            f"Unexpected error in services callback for user {message.from_user.id}: {e}",
            exc_info=True
        )

        # Дополнительная информация об ошибке
        error_context = {
            'user_id': message.from_user.id,
            'chat_id': message.message.chat.id if message.message else 'unknown',
            'error_type': type(e).__name__,
            'error_message': str(e)
        }
        logger.debug(f"Error context: {error_context}")

        await message.answer("Произошла непредвиденная ошибка", show_alert=False)