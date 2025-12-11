import asyncio

from aiogram import Dispatcher

from bot_instance import bot
from bot.handlers.start import router as start_router
from bot.handlers.about import router as about_router
from bot.handlers.examples import router as examples_router
from bot.handlers.create_pil import router as create_pil_router
from bot.handlers.make_order import router as make_order_router

from db import create_db

from bot.handlers.errors import catch

import logging

import os


def create_folders(names: str|list) -> None:
    """
    Create folders if not exist
    """
    if isinstance(names, str):
        names = [names]
        
    for name in names:
        if not os.path.exists(name):
            os.makedirs(name)


def register_routes(dispatcher: Dispatcher) -> None:
    """
    Initialize routes of the bot
    """
    logging.info(f"Initialize routers")

    dispatcher.include_router(start_router)
    dispatcher.include_router(about_router)
    dispatcher.include_router(examples_router)
    dispatcher.include_router(create_pil_router)
    dispatcher.include_router(make_order_router)


async def main() -> None:
    """
    The main function that create and start bot
    """
    create_folders(["data", "data/got_img", "data/no_bg", "data/pil_effect", "data/examples"])

    await create_db()

    dispatcher = Dispatcher()

    dispatcher.errors.register(catch)

    register_routes(dispatcher)

    await dispatcher.start_polling(bot, timeout=160)


if __name__ == '__main__':
    # Start loggining

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("bot_logs.log"),
            logging.StreamHandler(),
        ],
    )


    # Run the bot

    asyncio.run(main())