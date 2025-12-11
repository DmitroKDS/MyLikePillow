from aiogram.filters import CommandStart, CommandObject
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram import Router

import logging

import config

import db

from .start import init as start

from datetime import datetime



router = Router()


@router.message(CommandStart(deep_link=True))
async def init(message: types.Message, state: FSMContext, command: CommandObject) -> None:
    param = command.args

    if f"paid{config.PAID_TOKEN}" in param:
        order_id = int(param.split(f"paid{config.PAID_TOKEN}")[1])

        logging.info(f"User paid order {order_id} | User ID and Name: {message.from_user.id}, {message.from_user.username}")

        await db.update(
            """
            UPDATE orders SET status=%s, log=CONCAT(%s, COALESCE(log, ''))
            WHERE order_id=%s
            """,
            (
                1,
                f"{datetime.now().strftime('%d.%m.%Y %H:%M')} - Замовлення оплачене\n",
                order_id
            )
        )

        await message.answer(
f"""Дякую за оплату. 
Ви оплатили замовлення номер - {order_id.zfill(8)}"""
        )

    elif "channel" in param:
        channel = int(param.replace("channel", ""))

        logging.info(f"User joined from channel {channel} | User ID and Name: {message.from_user.id}, {message.from_user.username}")

        await start(message, state, channel)