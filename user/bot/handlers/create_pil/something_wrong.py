from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram import Router

import logging

from bot.functions import inline_keyboard


router = Router()

@router.callback_query(F.data.contains('something_wrong'))
async def init(callback_query: types.CallbackQuery, state: FSMContext):
    logging.info(f"User create pillow | User ID and Name: {callback_query.message.from_user.id}, {callback_query.message.from_user.username}")

    request_id = callback_query.data.split("something_wrong")[-1]

    await callback_query.message.answer(
"""🤔 Що саме вам не сподобалось? Ми зробимо все, щоб ваша подушка була ТОП! 💪✨""",
        reply_markup=inline_keyboard.create(('На макеті подушки зайвий елемент', f'question_to_designer1_{request_id}'), ('Інше', f'question_to_designer2_{request_id}'), ('Повернутись на шаг назад', f'revote{request_id}'))
    )