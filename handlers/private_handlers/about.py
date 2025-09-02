import logging
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest
from keyboards import start_kb

logger = logging.getLogger(__name__)


class AboutHandler:
    """
    Обрабатывает нажатие кнопки 'О нас' и отправляет информацию о компании.
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
        Регистрирует хендлер на текстовое сообщение "👨‍🔧 О нас".
        """
        self.router.message.register(self.about, F.text == "👨‍🔧 О нас")

    async def about(self, message: Message) -> None:
        """
        Отправляет подробную информацию о компании пользователю.

        Args:
            message (Message): Сообщение Telegram.
        """
        try:
            user_id = message.from_user.id
            username = message.from_user.username
            logger.info(f"User {user_id} ({username}) requested info")
            await message.delete()

            text = (
                "*О нас*\n\n"
                "Мы специализируемся на инженерных системах, "
                "которые делают дом и бизнес комфортными и безопасными. "
                "С конца 90-х годов устанавливаем и меняем газовые котлы, "
                "колонки и бойлеры, проектируем и монтируем системы отопления "
                "и водоснабжения под ключ.\n\n"
                "Работаем как с частными клиентами, так и с организациями. "
                "Для одних это гарантия тёплого и надёжного дома, "
                "для других — бесперебойная работа объекта без простоя "
                "и лишних затрат.\n\n"
                "Наша команда не только монтирует новое оборудование, "
                "но и продлевает срок службы существующего: "
                "промываем системы отопления и водоснабжения, "
                "чистим бойлеры, устраняем засоры "
                "и повышаем эффективность работы.\n\n"
                "Опыт более 25 лет — это умение решать задачи "
                "разного масштаба: от квартиры и коттеджа до "
                "производственного помещения. Мы знаем, что от "
                "инженерных сетей зависит каждый день жизни, "
                "и поэтому делаем их максимально надёжными, "
                "экономичными и простыми в обслуживании."
            )

            await message.answer(
                text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=start_kb)
            logger.info(f"About message successfully sent to user {user_id}")

        except TelegramBadRequest as e:
            user_id = message.from_user.id
            if "message is not modified" in str(e):
                logger.debug(
                    f"Message not modified for user {user_id} - same content"
                )
                await message.answer()
            else:
                logger.error(f"TelegramBadRequest for user {user_id}: {e}")
                await message.answer(
                    "Произошла ошибка при обновлении сообщения",
                    show_alert=False
                )

        except Exception as e:
            user_id = message.from_user.id
            logger.error(
                f"Unexpected error for user {user_id}: {e}",
                exc_info=True
            )
            await message.answer(
                "Произошла непредвиденная ошибка",
                show_alert=False
            )


router = Router()
AboutHandler(router)
