from aiogram import Router
from .examples import router as examples_router
from .manager_question import router as manager_question_router

router = Router()

router.include_router(examples_router)
router.include_router(manager_question_router)