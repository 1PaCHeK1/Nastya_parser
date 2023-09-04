from fastapi import Request
from starlette import status
from fastapi.responses import JSONResponse
from business_validator import ErrorSchema, ValidationError


async def handle_validation_errors(
    request: Request,
    exc: ValidationError[ErrorSchema],
):
    return JSONResponse(
        content=[error.dict() for error in exc.messages],
        status_code=status.HTTP_400_BAD_REQUEST,
    )
