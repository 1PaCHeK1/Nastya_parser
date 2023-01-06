import scrapy
from scrapy.http.response.html import HtmlResponse
from ..items import WordItem


class CambridgeSpiderSpider(scrapy.Spider):
    name = 'cambridge_spider'
    allowed_domains = ['dictionary.cambridge.org']
    start_urls = [
        'http://dictionary.cambridge.org/dictionary/english-russian',
    ]

    def parse(self, response: HtmlResponse):
        favorite_words_search = response.xpath("//div[@class='x']/div/div/div/div/ul/li/a/span/span/span/text()")
        for favorite_word in favorite_words_search.getall():
            yield response.follow(response.urljoin(favorite_word), self.parse_page)
    
    def parse_page(self, response: HtmlResponse):
        words = response.xpath("//div[@class='pr entry-body__el']")
        for word in words:
            yield self.parse_word(word)

    def parse_word(self, body):
        word = body.xpath("//span[@class='headword hdb tw-bw dhw dpos-h_hw ']/span/text()").get()
        translate_words = body.xpath("//span[@class='trans dtrans dtrans-se ']/text()").get()
        return WordItem(
            word=word,
            translate_words=list(map(str.strip, translate_words.split(", ")))
        )

