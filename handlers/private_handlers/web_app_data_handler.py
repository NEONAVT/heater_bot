import json
import logging
from datetime import datetime, timezone

from aiogram import types, Router, F
from aiogram.enums import ParseMode
from bot_config import telegram_client
from keyboards import remind_kb
from services import users_service, reminders_service
from settings import settings

logger = logging.getLogger(__name__)


class WebAppHandler:
    """
    Обрабатывает данные WebApp форм и медиафайлы от пользователя.
    Сохраняет заявки на обратный звонок или описание проблемы
    и отправляет их администратору.
    """

    active_requests: dict[int, dict] = {}

    def __init__(self, router: Router) -> None:
        self.router: Router = router
        self.register_handlers()

    def register_handlers(self) -> None:
        self.router.message.register(self.web_app_data_handler, F.web_app_data)
        self.router.message.register(
            self.handle_files,
            F.photo | F.video | F.document | F.voice | F.video_note
        )

    async def web_app_data_handler(self, message: types.Message) -> None:
        try:
            logger.info(
                f"Web app data received from user "
                f"{message.from_user.id}")
            logger.debug(f"Raw web app data: {message.web_app_data.data}")

            data = json.loads(message.web_app_data.data)
            form_type = data.get("form", "unknown")
            logger.info(f"Form type: {form_type}")
            logger.debug(f"Parsed data: {data}")

            if form_type == "callback":
                await self._handle_callback_form(message, data)
            elif form_type == "problem":
                await self._handle_problem_form(message, data)
            else:
                logger.warning(
                    f"Unknown form type from user "
                    f"{message.from_user.id}: {form_type}"
                )
                await message.answer(
                    "Неизвестный тип формы. Пожалуйста, попробуйте снова."
                )

        except json.JSONDecodeError as e:
            logger.error(
                f"JSON decode error from user "
                f"{message.from_user.id}: {e}"
            )
            await message.answer(
                "Ошибка обработки данных. Попробуйте снова."
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in web_app_data_handler for user "
                f"{message.from_user.id}: {e}",
                exc_info=True
            )
            await message.answer(
                "Произошла непредвиденная ошибка. Попробуйте позже."
            )

    async def _handle_callback_form(
            self, message: types.Message, data: dict
    ) -> None:
        admin_id = settings.ADMIN_CHAT_ID
        name = data.get("name", "не указано")
        phone = data.get("phone", "не указано")
        topic = data.get("topic", "не указано")
        time_val = data.get("time", "не указано")

        text_msg = (
            f"🔔 Заказан ОБРАТНЫЙ ЗВОНОК от {name.capitalize()}\n"
            f"на номер телефона {phone}\n"
            f"удобное время звонка: {time_val}\n"
            f'тема звонка: "{topic.capitalize()}"\n\n'
            f"Для связи в чате "
            f"@{message.from_user.username or 'нет username'}\n\n"
            f"❓ Напомнить позже?"
        )

        response = await telegram_client.post(
            method="sendMessage",
            chat_id=admin_id,
            text=text_msg,
            reply_markup=remind_kb
        )
        msg_id = response['result']['message_id']

        await reminders_service.save_reminder(
            chat_id=admin_id,
            message_id=msg_id,
            type_="callback",
            username=message.from_user.username
        )

        await message.answer(
            f"{message.from_user.first_name}, спасибо!\n"
            "📨 Ваша заявка на обратный звонок передана!\n"
            "С вами свяжутся наши специалисты в удобное время."
        )
        await users_service.set_phone_number(
            user_id=message.from_user.id, phone_number=phone
        )
        await users_service.update_last_data(
            user_id=message.from_user.id,
            updated_date=datetime.now(timezone.utc)
        )
        await users_service.set_client_status(
            user_id=message.from_user.id
        )
        logger.info(
            f"Callback confirmation sent to user "
            f"{message.from_user.id}"
        )

    async def _handle_problem_form(
            self, message: types.Message, data: dict
    ) -> None:
        name = data.get("name", "не указано")
        phone = data.get("phone", "не указано")
        problem = data.get("topic", "не указано")

        self.active_requests[message.chat.id] = {
            "name": name,
            "phone": phone,
            "problem": problem,
            "files": []
        }

        logger.info(
            f"Problem request started for user {message.from_user.id}: "
            f"name={name}, phone={phone}"
        )
        logger.debug(f"Problem description: {problem}")

        await message.answer(
            f"Заявка сохранена:\nИмя: {name}\nТелефон: {phone}\n"
            f"Описание проблемы: {problem}\n\n"
            "*📷 Пришлите одно фото или видео вашей проблемы.*\n"
            "*Или можете записать 🎙️голосовое или 📹видео-сообщение.*",
            parse_mode=ParseMode.MARKDOWN,
        )

        await users_service.update_last_data(
            user_id=message.from_user.id,
            updated_date=datetime.now(timezone.utc)
        )
        await users_service.set_client_status(user_id=message.from_user.id)
        logger.info(
            f"Problem request instructions sent to user "
            f"{message.from_user.id}")

    async def handle_files(self, message: types.Message) -> None:
        if message.chat.id not in self.active_requests:
            logger.warning(
                f"File received from user "
                f"{message.from_user.id} without active request"
            )
            await message.answer(
                "У вас нет активной заявки. Сначала заполните форму."
            )
            return

        req = self.active_requests[message.chat.id]
        file_type, file_id = None, None

        if message.photo:
            file_type, file_id = "photo", message.photo[-1].file_id
        elif message.video:
            file_type, file_id = "video", message.video.file_id
        elif message.document:
            file_type, file_id = "document", message.document.file_id
        elif message.voice:
            file_type, file_id = "voice", message.voice.file_id
        elif message.video_note:
            file_type, file_id = "video_note", message.video_note.file_id

        if file_type and file_id:
            req["files"].append((file_type, file_id))
            logger.info(
                f"File added to request for user {message.from_user.id}: "
                f"type={file_type}, id={file_id}"
            )
            logger.debug(f"Total files in request: {len(req['files'])}")

        await self.finalize_request(message.chat.id, message)

    async def finalize_request(
            self, chat_id: int, message: types.Message
    ) -> None:
        req = self.active_requests.pop(chat_id, None)
        if not req:
            logger.warning(
                f"Finalize request called for user "
                f"{message.from_user.id} but no active request"
            )
            await message.answer("У вас нет активной заявки.")
            return

        admin_id = settings.ADMIN_CHAT_ID
        text_msg = (
            f"🔔 Новая заявка от {req['name'].capitalize()}\n"
            f"Телефон: {req['phone']}\n"
            f"Проблема: {req['problem']}\n\n"
            f"Для связи: @{message.from_user.username or 'нет username'}\n\n"
            f"❓ Напомнить позже?"
        )

        logger.info(
            f"Sending problem request to admins: "
            f"{admin_id}, files count: {len(req['files'])}"
        )

        response = await telegram_client.post(
            method="sendMessage",
            chat_id=admin_id,
            text=text_msg,
            reply_markup=remind_kb
        )
        msg_id = response['result']['message_id']
        await reminders_service.save_reminder(
            chat_id=admin_id,
            message_id=msg_id,
            type_="problem",
            username=message.from_user.username
        )
        logger.info(f"Problem request text sent to admin {admin_id}")

        for ftype, fid in req["files"]:
            method_map = {
                "photo": "sendPhoto",
                "video": "sendVideo",
                "document": "sendDocument",
                "voice": "sendVoice",
                "video_note": "sendVideoNote"
            }
            try:
                await telegram_client.post(
                    method=method_map[ftype],
                    chat_id=admin_id,
                    **{ftype: fid})
                logger.info(f"File sent to admin {admin_id}: type={ftype}")
            except Exception as file_e:
                logger.error(
                    f"Failed to send file to admin"
                    f" {admin_id}: {file_e}")

        await message.answer("✅ Ваша заявка передана администратору.")
        logger.info(f"Request finalized for user {message.from_user.id}")


router = Router()
WebAppHandler(router)
