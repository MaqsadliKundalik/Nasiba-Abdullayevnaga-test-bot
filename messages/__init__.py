from . import register, check_test, manage_test
from aiogram import Router

router = Router()

router.include_router(register.router)
router.include_router(check_test.router)
router.include_router(manage_test.router)