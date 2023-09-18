from aiogram import Router

from . import (
    registration,
    other,
    quize,
    word,
    parse_image,
    email,
    reminder,
)


router = Router(name="main")


router.include_router(registration.router)
router.include_router(other.router)
router.include_router(quize.router)
router.include_router(parse_image.router)
router.include_router(email.router)
router.include_router(reminder.router)
router.include_router(word.router)
