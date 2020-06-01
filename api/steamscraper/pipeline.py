from scrapy.exceptions import DropItem


class SteamPipeline:

    def process_items(self, item, spider):
        if item.get('name'):
            print(item['name'])
            return item
        else:
            raise DropItem('Missing game name in %s', item)

