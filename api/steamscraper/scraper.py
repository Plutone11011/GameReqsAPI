from scrapy import Item, Field
from scrapy.exceptions import CloseSpider
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class SteamSpider(CrawlSpider):
    name = 'store.steampowered'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['https://store.steampowered.com/app']

    rules = (Rule(LinkExtractor(allow=('1284410/',)), callback='parse_item'),)

    custom_settings = {'ITEM_PIPELINES': {'api.steamscraper.pipeline.SteamPipeline': 100}}


    def parse_item(self, response):
        #if 'Bandwidth exceeded' in response.body:
        #    raise CloseSpider('bandwidth_exceeded')

        item_loader = ItemLoader(ItemGame(), response=response)
        item_loader.add_css('name', '.apphub_AppName::text')
        item_loader.add_css('description', '.game_description_snippet::text')
        return item_loader.load_item()


class ItemGame(Item):
    name = Field()
    description = Field(output_processor=MapCompose(lambda des : des.strip('\r\t\n')))
    # developer = Field()
    # ram_min = Field()
    # cpu_min = Field()
    # gpu_min = Field()
    # OS_min = Field()
    # storage_min = Field()
    # ram_rec = Field()
    # cpu_rec = Field()
    # gpu_rec = Field()
    # OS_rec = Field()
    # storage_rec = Field()