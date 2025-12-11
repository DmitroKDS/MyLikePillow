from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram import Router

import logging

import db

from .start import init as start


router = Router()

@router.message(F.content_type == "contact")
async def upload(message: types.Message, state: FSMContext) -> None:
    logging.info(f"User upload contact | User ID and Name: {message.from_user.id}, {message.from_user.username}")

    contact = message.contact

    await db.update(
        "INSERT INTO contacts(id, full_name, phone) VALUES (%s, %s, %s)",
        (
            message.chat.id,
            f"{contact.first_name} {contact.last_name}",
            contact.phone_number
        )
    )

    await start(message, state)