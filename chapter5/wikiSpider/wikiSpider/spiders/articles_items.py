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
        print(20 * "-")
        print(f'URL is: {response.url}')
        article = Article()
        article['url'] = response.url
        article['title'] = response.css('h1 span::text').get()
        article['text'] = response.xpath(
            '//div[@id="mw-content-text"]//text()').extract()
        lastUpdated = response.css(
            'li#footer-inf-lastmod::text').extract_first()
        if lastUpdated:
            article['lastUpdated'] = lastUpdated.replace(
                'This page was last edited on ', '')
        print(f'Title is {article["title"]}')
        print(f'Last updated: {lastUpdated}')
        return article
