import os
from os.path import join, abspath, dirname

BASE_DIR = dirname(dirname(abspath(__file__)))

BOT_NAME = 'project'
USER_AGENT = 'Mozilla/5.0'

#~ LOG_ENABLED = True
LOG_ENABLED = False

SPIDER_MODULES = ['project.spiders']
NEWSPIDER_MODULE = 'project.spiders'

ITEM_PIPELINES = (
    'project.pipelines.FlvPipeline',
)

#~ IMAGES_STORE = join(BASE_DIR, 'flvs')
IMAGES_STORE = join(BASE_DIR, '..')
