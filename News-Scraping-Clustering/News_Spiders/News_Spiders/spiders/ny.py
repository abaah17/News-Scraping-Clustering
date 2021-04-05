import scrapy


class NySpider(scrapy.Spider):
    name = 'ny'
    allowed_domains = ['nytimes.com']
    start_urls = ['http://nytimes.com/']

    def parse(self, response):
        newstype_to_scrap = ['politics', 'sports', 'business', 'style']

        news_type = response.css('header > div.css-1d8a290 > ul > li > a::text').getall()
        news_type_urls = response.css('header > div.css-1d8a290 > ul > li > a::attr(href)').getall()

        for category, url in zip(news_type, news_type_urls):
            if category.lower() in newstype_to_scrap:
                yield scrapy.Request(url, self.parse_articles, cb_kwargs=dict(category=category.lower()))

    def parse_articles(self, response, category):
        sect_1 = response.css('ol > li > article > div > h2 > a::attr(href)').getall()
        sect_2 = response.css('ol > li > div > div.css-1l4spti > a::attr(href)').getall()

        for url in sect_1 + sect_2:
            article_url = "https://www.nytimes.com" + url
            yield scrapy.Request(article_url, self.parse_story, cb_kwargs=dict(category=category))

    def parse_story(self, response, category):
        title = response.css('header > div.css-1vkm6nb > h1::text').get()
        article = response.css('#story > section > div.css-1fanzo5  > div > p::text').getall()

        article = ' '.join([paragraph for paragraph in article])

        yield {
            'Title': title,
            'Category': category,
            'Article_url': response.url,
            'Article': article
        }
