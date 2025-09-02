import logging
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest
from keyboards import prices_kb

logger = logging.getLogger(__name__)


class PricesHandler:
    """
    Обрабатывает нажатие кнопки 'Стоимость' и отправляет информацию
    о стоимости услуг и порядке расчета.
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
        Регистрирует хендлер на текстовое сообщение "🧾 Стоимость".
        """
        self.router.message.register(self.prices, F.text == "🧾 Стоимость")

    async def prices(self, message: Message) -> None:
        """
        Отправляет пользователю информацию о стоимости услуг.

        Args:
            message (Message): Сообщение Telegram.
        """
        try:
            user_id = message.from_user.id
            username = message.from_user.username
            logger.info(f"User {user_id} ({username}) requested prices")
            await message.delete()

            text = (
                "💰 *Стоимость услуг*\n\n"
                "Мы занимаемся заменой и установкой "
                "газовых котлов, колонок, бойлеров, "
                "монтажом систем отопления и водоснабжения с нуля,"
                " а также ремонтом сантехники.\n\n"
                "Каждый проект уникален, поэтому "
                "стоимость рассчитывается индивидуально "
                "в зависимости от ваших потребностей и условий.\n\n"
                "Вы можете описать свою проблему или прислать фото "
                "— мы внимательно рассмотрим "
                "заявку и свяжемся с вами для точного расчета.\n\n"
                "*👇Для этого воспользуйтесь кнопкой "
                "'Отправить заявку на расчет' ниже.*\n"
                "Заполните форму обратной связи и отправьте файл"
            )

            await message.answer(
                text, parse_mode=ParseMode.MARKDOWN, reply_markup=prices_kb
            )
            logger.info(f"Prices message successfully sent to user {user_id}")

        except TelegramBadRequest as e:
            user_id = message.from_user.id
            if "message is not modified" in str(e):
                logger.debug(
                    f"Message not modified for user {user_id} - same content")
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
PricesHandler(router)
