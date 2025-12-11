from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router

import logging

from bot.functions import inline_keyboard
from bot.functions import work_time

import db

import config

from datetime import datetime


router = Router()


@router.callback_query(F.data.contains('question_to_designer'))
async def ask(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    logging.info(f"Question to manager | User ID and Name: {callback_query.message.from_user.id}, {callback_query.message.from_user.username}")

    question_type, request_id = callback_query.data.split('question_to_designer')[1].split("_")

    await callback_query.message.answer(
f"""💬 Маєте проблему чи запитання до дизайнера?
Натискайте на кнопку нижче, щоб описати це прямо тут у чаті. Ми зробимо все можливе, щоб допомогти! 💪✨""",
        reply_markup=inline_keyboard.create(("Запитай тут", "url:https://t.me/mylikepillow_s_bot"))
    )

    await db.update(
        "INSERT INTO messages(problem, contact_id, request_id, date, status, log) VALUES (%s, %s, %s, %s, %s, %s)",
        (
            config.DESIGNER_QUESTIONS[question_type],
            callback_query.message.chat.id,
            request_id,
            datetime.now(),
            0,
            f"{datetime.now().strftime("%d.%m.%Y %H:%M")} - Питання було створено"
        )
    )