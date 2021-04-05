import scrapy


class FoxSpider(scrapy.Spider):
    name = 'fox'
    allowed_domains = ['foxnews.com']
    start_urls = ['http://foxnews.com/']

    def parse(self, response):
        newstype_to_scrap = ['business', 'politics', 'lifestyle', 'sports']

        news_type = response.css('#main-nav > ul > li > a::text').getall()
        news_type_urls = response.css('#main-nav > ul > li > a::attr(href)').getall()

        for category, url in zip(news_type, news_type_urls):
            if category.lower() in newstype_to_scrap:
                yield scrapy.Request(url, self.parse_articles, cb_kwargs=dict(category=category.lower()))

    def parse_articles(self, response, category):
        sect_1 = response.css('div.info > header > h2 > a::attr(href)').getall()
        sect_2 = response.css('div.info > header > h4 > a::attr(href)').getall()

        for url in sect_1 + sect_2:
            article_url = "https://www.foxnews.com/" + url

            yield scrapy.Request(article_url, self.parse_story, cb_kwargs=dict(category=category))

    def parse_story(self, response, category):
        title = response.css('main > article > header > h1::text').get()
        article = response.css(' div.article-content > div.article-body > p::text').getall()

        article = ' '.join([paragraph for paragraph in article])

        yield {
            'Title': title,
            'Category': category,
            'Article_url': response.url,
            'Article': article
        }
