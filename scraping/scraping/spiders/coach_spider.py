import scrapy
import pickle


class CoachSpider(scrapy.Spider):
    name = "Coach"

    def start_requests(self):
        teams = pickle.load(open('/home/jon/Desktop/thesis/Pickles/2010/full_names.p', 'rb'))
        years = ['2010', '2011', '2012', '2013']

        for year in years:
            for team in teams:
                url = f"https://en.wikipedia.org/wiki/{year}_{'_'.join(team.split(' '))}_season"
                identifier = team + "_" + year
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield {
            'Metadata': response.css('h1 ::text').extract()[0],
            'Coach': response.css('table.infobox.vcard td.agent ::text').extract()[0]
        }
