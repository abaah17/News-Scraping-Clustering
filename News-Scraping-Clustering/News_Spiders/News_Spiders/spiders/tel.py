import scrapy


class TelSpider(scrapy.Spider):
    name = 'tel'
    allowed_domains = ['telegraph.co.uk']
    start_urls = ['http://telegraph.co.uk/']

    def parse(self, response):
        newstype_to_scrap = ['politics', 'sports', 'business', 'style']

        news_type = response.css('div.site-header__primary-navigation-wrapper > div > nav > ul > li > a::attr('
                                       'href)').getall()

        for category in news_type:
            if category.split("/")[1] in newstype_to_scrap:
                category_url = response.url + category

                yield scrapy.Request(category_url, callback=self.parse_articles,
                                     cb_kwargs=dict(category=category.split("/")[1]))

    def parse_articles(self, response, category):
        article_urls = response.css('section > ul > li > article > div.card__content > h3 > a::attr(href)').getall()

        for url in article_urls:
            article_url = "https://www.telegraph.co.uk" + url

            yield scrapy.Request(article_url, callback=self.parse_story, cb_kwargs=dict(category=category))

    def parse_story(self, response, category):
        title = response.css('article > header > h1::text').get()
        article = response.css(
            'article > div.grid-col.grid-col-12.article__layout.article__layout--content > div:nth-child(1) > '
            'div.articleBodyText.section > div.component.article-body-text > p::text').getall()

        article = ' '.join([paragraph for paragraph in article])

        yield {
            'Title': title,
            'Category': category,
            'Article_url': response.url,
            'Article': article
        }
