# Scrapy settings for immo_eliza_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "immo_eliza_scraper"

SPIDER_MODULES = ["immo_eliza_scraper.spiders"]
NEWSPIDER_MODULE = "immo_eliza_scraper.spiders"

ADDONS = {}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "immo_eliza_scraper (+http://www.yourdomain.com)"

# 1. Stop telling the site you are a Scrapy bot
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}

# 2. Be polite: Wait 3-5 seconds between every page
DOWNLOAD_DELAY = 1.5
DOWNLOAD_TIMEOUT = 15
RANDOMIZE_DOWNLOAD_DELAY = True
ALLOWED_DOMAINS = ['www.immovlan.be']

# 3. Disable the "I am a robot" flag
ROBOTSTXT_OBEY = False

# 4. Turn on AutoThrottle (Scrapy will slow down if the site gets stressed)
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0
AUTOTHROTTLE_MAX_DELAY = 60.0

# Obey robots.txt rules
#ROBOTSTXT_OBEY = True

# Concurrency and throttling settings
CONCURRENT_REQUESTS = 64
CONCURRENT_REQUESTS_PER_DOMAIN = 32
DOWNLOAD_DELAY = 1.5
RANDOMIZE_DOWNLOAD_DELAY = True

# Disable cookies (enabled by default)
COOKIES_ENABLED = False
LOG_FILE = 'logs/scraping_execution.log'
LOG_LEVEL = 'INFO'
RETRY_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "immo_eliza_scraper.middlewares.ImmoElizaScraperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "immo_eliza_scraper.middlewares.ImmoElizaScraperDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "immo_eliza_scraper.pipelines.ImmoElizaScraperPipeline": 300,
}


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 8.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"

# Path where you want to save the CSV
FEEDS = {
    '../data/immovlan_data.csv': {
        'format': 'csv',
        'encoding': 'utf8',
        'store_empty': False,
        'fields': None,  # Use None to export all fields yielded by the spider
        'indent': 4,
        'overwrite': True, # Set to False if you want to append data on every run
    }
}

# Optional: Define the order of columns in your CSV
FEED_EXPORT_FIELDS = [
    'locality', 'property_type', 'subtype', 'price', 'type_of_sale', 
    'nb_rooms', 'living_area', 'kitchen_equipped', 'furnished', 
    'open_fire', 'terrace', 'terrace_area', 'garden', 'garden_area', 
    'surface_land', 'plot_surface', 'facades', 'swimming_pool', 
    'building_state', 'url'
]
