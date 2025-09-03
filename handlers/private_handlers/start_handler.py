import logging
from aiogram import Router, types
from aiogram.filters import CommandStart
from services import users_service
from keyboards import start_kb

logger = logging.getLogger(__name__)


class StartHandler:
    """
    Обрабатывает команду /start и отправляет приветственное сообщение
    пользователю, а также регистрирует его в базе данных.
    """

    def __init__(self, router: Router) -> None:
        self.router: Router = router
        self.register_handlers()

    def register_handlers(self) -> None:
        self.router.message.register(self.start, CommandStart())

    @staticmethod
    async def start(message: types.Message) -> None:
        try:
            user_info = f"ID: {message.from_user.id}, "
            if message.from_user.username:
                user_info += f"Username: @{message.from_user.username}, "
            user_info += f"Name: {message.from_user.first_name}"
            if message.from_user.last_name:
                user_info += f" {message.from_user.last_name}"

            logger.info(f"Start command received from user: {user_info}")
            logger.info(
                f"Chat ID: {message.chat.id}, "
                f"Chat type: {message.chat.type}")

            user = await users_service.register_user(
                user_id=message.from_user.id,
                chat_id=message.chat.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name
            )

            text = (
                f"👋Добрый день, {user.first_name or user.username}!\n\n"
                f"Мы помогаем с заменой и установкой "
                f"газовых котлов, колонок, бойлеров, "
                f"а также с монтажом систем отопления "
                f"и водоснабжения с нуля.\n\n"
                f"📞Звонки принимаются с 8:00 до 10:00.\n"
                f"В остальное время мы занимаемся выполнением заказов, "
                f"чтобы всё было сделано качественно и в срок.\n\n"
                f"Вы можете быстро узнать о наших услугах "
                f"или заказать обратный звонок — "
                f"с вами свяжутся в ближайшее время.\n\n"
                f"⬇️Для получения информации воспользуйтесь кнопками ниже."
            )

            await message.answer(text=text, reply_markup=start_kb)
            logger.info(
                f"Start message successfully sent to user "
                f"{message.from_user.id}")

        except Exception as e:
            logger.error(
                f"Error sending start message to user "
                f"{message.from_user.id}: {e}",
                exc_info=True
            )
            logger.debug({
                "user_id": message.from_user.id,
                "chat_id": message.chat.id,
                "error_type": type(e).__name__,
                "error_message": str(e),
            })

            try:
                await message.answer(
                    "⚠️ Произошла ошибка при обработке запроса. "
                    "Попробуйте позже."
                )
            except Exception as inner_e:
                logger.error(
                    f"Failed to send error message to user: {inner_e}")


router = Router()
StartHandler(router)
