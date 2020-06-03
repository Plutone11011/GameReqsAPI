from scrapy import Item, Field
from scrapy.exceptions import CloseSpider
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Compose
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Response

from bs4 import BeautifulSoup


class SteamSpider(CrawlSpider):
    name = 'store.steampowered'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['https://store.steampowered.com/app']

    rules = (Rule(LinkExtractor(allow=('1284410/',)), callback='parse_item'),)

    custom_settings = {'ITEM_PIPELINES': {'api.steamscraper.pipeline.SteamPipeline': 100}}

    def parse_item(self, response: Response):
        #if 'Bandwidth exceeded' in response.body:
        #    raise CloseSpider('bandwidth_exceeded')

        item_loader = ItemLoader(ItemGame(), response=response)
        item_loader.add_css('name', '.apphub_AppName::text')
        item_loader.add_css('description', '.game_description_snippet::text')
        item_loader.add_css('developer', '#developers_list > a::text')

        SteamSpider._parse_requirements('.game_area_sys_req_rightCol', response, item_loader)
        SteamSpider._parse_requirements('.game_area_sys_req_leftCol', response, item_loader)
        return item_loader.load_item()

    @staticmethod
    def _parse_requirements(req_column_selector: str, response: Response, item_loader: ItemLoader):
        div_req_col = response.css(req_column_selector).get()
        if 'Minimum' in div_req_col:
            requirements = {'Memory': 'ram_min', 'Processor': 'cpu_min', 'Graphics': 'gpu_min', 'OS': 'OS_min',
                            'Storage': 'storage_min'}
            SteamSpider._parse_li(requirements, req_column_selector, response, item_loader)
        elif 'Recommended' in div_req_col:
            requirements = {'Memory': 'ram_rec', 'Processor': 'cpu_rec', 'Graphics': 'gpu_rec', 'OS': 'OS_rec',
                            'Storage': 'storage_rec'}
            SteamSpider._parse_li(requirements, req_column_selector, response, item_loader)
        else:
            print('No mininum or recommended?')

    @staticmethod
    def _parse_li(requirements: dict, req_column_selector: str, response: Response, item_loader: ItemLoader):
        reqs_li = response.css(f'{req_column_selector} .bb_ul > li').getall()
        req_keys = requirements.keys()
        for index, li in enumerate(reqs_li):
            for k in req_keys:
                if k in li:
                    #adds current li child if it's one of the requirements
                    print(f'{req_column_selector} li:nth-child{index+1}')
                    item_loader.add_css(requirements[k], f'{req_column_selector} li:nth-child({index+1})')


def parse_soup(li_item):
    soup = BeautifulSoup(li_item, 'html.parser')
    li_soup = soup.li
    try:
        soup.strong.extract()
        soup.br.extract()
    except AttributeError:
        print('There was no br or strong tag')
    return li_soup.string


class ItemGame(Item):
    name = Field()
    description = Field(output_processor=MapCompose(lambda des : des.strip('\r\t\n')))
    developer = Field()
    ram_min = Field(output_processor=MapCompose(parse_soup))
    cpu_min = Field(output_processor=MapCompose(parse_soup))
    gpu_min = Field(output_processor=MapCompose(parse_soup))
    OS_min = Field(output_processor=MapCompose(parse_soup))
    storage_min = Field(output_processor=MapCompose(parse_soup))
    ram_rec = Field(output_processor=MapCompose(parse_soup))
    cpu_rec = Field(output_processor=MapCompose(parse_soup))
    gpu_rec = Field(output_processor=MapCompose(parse_soup))
    OS_rec = Field(output_processor=MapCompose(parse_soup))
    storage_rec = Field(output_processor=MapCompose(parse_soup))