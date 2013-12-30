import hashlib
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy import log
from scrapy.http import Request
from project.settings import *

class FlvError(Exception):
    pass

class FlvPipeline(ImagesPipeline):
    
    def open_spider(self, spider):
        print '-- starting spider'
        super(FlvPipeline, self).open_spider(spider)
    
    def close_spider(self, spider):
        print '-- closing spider'
    
    def process_item(self, item, spider):
        print '--', item.get('url', '')
        print '--', item.get('title', '')
        self.item = item
        return super(FlvPipeline, self).process_item(item, spider)
    
    def get_media_requests(self, item, info):
        return [Request(x) for x in item.get('flv_urls', [])]
    
    def media_downloaded(self, response, request, info):
        referer = request.headers.get('Referer')

        if response.status != 200:
            log.msg(format='Flv (code: %(status)s): Error downloading flv from %(request)s referred in <%(referer)s>',
                    level=log.WARNING, spider=info.spider,
                    status=response.status, request=request, referer=referer)
            raise FlvError('download-error')

        if not response.body:
            log.msg(format='Flv (empty-content): Empty flv from %(request)s referred in <%(referer)s>: no-content',
                    level=log.WARNING, spider=info.spider,
                    request=request, referer=referer)
            raise FlvError('empty-content')

        status = 'cached' if 'cached' in response.flags else 'downloaded'
        log.msg(format='Flv (%(status)s): Downloaded flv from %(request)s referred in <%(referer)s>',
                level=log.DEBUG, spider=info.spider,
                status=status, request=request, referer=referer)
        self.inc_stats(info.spider, status)
        
        # write to disk
        checksum = hashlib.md5(request.url).hexdigest()
        
        path = self.item.get('title', '')
        
        abs_path = join(IMAGES_STORE, path)
        if not os.path.exists(abs_path):
            os.makedirs(abs_path)
        
        fname = os.path.basename(response.url)
        if not fname.endswith('.flv'):
            fname += '.flv'
        
        print '--', fname
        
        fd = open(join(abs_path, fname), 'wb')
        try:
            fd.write(response.body)
        finally:
            try:
                fd.close()
            except: pass
        
        return {'url': request.url, 'path': path, 'checksum': checksum}
