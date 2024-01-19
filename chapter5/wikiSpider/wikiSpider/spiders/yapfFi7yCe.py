from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ArticleSpider(CrawlSpider):
    name = 'articles'
    allowed_domains = ['wikipedia.org']
    start_urls = [
        'https://en.wikipedia.org/wiki/'
        'Benevolent_dictator_for_life'
    ]
    rules = [
        Rule(
            LinkExtractor(allow='^(/wiki/)((?!:).)*'),
            callback='parse_items',
            follow=True,
            cb_kwargs={'is_article': True},
        ),
        Rule(
            LinkExtractor(allow=r".*"),
            callback="parse_items",
            follow=True,
            cb_kwargs={'is_article': False},
        )
    ]

    def parse(self, response, is_article):
        print(f'URL is: {response.url}')
        title = response.css('h1 span::text').get()
        if is_article:
            text = response.xpath(
                '//div[@id="mw-content-text"]//text()').extract()
            lastUpdated = response.css(
                'li#footer-inf-lastmod::text').extract_first()
            lastUpdated = lastUpdated.replace('This page was last edited on ',
                                              '')
            print(f'Title is {title}')
            print(f'Text is: {text}')
            print(f'Last updated: {lastUpdated}')
        else:
            print(f'This is not an article: {title}')
