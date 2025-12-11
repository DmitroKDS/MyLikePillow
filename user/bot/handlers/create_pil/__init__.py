from aiogram import Router
from .pil import router as pil_router
from .designer_question import router as designer_question_router
from .something_wrong import router as something_wrong_router

router = Router()

router.include_router(pil_router)
router.include_router(designer_question_router)
router.include_router(something_wrong_router)