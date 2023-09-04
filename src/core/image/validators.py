from dataclasses import dataclass

from business_validator import ErrorSchema, Validator, validate
from fastapi import UploadFile

_AVAIBLES_CONTENT_TYPE = [
    "image/jpeg",
    "image/jpg",
    "image/png",
]

_MAX_IMAGE_SIZE = 1980 * 1080


@dataclass
class ImageValidator(Validator[ErrorSchema]):
    file: UploadFile

    @validate
    async def validate_content_type(self) -> None:
        if self.file.content_type not in _AVAIBLES_CONTENT_TYPE:
            self.context.add_error(
                ErrorSchema(code="content-type", message="avaible image"),
            )

    @validate
    async def validate_size(self) -> None:
        if self.file.size > _MAX_IMAGE_SIZE:
            self.context.add_error(
                ErrorSchema(code="large-size", message="file size very large!"),
            )
