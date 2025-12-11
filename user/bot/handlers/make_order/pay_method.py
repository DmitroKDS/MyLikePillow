from config import PRICES

from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram import Router

import logging

from bot.functions import inline_keyboard

from bot.functions import offer

import db

from datetime import datetime


router = Router()


@router.callback_query(F.data.contains("quantity"))
async def ask(message: types.CallbackQuery | types.Message, state: FSMContext, quantity: str = None) -> None:
    if quantity == None: 
        quantity = int(message.data.split('quantity')[-1])
        message = message.message

    logging.info(f"User selected quantity | User ID and Name: {message.from_user.id}, {message.from_user.username}")

    id  = (await state.get_data())["order"]["id"]
    size  = (await state.get_data())["order"]["size"]
    order = {
        "id": id,
        "size": size,
        "quantity": quantity
    }
    price = PRICES.get(order["size"], 0)

    await state.update_data(order=order)


    await message.answer(
f"""Ваше замовлеення - {str(id).zfill(8)}
{quantity} подуш{"ка" if quantity==1 else ("ки" if quantity<5 else "ок")} розміром — {size}
До сплати — {quantity*price} грн.

Тепер обирай зручний спосіб оплати та доставки:
1️⃣ Повна оплата через систему MonoPay.

2️⃣ Накладений платіж – сплачуєш лише завдаток у розмірі 300 грн, решту при отриманні.

Обирай свій варіант, і вперед до мрії! 😊💳📦""",
        reply_markup=inline_keyboard.create(("1️⃣", "pay_method1"), ("2️⃣", "pay_method2"))
    )



@router.callback_query(F.data.contains('pay_method'))
async def pay(callback_query: types.CallbackQuery, state: FSMContext):
    logging.info(f"User selected quantity | User ID and Name: {callback_query.message.from_user.id}, {callback_query.message.from_user.username}")

    order = (await state.get_data())["order"]
    price = PRICES.get(order["size"], 0)
    pay_method = callback_query.data.split("pay_method")[1]

    offer_url = await offer.create(order["id"], order["size"], order["quantity"], price, order["quantity"]*price if pay_method=="1" else 300)

    orders = await db.select("SELECT status FROM orders WHERE request_id=%s", (order["id"],))
    if len(orders)==0:
        await db.update(
            """
            INSERT INTO orders(request_id, contact_id, pay_method, pil_size, pil_quantity, full_price, date, status, log)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                order["id"],
                callback_query.message.chat.id,
                pay_method,
                order["size"],
                order["quantity"],
                order["quantity"]*price,
                datetime.now(),
                0,
                f"{datetime.now().strftime("%d.%m.%Y %H:%M")} - Замовлення було створено"
            )
        )
    elif orders[-1][0]==0:

        await db.update(
            """
            UPDATE orders SET pay_method=%s, pil_size=%s, pil_quantity=%s, full_price=%s, date=%s, log=CONCAT(%s, COALESCE(log, ''))
            WHERE request_id=%s
            """,
            (
                pay_method,
                order["size"],
                order["quantity"],
                order["quantity"]*price,
                datetime.now(),
                f"{datetime.now().strftime("%d.%m.%Y %H:%M")} - Змінено тип оплати на {pay_method.replace("1", "Повний платіж").replace("2", "Накладений платіж")}\n",
                order["id"]
            )
        )
    else:
        return


    await callback_query.message.answer(
f"""{'1️⃣' if pay_method=="1" else '2️⃣'}Давай перейдомо до оплати та вибора способа доставки.
Тицяй ось тут і оплати легко і швидко через систему MonoPay - {offer_url}"""
    )
