from fastapi import APIRouter

from .auth import router as auth_router
from .word import router as word_router


router = APIRouter()

router.include_router(auth_router)
router.include_router(word_router)