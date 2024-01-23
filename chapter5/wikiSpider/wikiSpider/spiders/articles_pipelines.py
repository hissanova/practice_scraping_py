from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wikiSpider.items import Article


class ArticleSpider(CrawlSpider):
    name = 'article_items'
    allowed_domains = ['wikipedia.org']
    start_urls = [
        'https://en.wikipedia.org/wiki/'
        'Benevolent_dictator_for_life'
    ]
    rules = [
        Rule(
            LinkExtractor(allow='(/wiki/)((?!:).)*'),
            callback='parse_items',
            follow=False,
        ),
    ]

    def parse_items(self, response):
        article = Article()
        article['url'] = response.url
        article['title'] = response.css('h1 span::text').get()
        article['text'] = response.xpath(
            '//div[@id="mw-content-text"]//text()').extract()
        article['last_updated'] = response.css(
            'li#footer-info-lastmod::text').extract_first()
        return article
