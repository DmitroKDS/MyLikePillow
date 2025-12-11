from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram import Router

import logging

from bot.functions import inline_keyboard


router = Router()


@router.callback_query(F.data.contains("make_order"))
async def make(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    logging.info(f"User make an order | User ID and Name: {callback_query.message.from_user.id}, {callback_query.message.from_user.username}")

    request_id = callback_query.data.split("make_order")[-1]

    await state.update_data(order={"id":request_id})

    await callback_query.message.answer(
"""<b>🎉 Це зображення ідеально підходить для подушок</b>
<b>Гігантська</b> (200 см з більшої сторони) - вартість <s>5500 грн</s> <i>Для підписників каналу</i> <b>2750 грн</b>
<b>Найбільша</b> (150 см з більшої сторони) - вартість <s>4300 грн</s> <i>Для підписників каналу</i> <b>2150 грн</b>
<b>Велика</b> (100 см з більшої сторони) - вартість <s>2700 грн</s> <i>Для підписників каналу</i> <b>1350 грн</b>
<b>Середня</b> (65 см з більшої сторони) - вартість <s>1700 грн</s> <i>Для підписників каналу</i> <b>850 грн</b>
<b>Маленька</b> (35 см з більшої сторони) - вартість <s>900 грн</s> <i>Для підписників каналу</i> <b>450 грн</b>

Який розмір обираєш? 😊""",
        reply_markup=inline_keyboard.create(("Гігантська", "sizeГігантська"), ("Найбільша", "sizeНайбільша"), ("Велика", "sizeВелика"), ("Середня", "sizeСередня"), ("Маленька", "sizeМаленька"))
    )
