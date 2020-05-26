from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
import os
import multiprocessing as mp


def start_full_crawl(output_directory):
    p = mp.Process(target=_exec_full_crawl, args=output_directory)
    p.start()
    p.join()


def start_append_crawl(output_directory, date):
    p = mp.Process(target=_exec_append_crawl, args=(output_directory, date))
    p.start()
    p.join()


def _exec_full_crawl(output_dir):
    settings = Settings()
    settings_module = 'hyperreal.crawler.hypercrawler.settings'
    os.environ['SCRAPY_SETTINGS_MODULE'] = settings_module
    settings.setmodule(settings_module, priority='project')
    settings.set('OUTPUT_DIRECTORY', output_dir)
    settings.set('START_DATE', None)

    process = CrawlerProcess(settings)
    process.crawl('posts')
    process.start()


def _exec_append_crawl(output_dir, date):
    settings = Settings()
    settings_module = 'hyperreal.crawler.hypercrawler.settings'
    os.environ['SCRAPY_SETTINGS_MODULE'] = settings_module
    settings.setmodule(settings_module, priority='project')
    settings.set('OUTPUT_DIRECTORY', output_dir)
    settings.set('START_DATE', date)

    process = CrawlerProcess(settings)
    process.crawl('posts')
    process.start()
