# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from typing import Annotated

from core.words.services import WordService
from core.words.schemas import WordCreateSchema
from aioinject import inject, Inject
from .items import WordItem


class SpiderPipeline:
    @inject
    async def process_item(
        self, item: WordItem, spider, word_service: Annotated[WordService, Inject]
    ):
        await word_service.append_word(
            WordCreateSchema(
                word=item["word"],
                translate_words=item["`translate_words`"],
            )
        )

        return item
