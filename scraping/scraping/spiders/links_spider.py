import scrapy


class LinksSpider(scrapy.Spider):
    name = "espn"

    def start_requests(self):
        url_base = 'http://www.espn.com/nfl/news/archive/_/month/'
        months = ['september', 'october', 'november', 'december']
        years = ['2010', '2011', '2012', '2013']

        month_bases = [url_base + month for month in months]

        urls = []
        for year in years:
            for base in month_bases:
                urls.append(base + r'/year/' + year)
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