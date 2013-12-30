
from scrapy.item import Item, Field
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.contrib.loader.processor import Identity
from scrapy.contrib.loader.processor import Compose

class FlvItem(Item):
    title = Field()
    url = Field()
    flv_urls = Field()

def _title(value, context=None):
    return ''.join(i.strip() for i in value if i.strip())

class FlvItemLoader(XPathItemLoader):
    default_output_processor = TakeFirst()
    
    title_out = Compose(_title)
    flv_urls_out = Identity()
