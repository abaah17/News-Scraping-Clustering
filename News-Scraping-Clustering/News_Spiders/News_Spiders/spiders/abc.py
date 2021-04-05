import scrapy


class AbcSpider(scrapy.Spider):
    name = 'abc'
    allowed_domains = ['abcnews.go.com']
    start_urls = ['http://abcnews.go.com/']

    def parse(self, response):
        print(response)
        newstype_to_scrap = ['business', 'politics', 'lifestyle', 'sports']

        news_type = response.css('#global-nav > ul > li.none.more > div > ul > li > a::text').getall()
        news_type_urls = response.css('#global-nav > ul > li.none.more > div > ul > li > a::attr(href)').getall()

        for category, url in zip(news_type, news_type_urls):
            if category.strip().lower() in newstype_to_scrap:
                yield scrapy.Request(url, self.parse_articles, cb_kwargs=dict(category=category.strip().lower()))

    # to get the urls of differing sections in the categoy page
    def parse_articles(self, response, category):
        sect_1 = response.css('div.band__lead.band > div > div > div > a::attr(href)').getall()
        sect_2 = response.css(
            'div.block__double-column.block > section > section > div > h2 > a::attr(href)').getall()

        for url in sect_1 + sect_2:
            yield scrapy.Request(url, self.parse_story, cb_kwargs=dict(category=category))

    # function to scrape content from news article
    def parse_story(self, response, category):
        title = response.css('header > div > h1::text').get()
        article = response.css('div.Article > section > article > section > p::text').getall()

        article = ' '.join([paragraph for paragraph in article])

        yield {
            'Title': title,
            'Category': category,
            'Article_url': response.url,
            'Article': article
        }
