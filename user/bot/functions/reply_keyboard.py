from aiogram import types

def create(*buttons: list[tuple[str, str] | str]) -> types.ReplyKeyboardMarkup:
    keyboard = []
    for button in buttons:
        if isinstance(button, str):
            keyboard.append([types.KeyboardButton(text=button)])
        elif button[1]=="contact":
            keyboard.append([types.KeyboardButton(text=button[0], request_contact=True)])

    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=keyboard,
    )

    return keyboard