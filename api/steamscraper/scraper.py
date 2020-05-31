import click
import scrapy
from flask.cli import with_appcontext
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class SteamSpider(CrawlSpider):
    name = 'store.steampowered'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['https://store.steampowered.com/app']

    rules = (Rule(LinkExtractor(allow=('app/262060/',) ),callback='parse_item'),)

    def parse_item(self, response):
        print(response.css('.sysreq_contents').get())
        return None
