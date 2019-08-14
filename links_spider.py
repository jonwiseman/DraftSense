import scrapy


class LinksSpider(scrapy.Spider):
    name = "espn"


    def start_requests(self):
        url_base = 'http://www.espn.com/nfl/news/archive/_/month/'
        months = ['January', 'February', 'August', 'September', 'October', 'November', 'December']
        years = ['2013', '2014']

        fall_months = [f'{url_base}{month}/year/{years[0]}' for month in months[2:]]
        spring_months = [f'{url_base}{month}/year/{years[1]}' for month in months[:2]]

        urls = fall_months + spring_months
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        for link in response.css('ul.inline-list.indent a::attr(href)').getall():
            yield response.follow(link, self.parse_article)


    def parse_article(self, response):
        yield{
            'title': response.css('h1::text').get(),
            'author': response.css('ul.authors div.author.has-bio::text').get(),
            'date': response.css('span.timestamp span::text').get(),
            'content': ' '.join(response.css('div.article-body p *::text').getall()).replace(" '", "'"),
            'link': response.request.url
        }
