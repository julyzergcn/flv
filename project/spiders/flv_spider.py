import re
import urllib
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from project.items import FlvItem, FlvItemLoader
from project.settings import *

def _url(url):
    base_url = 'http://www.flvcd.com/parse.php?flag=&format=&kw='
    if url.startswith(base_url):
        return urllib.unquote_plus(url[len(base_url):])
    else:
        return base_url + urllib.quote_plus(url.encode('utf8'))

class FlvSpider(BaseSpider):
    name = 'flv'
    allowed_domains = (
        'youku.com',
    )
    
    start_urls = []
    for line in open(join(BASE_DIR, 'urls.txt')):
        start_urls.append(_url(line.strip()))
    
    def parse(self, response):
        loader = FlvItemLoader(FlvItem(), response=response)
        loader.add_value('url', _url(response.url))
        loader.add_xpath('title', '//table[1]/tr[4]//table[1]/tr/td/text()')
        loader.add_xpath('flv_urls', '//table[1]/tr[4]//table[2]/tr[1]/td[1]/a/@href')
        return loader.load_item()
