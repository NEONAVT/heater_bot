import logging
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from keyboards import services_kb

logger = logging.getLogger(__name__)


class RepairHandler:
    """
    Обрабатывает нажатие кнопки 'Ремонт оборудования' и отправляет
    информацию о ремонте и обслуживании газового оборудования.
    """

    def __init__(self, router: Router) -> None:
        self.router: Router = router
        self.register_handlers()

    def register_handlers(self) -> None:
        self.router.message.register(
            self.services_callback, F.text == "🔧 Ремонт оборудования"
        )

    async def services_callback(self, message: Message) -> None:
        """
        Отправляет пользователю информацию о сервисе оборудования.

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
                "*Ремонт и обслуживание оборудования:*\n\n"
                "Мы выполняем полный спектр работ по ремонту и техническому "
                "обслуживанию газовых котлов, колонок "
                "и другого оборудования:\n"
                "- Ежегодное плановое техническое обслуживание "
                "для безопасной и надежной работы.\n"
                "- Диагностика неисправностей и оперативный ремонт всех видов "
                "оборудования.\n"
                "- Настройка котлов при первом пуске для эффективной работы.\n"
                "- Консультации и помощь в подборе котла на замену по вашим "
                "потребностям.\n"
                "- Сопровождение при покупке оборудования "
                "и установка при необходимости.\n\n"
                "*Наши сервисные мастера всегда готовы помочь:*\n"
                "Андрей: +7 000 000 00 00\n"
                "Павел: +7 000 000 00 00\n\n"
                "_Обеспечиваем долгую и безопасную работу оборудования, "
                "избавляя вас от неожиданных поломок._"
            )

            await message.answer(
                text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=services_kb,
            )

            logger.info(
                f"Repair message successfully sent to user "
                f"{message.from_user.id}"
            )

        except Exception as e:
            logger.error(
                f"Unexpected error in services callback for user "
                f"{message.from_user.id}: {e}",
                exc_info=True
            )
            logger.debug({
                "user_id": message.from_user.id,
                "chat_id": getattr(message.chat, "id", "unknown"),
                "error_type": type(e).__name__,
                "error_message": str(e),
            })

            await message.answer(
                "Произошла непредвиденная ошибка", show_alert=False
            )


router = Router()
RepairHandler(router)
