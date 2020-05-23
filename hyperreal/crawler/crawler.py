from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
import os


def start_full_crawl(output_directory):
    settings = Settings()
    settings_module = 'hyperreal.crawler.hypercrawler.settings'
    os.environ['SCRAPY_SETTINGS_MODULE'] = settings_module
    settings.setmodule(settings_module, priority='project')
    settings.set('OUTPUT_DIRECTORY', output_directory)
    settings.set('START_DATE', None)

    process = CrawlerProcess(settings)
    process.crawl('posts')
    process.start()


def start_append_crawl(output_directory, date):
    settings = Settings()
    settings_module = 'hyperreal.crawler.hypercrawler.settings'
    os.environ['SCRAPY_SETTINGS_MODULE'] = settings_module
    settings.setmodule(settings_module, priority='project')
    settings.set('OUTPUT_DIRECTORY', output_directory)
    settings.set('START_DATE', date)

    process = CrawlerProcess(settings)
    process.crawl('posts')
    process.start()
