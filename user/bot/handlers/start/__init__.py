from aiogram import Router
from .contact import router as contact_router
from .start import router as start_router
from .start_with_param import router as start_with_param_router

router = Router()
router.include_router(contact_router)
router.include_router(start_router)
router.include_router(start_with_param_router)