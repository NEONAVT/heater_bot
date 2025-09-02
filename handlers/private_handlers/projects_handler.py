import logging
from pathlib import Path
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, InputMediaPhoto, FSInputFile
from bot_config import bot
from handlers.private_handlers.start_hendler import StartHandler
from keyboards import projects_kb

logger = logging.getLogger(__name__)


class ProjectsHandlers:
    """
    Обрабатывает нажатие кнопок с проектами и отправляет
    пользователю информацию и изображения по выбранной категории.
    """

    def __init__(self, router: Router) -> None:
        self.router: Router = router
        self.BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
        self.register_handlers()

    def register_handlers(self) -> None:
        self.router.message.register(
            self.projects_callback,
            F.text == "✅ Проекты")
        self.router.message.register(
            self.pipes_cleaning_callback,
            F.text == "Сервис котлов и труб"
        )
        self.router.message.register(
            self.warm_floor_callback,
            F.text == "Монтаж тёплого пола"
        )
        self.router.message.register(
            self.pipes_routing_callback,
            F.text == "Водопроводная разводка"
        )
        self.router.message.register(
            self.heater_installation_callback,
            F.text == "Установка котлов и бойлеров"
        )
        self.router.message.register(
            self.main_callback,
            F.text == "В начало")

    async def projects_callback(self, message: Message) -> None:
        try:
            user_info = f"ID: {message.from_user.id}, "
            if message.from_user.username:
                user_info += f"Username: @{message.from_user.username}, "
            user_info += f"Name: {message.from_user.first_name}"
            if message.from_user.last_name:
                user_info += f" {message.from_user.last_name}"
            logger.info(f"Projects callback received from user: {user_info}")

            await message.delete()
            await message.answer(
                (
                    "*Вы можете ознакомиться с нашими проектами ниже, "
                    "нажимая кнопки.*\n\n"
                    "Если у вас появились вопросы - нажмите на кнопку "
                    "'Хочу консультацию' и мы подробно на них ответим"
                ),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=projects_kb,
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in projects callback for user "
                f"{message.from_user.id}: {e}",
                exc_info=True,
            )

    async def pipes_cleaning_callback(self, message: Message) -> None:
        caption = (
            "*Накипь, ржавчина, мусор — всё, что съедает ваш котёл, бойлер "
            "и трубы изнутри.*\n\n"
            "Мы вычищаем — до состояния 'как новый'.\n"
            "🛠️ Чистка котлов, бойлеров, труб — быстро и качественно.\n"
            "👉 Не ждите аварии! Проверьте своё оборудование уже сегодня.\n"
            "📩 Напишите — сделаем чистку за 1 день.\n\n"
        )
        await self._send_media_group(message, "calc_plaque", caption)

    async def warm_floor_callback(self, message: Message) -> None:
        caption = (
            "🔥 *Теплый пол — комфорт и экономия круглый год*\n\n"
            "*Холодные полы, сквозняки, высокая влажность — всё это делает "
            "ваш дом неудобным.*\n\n"
            "Мы укладываем тёплые полы — ровно, надёжно, безопасно.\n"
            "🛠️ Монтаж теплых полов под любые покрытия: "
            "плитка, ламинат, паркет.\n"
            "⚡ Быстрое подключение к системе отопления и управление через "
            "терморегулятор.\n"
            "👉 Забудьте про холод и сырость — сделайте дом комфортным уже "
            "сегодня.\n"
            "📩 Свяжитесь с нами — проконсультируем и рассчитаем стоимость "
            "за 1 день."
        )
        await self._send_media_group(
            message,
            "warm_floor_installation",
            caption)

    async def pipes_routing_callback(self, message: Message) -> None:
        caption = (
            "🔧 *Профессиональная разводка труб —"
            " залог надежного отопления*\n\n"
            "*Хаотичная прокладка и некачественные соединения приводят к "
            "утечкам, шуму и поломкам.*\n\n"
            "Мы делаем аккуратную, продуманную разводку — надёжно, "
            "эстетично, безопасно.\n"
            "🛠️ Монтаж труб любой сложности, под ключ, "
            "с гарантией на работу.\n"
            "⚡ Оптимальная схема для котельного "
            "оборудования и бойлеров.\n"
            "👉 Забудьте про проблемы с отоплением "
            "— всё будет работать идеально.\n"
            "📩 Свяжитесь с нами — проект и монтаж за 1 день."
        )
        await self._send_media_group(message, "water_supply_routing", caption)

    async def heater_installation_callback(self, message: Message) -> None:
        caption = (
            "🔥 *Установка котлов и бойлеров — надёжное тепло в доме*\n\n"
            "*Неправильная установка оборудования "
            "приводит к поломкам, авариям и лишним расходам.*\n\n"
            "Мы устанавливаем котлы и бойлеры — "
            "точно, безопасно, с гарантией.\n"
            "🛠️ Подключение к системе отопления и водоснабжения, "
            "настройка и пуск "
            "под ключ.\n"
            "⚡ Оптимальная работа и долгий срок службы оборудования.\n"
            "👉 Забудьте про перебои с горячей водой и отоплением — всё будет "
            "работать без проблем.\n"
            "📩 Свяжитесь с нами — монтаж и настройка за 1 день."
        )
        await self._send_media_group(message, "heater_installation", caption)

    async def main_callback(self, message: Message) -> None:
        await message.delete()
        await StartHandler.start(message)

    async def _send_media_group(
        self, message: Message, folder_name: str, caption: str
    ) -> None:
        try:
            PHOTO_DIR = self.BASE_DIR / "projects_images" / folder_name
            file_paths = [
                PHOTO_DIR / f
                for f in sorted(path.name for path in PHOTO_DIR.iterdir())
                if f.endswith(".jpg")
            ]
            if not file_paths:
                logger.error(f"No files found in folder: {PHOTO_DIR}")
                return

            media = []
            for i, path in enumerate(file_paths):
                if i == 0:
                    media.append(
                        InputMediaPhoto(
                            media=FSInputFile(path),
                            caption=caption,
                            parse_mode=ParseMode.MARKDOWN,
                            reply_markup=projects_kb,
                        )
                    )
                else:
                    media.append(InputMediaPhoto(media=FSInputFile(path)))
            await bot.send_media_group(chat_id=message.chat.id, media=media)
        except Exception as e:
            logger.error(f"Error sending media group: {e}", exc_info=True)


router = Router()
ProjectsHandlers(router)
