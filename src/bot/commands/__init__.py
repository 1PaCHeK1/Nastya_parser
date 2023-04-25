from .registration import router as registration_router
from .other import router as other_router
from .quize import router as quize_router
from .word import router as word_router

__all__ = [
    "registration_router",
    "other_router",
    "quize_router",
    "word_router",
]
