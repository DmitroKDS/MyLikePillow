from config import PRICES

from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router

import logging

from bot.functions import inline_keyboard

from . import pay_method


router = Router()


class CustomQuantity(StatesGroup):
    waiting = State()

@router.callback_query(F.data.contains("size"))
async def ask(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    logging.info(f"User selected size | User ID and Name: {callback_query.message.from_user.id}, {callback_query.message.from_user.username}")

    id = (await state.get_data())["order"]["id"]
    size = callback_query.data.split("size")[1]
    await state.update_data(order={"id":id, "size":size})

    order_price = PRICES.get(size, 0)

    await callback_query.message.answer(
f"""🎉 Крок 2. Тепер виберіть кількість яку вам потрібно
1 - вартість {order_price} грн
2 - вартість {order_price*2} грн
3 - вартість {order_price*3} грн
Своя кількість - вартість в залежності від кількості

Яку кількість обираєш? 😊""",
        reply_markup=inline_keyboard.create(("1", "quantity1"), ("2", "quantity2"), ("3", "quantity3"), ("Своя кількість", "custom_q"))
    )


@router.callback_query(F.data == 'custom_q')
async def custom_quantity(callback_query: types.CallbackQuery, state: FSMContext):
    logging.info(f"User want custom quantity | User ID and Name: {callback_query.message.from_user.id}, {callback_query.message.from_user.username}")

    await callback_query.message.answer(
        """Відправте в чат кількість яку ви хочете (Наприклад: 10) 😊"""
    )

    await state.set_state(CustomQuantity.waiting)


@router.message(
    (F.content_type == "text"),
    CustomQuantity.waiting
)
async def set_custom_quantity(message: types.Message, state: FSMContext):
    logging.info(f"User selected custom quantity | User ID and Name: {message.from_user.id}, {message.from_user.username}")

    quantity = message.text

    if not quantity.isdigit() or int(quantity) <= 0:
        return
    
    quantity = int(quantity)

    await pay_method.ask(message, state, quantity)