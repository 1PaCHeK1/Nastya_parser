# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WordItem(scrapy.Item):
    word: str = scrapy.Field()
    translate_words: list[str] = scrapy.Field()
