from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router

import logging

from bot.functions import inline_keyboard

import io

import db

import asyncio

from PIL import Image

import config

import bg

from bg.img import thumbnail


router = Router()


class ImgToPillow(StatesGroup):
    waiting = State()

@router.message(lambda message: message.text == '✨ Створити подушку')
@router.callback_query(F.data == 'upload_pil')
async def upload(message: types.Message | types.CallbackQuery, state: FSMContext) -> None:
    if isinstance(message, types.CallbackQuery):
        message = message.message

    logging.info(f"User get pillow | User ID and Name: {message.from_user.id}, {message.from_user.username}")

    await message.answer(
        """🔽 Завантаж зображення, яке потрібно надрукувати на подушці.

Якість буде краща, якщо скористатися функцією завантажити, як “Файл”"""
    )

    await state.set_state(ImgToPillow.waiting)
    await state.update_data(processed=True)




@router.message(F.content_type.in_(['photo', 'document', 'sticker']), ImgToPillow.waiting)
async def create(message: types.Message, state: FSMContext):
    logging.info(f"User create pillow | User ID and Name: {message.from_user.id}, {message.from_user.username}")

    if not (await state.get_data()).get("processed", False):
        logging.info(f"Ignored additional upload | User ID: {message.from_user.id}")
        return
    
    await state.clear()

    contact_id = message.chat.id

    pillow_image_io = io.BytesIO()
    image_format="png"
    
    if message.content_type == 'photo':
        await message.bot.download(message.photo[-1], destination=pillow_image_io)
    elif message.content_type in 'document':
        await message.bot.download(message.document, destination=pillow_image_io)
        image_format = message.document.file_name.split(".")[-1]
    elif message.content_type == 'sticker':
        await message.bot.download(message.sticker, destination=pillow_image_io)
        image_format = "webp"


    if image_format in ["png", "jpg", "jpeg", "webp", "heic"]:
        request_id = await db.update("INSERT INTO requests(contact_id) VALUES (%s)",
            (
                contact_id,
            )
        )

        await message.answer(
f"""Твоя заявка №{str(request_id).zfill(8)}.

✨ Чудово! Потрібно зачекати від 1 до 5 хвилин ⏳.
Наш розумний ШІ 🤖 вже аналізує зображення 🖼️ та видаляє фон 🌟!"""
        )


        got_img = Image.open(pillow_image_io)

        got_img_path = f"data/got_img/{request_id}.png"

        await asyncio.to_thread(got_img.save, got_img_path)

        logging.info(f"Got image saved | User ID and Name: {message.from_user.id}, {message.from_user.username}")



        result = await bg.remove_img(got_img, f"{config.FTP}/{got_img_path}")

        no_bg_img_path, no_bg_img = list(result.items())[0]
        pil_effect_img_path, pil_effect_img = list(result.items())[1]

        await asyncio.to_thread(no_bg_img.save, no_bg_img_path)

        logging.info(f"No bg image saved | User ID and Name: {message.from_user.id}, {message.from_user.username}")


        await asyncio.to_thread(pil_effect_img.save, pil_effect_img_path)

        logging.info(f"Pillow effect image saved | User ID and Name: {message.from_user.id}, {message.from_user.username}")



        preview_img = await asyncio.to_thread( thumbnail.init, pil_effect_img, (600, 600) )

        preview_img_bytes = io.BytesIO()
        await asyncio.to_thread(preview_img.save, preview_img_bytes, format='PNG')
        preview_img_bytes.seek(0)



        await message.answer_photo(
            types.BufferedInputFile(
                preview_img_bytes.read(),
                filename=f"{request_id}_preview.png"
            )
        )

        logging.info(f"Preview image sent | User ID and Name: {message.from_user.id}, {message.from_user.username}")



        await message.answer(
"""🏆 Ось, що вийшло після видалення фону.

❔Чи подобається такий результат результат?

ℹ️ Чорна лінія то є відображення контуру подушки на готовій подушці їх не буде.""",
            reply_markup=inline_keyboard.create(('✅ Так, все чудово. Продовжити замовлення', f'make_order{request_id}'), ('❌ Ні, щось не подобається.', f'something_wrong{request_id}'), ('🆕 Хочу завантажити інше фото', 'upload_pil'))
        )



    else:

        await message.answer(
"""📂 Ой, щось пішло не так! Ви завантажили файл у форматі, який ми, на жаль, не можемо обробити. 😔

✅ Завантажте, будь ласка, файл у форматі JPG, PNG або JPEG – і все запрацює! 🎉
Якщо виникнуть питання, ми завжди поруч, щоб допомогти! 😊"""
        )




@router.callback_query(F.data.contains('revote'))
async def revote(callback_query: types.CallbackQuery):
    logging.info(f"Preview image sent | User ID and Name: {callback_query.message.from_user.id}, {callback_query.message.from_user.username}")

    request_id = callback_query.data.split("revote")[-1]

    await callback_query.message.answer(
"""❔Чи все подобається вам в результаті?""",
        reply_markup=inline_keyboard.create(('✅ Так, все чудово. Продовжити замовлення', f'make_order{request_id}'), ('❌ Ні, щось не подобається.', f'something_wrong{request_id}'), ('🆕 Хочу завантажити інше фото', 'upload_pil'))
    )