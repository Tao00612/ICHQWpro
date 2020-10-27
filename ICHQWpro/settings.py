
BOT_NAME = 'ICHQWpro'

SPIDER_MODULES = ['ICHQWpro.spiders']
NEWSPIDER_MODULE = 'ICHQWpro.spiders'


USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3'
ROBOTSTXT_OBEY = False
LOG_LEVEL = 'ERROR'


# DOWNLOAD_DELAY = 0.01



DOWNLOADER_MIDDLEWARES = {
   'ICHQWpro.middlewares.CookieMiddleware': 543,
   'ICHQWpro.middlewares.RandomUserAgent': 542,
   'ICHQWpro.middlewares.RandomProxy': 541,
}

ITEM_PIPELINES = {
   'ICHQWpro.pipelines.Pipeline': 300,
}


