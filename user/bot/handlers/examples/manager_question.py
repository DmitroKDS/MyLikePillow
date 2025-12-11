from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router

import logging

from bot.functions import inline_keyboard

import db

from datetime import datetime


router = Router()


@router.callback_query(F.data == 'question_to_manager')
async def ask(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    logging.info(f"Question to manager | User ID and Name: {callback_query.message.from_user.id}, {callback_query.message.from_user.username}")

    await callback_query.message.answer(
f"""💬 Маєте запитання?
Просто натисніть кнопку, щоб поставити його тут у чаті! 😊""",
        reply_markup=inline_keyboard.create(("Запитай тут", "url:https://t.me/mylikepillow_s_bot"))
    )

    await db.update(
        "INSERT INTO messages(problem, contact_id, date, status, log) VALUES (%s, %s, %s, %s, %s)",
        (
            "Питання",
            callback_query.message.chat.id,
            datetime.now(),
            0,
            f"{datetime.now().strftime("%d.%m.%Y %H:%M")} - Питання було створено"
        )
    )