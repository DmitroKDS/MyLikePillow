from aiogram.filters import CommandStart
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram import Router

import logging

import db

from bot.functions import reply_keyboard


router = Router()


@router.message(CommandStart())
@router.message(F.text == "🔙 Почати з початку")
async def init(message: types.Message, state: FSMContext, channel: int|None = None) -> None:
    logging.info(f"Start | User ID and Name: {message.from_user.id}, {message.from_user.username}")
    print(message.from_user)

    contact = await db.select(
        "SELECT full_name, phone FROM contacts WHERE id = %s LIMIT 1", 
        (
            message.chat.id,
        )
    )
    
    if len(contact)==0:
        if channel!=None:
            await db.update(
                "UPDATE channels SET count = count + 1 WHERE id = %s",
                (
                    channel,
                )
            )

        await message.answer(
"""Привіт!
Ми – майстерня улюблених подушок MyLikePillow! 💥
Давайте почнемо зі знайомства.
Завантажте, будь ласка, контакт для авторизації.""",
            reply_markup=reply_keyboard.create(("Завантажити контакт", "contact"))
        )


    else:
        await message.answer(
f"""Привіт {contact[-1][0]} !😏 

Хочеш створити унікальну подушку зі своїм дизайном? 
Тоді ти за адресою! Ми робимо круті ростові подушки до 2 метрів! 🛌💥

Завантаж своє фото (чи друга, котика або кумира), і наш бот разом із штучним інтелектом прибере фон, підготує візуалізацію, а ми зробимо подушку твоєї мрії! Все просто і швидко! 🎉

Лише обери бажаний розмір – від 30 см до 2 метрів! ✨""",
            reply_markup=reply_keyboard.create("✨ Створити подушку", "💰 Вартість та склад", "🔍 Переглянути приклади", "🔙 Почати з початку")
        )

        await state.clear()