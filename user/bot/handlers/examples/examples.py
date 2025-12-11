from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram import Router

import logging

import os

from bot.functions import inline_keyboard


router = Router()


@router.message(lambda message: message.text == '🔍 Переглянути приклади')
async def init(message: types.Message) -> None:
    logging.info(f"User in examples | User ID and Name: {message.from_user.id}, {message.from_user.username}")

    await message.answer(
"""🖼 Ось кілька прикладів наших подушок:"""
    )

    media = [types.InputMediaPhoto(media=types.FSInputFile(f"data/examples/{image}")) for image in os.listdir("data/examples/")]

    if media:
        await message.answer_media_group(
            media
        )

    await message.answer(
"""❓ Сподобалися приклади?
✅ Можемо перейти до створення подушки?""",
        reply_markup=inline_keyboard.create(('🌟 Створити подушку', 'upload_pil'), ('❓ В мене є питання', 'question_to_manager'))
    )