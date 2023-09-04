from collections.abc import Sequence

from business_validator import ErrorSchema
from fastapi import UploadFile

from core.image.services import ImageProcessService

from .validators import ImageValidator


class ReadTextFromImageUseCase:
    def __init__(
        self,
        service: ImageProcessService,
    ) -> None:
        self.service = service

    async def execute(self, file: UploadFile) -> str | Sequence[ErrorSchema]:
        errors = await ImageValidator(file).errors()
        if errors:
            return errors

        return self.service.get_text_from_image(file.file)
