import logging
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from keyboards import services_kb

logger = logging.getLogger(__name__)


class InstallationHandler:
    """
    Обрабатывает нажатие кнопки 'Монтаж оборудования' и отправляет
    информацию о предоставляемых услугах монтажа и систем отопления.
    """

    def __init__(self, router: Router) -> None:
        """
        Инициализация обработчика и регистрация хендлера сообщений.

        Args:
            router (Router): Aiogram Router для регистрации хендлеров.
        """
        self.router: Router = router
        self.register_handlers()

    def register_handlers(self) -> None:
        """
        Регистрирует хендлер на текстовое сообщение
        "⚙️ Монтаж оборудования".
        """
        self.router.message.register(
            self.services_callback, F.text == "⚙️ Монтаж оборудования"
        )

    async def services_callback(self, message: Message) -> None:
        """
        Отправляет пользователю информацию о монтажных услугах.

        Args:
            message (Message): Сообщение Telegram.
        """
        try:
            user_info = f"ID: {message.from_user.id}, "
            if message.from_user.username:
                user_info += f"Username: @{message.from_user.username}, "
            user_info += f"Name: {message.from_user.first_name}"
            if message.from_user.last_name:
                user_info += f" {message.from_user.last_name}"

            logger.info(f"Services callback received from user: {user_info}")

            await message.delete()

            text = (
                "*Монтаж оборудования:*\n\n"
                "Меняем, устанавливаем газовые котлы, колонки, "
                "бойлеры и другое газовое оборудование.\n"
                "_Гарантируем безопасную и надёжную работу оборудования._\n\n"
                "*Системы отопления:*\n"
                "Проектируем и монтируем системы отопления с нуля.\n"
                "_Эффективно, долговечно, с учётом всех норм._\n\n"
                "*Сантехника:*\n"
                "Устанавливаем и ремонтируем водоснабжение, "
                "трубы и сантехническое оборудование.\n"
                "_Работа без протечек и с долгим сроком службы._\n\n"
                "*Если хотите получить консультацию или точную оценку, "
                "нажмите кнопку «Хочу консультацию».*"
            )

            await message.answer(
                text, parse_mode=ParseMode.MARKDOWN, reply_markup=services_kb
            )
            logger.info(
                f"Services message successfully sent to user "
                f"{message.from_user.id}"
            )

        except Exception as e:
            logger.error(
                f"Unexpected error in services callback for user "
                f"{message.from_user.id}: {e}",
                exc_info=True
            )
            logger.debug(
                {
                    "user_id": message.from_user.id,
                    "chat_id": getattr(message.chat, "id", "unknown"),
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                }
            )
            await message.answer(
                "Произошла непредвиденная ошибка",
                show_alert=False)


router = Router()
InstallationHandler(router)
