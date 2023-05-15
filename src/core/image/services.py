from typing import IO, BinaryIO
from PIL import Image, ImageFilter
from contextlib import contextmanager

import pytesseract

import enum
import tempfile


class LanguageEnum(enum.Enum):
    auto = enum.auto()
    rus = enum.auto()
    eng = enum.auto()


class ImageProcessService:
    def get_text_from_image(
        self,
        image: Image.Image | BinaryIO |  bytes,
        lang: LanguageEnum = LanguageEnum.auto,
    ) -> str:
        with self.build_image(image) as image:
            lang = self.analyze_language(image, lang)
            return self._parse_text_from_image(image, lang)

    def _parse_text_from_image(
        self,
        image: Image.Image,
        lang: LanguageEnum,
    ) -> str:
        prepared_image = (
            image
            .convert("L")
            .filter(
                ImageFilter.SMOOTH_MORE(),
            )
        )
        return pytesseract.image_to_string(
            prepared_image,
            lang=lang.name,
        )

    def analyze_language(
        self,
        image: Image.Image,
        lang: LanguageEnum,
    ) -> LanguageEnum:
        if lang is not LanguageEnum.auto:
            return lang
        return LanguageEnum.eng

    @contextmanager
    def build_image(
        self,
        image: Image.Image | BinaryIO | bytes,
    ) -> Image.Image:
        if isinstance(image, Image.Image):
            yield image
        elif isinstance(image, bytes):
            with tempfile.TemporaryFile("w+b") as file:
                file.write(image)
                yield Image.open(file)
        else:
            yield Image.open(image)
