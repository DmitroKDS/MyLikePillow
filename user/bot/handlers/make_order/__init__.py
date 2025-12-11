from aiogram import Router
from .size import router as size_router
from .quantity import router as quantity_router
from .pay_method import router as pay_method_router

router = Router()

router.include_router(size_router)
router.include_router(quantity_router)
router.include_router(pay_method_router)