from hyperreal.crawler.hypercrawler.items import *
import csv
import re
import w3lib.html
import os
from hyperreal.crawler.constants import *
import scrapy
import typing


class HyperrealPipeline:

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings.get('OUTPUT_DIRECTORY'), settings.get('START_DATE'))

    def __init__(self, output_directory, start_date):
        self.output_directory = output_directory
        self.start_date = start_date

    def open_spider(self, _) -> None:
        """
        Called during spider startup. Opens and truncates output files and prepares csv writers.
        """

        def open_output_file(file_name: str) -> typing.IO:
            return open(os.path.join(self.output_directory, file_name), 'w', newline='', encoding='utf-8')

        if self.start_date is None:
            self.forum_file = open_output_file(FORUMS_FILE_NAME)
            self.topic_file = open_output_file(TOPICS_FILE_NAME)
            self.post_file = open_output_file(POSTS_FILE_NAME)
        else:
            self.forum_file = open_output_file(FORUMS_TO_APPEND_FILE_NAME)
            self.topic_file = open_output_file(TOPICS_TO_APPEND_FILE_NAME)
            self.post_file = open_output_file(POSTS_TO_APPEND_FILE_NAME)

        self.forum_writer = csv.writer(self.forum_file)
        self.topic_writer = csv.writer(self.topic_file)
        self.post_writer = csv.writer(self.post_file)

    def close_spider(self) -> None:
        """
        Called when spider finishes work. Closes output files
        :param spider: Spider, which finished it's work
        """
        self.forum_file.close()
        self.topic_file.close()
        self.post_file.close()

    def process_item(self, item: scrapy.Item, _) -> scrapy.Item:
        """
        Processes scraped item and saves it in a output file accordingly
        :param item: Item to process. Might be a :class:`hyperreal.crawler.hypercrawler.items.PostItem`,
        :class:`hyperreal.crawler.hypercrawler.items.ForumItem` or :class:`hypercrawler.items.TopicItem`
        """
        if isinstance(item, ForumItem):
            return self.handle_forum(item)
        if isinstance(item, TopicItem):
            return self.handle_topic(item)
        if isinstance(item, PostItem):
            return self.handle_post(item)
        return item

    def handle_forum(self, item: scrapy.Item) -> scrapy.Item:
        """
        Process ForumItem and save it to the output file
        :param item: ForumItem to process
        """
        link = item['link'][0]

        forum_id_match = re.compile(r'.*/talk/(.*)\.html$').match(link)
        if forum_id_match is not None:
            self.forum_writer.writerow([link, item['name'][0], forum_id_match.group(1)])
        return item

    def handle_topic(self, item: scrapy.Item) -> scrapy.Item:
        """
        Process TopicItem and save it to the output file
        :param item: TopicItem to process
        """
        forum_id_match = re.compile(r'.*/talk/(.*)\.html$').match(item['forum_link'][0])
        if forum_id_match is not None:
            self.topic_writer.writerow(
                [item['id'][0], forum_id_match.group(1), item['thread_link'][0], item['name'][0]])
        return item

    def handle_post(self, item: scrapy.Item) -> scrapy.Item:
        """
        Process PostItem and save it to the output file
        :param item: PostItem
        """
        thread_url = item['thread_url'][0]
        res = re.compile(r'-t[0-9]*-([0-9]*)\.html').findall(thread_url)
        post_number = item['post_number'][0]
        if res:
            post_number += int(res[-1])

        thread_id = re.compile(r'.*-(t[0-9]*)(-[0-9]*)?\.html').match(thread_url).group(1)

        self.post_writer.writerow([
            item['post_id'][0],
            thread_id,
            post_number,
            item['username'][0],
            w3lib.html.remove_tags(item['content'][0]),
            item['date'][0]
        ])
        return item
