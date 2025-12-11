from aiogram import Router
from .about import router as about_router

router = Router()

router.include_router(about_router)