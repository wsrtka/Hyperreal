from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
import os
import multiprocessing as mp
from threading import Thread
from hyperreal.crawler.datautils import create_data_csv, append_data_csv
from hyperreal.gui.events import CrawlerDoneEvent
import wx
import time
import datetime


class CrawlerThread:
    def __init__(self, process, append, output_directory, notify):
        self.thread = _CrawlerThread()
        self.thread.process = process
        self.thread.append = append
        self.thread.wants_abort = False
        self.thread.output_directory = output_directory
        self.thread.notify = notify

    def abort(self):
        """
        Abort current crawl
        """
        self.thread.wants_abort = True

    def start(self):
        """
        Begin crawl
        :return:
        """
        self.thread.start()

    def is_alive(self):
        return self.thread.is_alive()


def start_full_crawl(output_directory: str, notify_window: wx.EvtHandler) -> CrawlerThread:
    """
    Delete stored data and crawl entire hyperreal.info forum
    :param output_directory: path to output directory
    :param notify_window: xwPython window to notify when finished
    :return: crawler thread
    """
    p = mp.Process(target=_exec_full_crawl, args=output_directory)
    return CrawlerThread(p, False, output_directory, notify_window)


def start_append_crawl(output_directory: str, date: datetime.date, notify_window: wx.EvtHandler) -> CrawlerThread:
    """
    Crawl posts from hyperreal.info forum created after given date
    :param output_directory: path to the output directory
    :param date: date, after which
    :param notify_window: xwPython window to notify when finished
    :return:
    """
    p = mp.Process(target=_exec_append_crawl, args=(output_directory, date))
    return CrawlerThread(p, False, output_directory, notify_window)


def _exec_full_crawl(output_dir: str) -> None:
    settings = Settings()
    settings_module = 'hyperreal.crawler.hypercrawler.settings'
    os.environ['SCRAPY_SETTINGS_MODULE'] = settings_module
    settings.setmodule(settings_module, priority='project')
    settings.set('OUTPUT_DIRECTORY', output_dir)
    settings.set('START_DATE', None)

    process = CrawlerProcess(settings)
    process.crawl('posts')
    process.start()


def _exec_append_crawl(output_dir: str, date: datetime.date) -> None:
    settings = Settings()
    settings_module = 'hyperreal.crawler.hypercrawler.settings'
    os.environ['SCRAPY_SETTINGS_MODULE'] = settings_module
    settings.setmodule(settings_module, priority='project')
    settings.set('OUTPUT_DIRECTORY', output_dir)
    settings.set('START_DATE', date)

    process = CrawlerProcess(settings)
    process.crawl('posts')
    process.start()
    wx.Abort()


class _CrawlerThread(Thread):
    def run(self):
        self.process.start()
        while self.process.is_alive():
            time.sleep(1)
            if self.wants_abort:
                self.process.terminate()

        if not self.wants_abort:
            if self.append:
                append_data_csv(self.output_directory)
            else:
                create_data_csv(self.output_directory)

        wx.PostEvent(self.notify, CrawlerDoneEvent(self.wants_abort))
