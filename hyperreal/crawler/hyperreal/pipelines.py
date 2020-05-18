from hyperreal.items import *
import csv
import re
import w3lib.html


class HyperrealPipeline:

    def open_spider(self, start_requests):
        """
        Called during spider startup. Opens and truncates output files and prepares csv writers.
        :param start_requests: Starting requests for the spider
        """
        self.forum_file = open('forums.csv', 'w', newline='', encoding='utf-8')
        self.topic_file = open('topics.csv', 'w', newline='', encoding='utf-8')
        self.post_file = open('posts.csv', 'w', newline='', encoding='utf-8')

        self.forum_writer = csv.writer(self.forum_file)
        self.topic_writer = csv.writer(self.topic_file)
        self.post_writer = csv.writer(self.post_file)

    def close_spider(self, spider):
        """
        Called when spider finishes work. Closes output files
        :param spider: Spider, which finished it's work
        """
        self.forum_file.close()
        self.topic_file.close()
        self.post_file.close()

    def process_item(self, item, spider):
        """
        Processes scraped item and saves it in a output file accordingly
        :param item: Item to process. Might be a :class:`hyperreal.items.PostItem`,
        :class:`hyperreal.items.ForumItem` or :class:`hyperreal.items.TopicItem`
        :param spider: a spider
        """
        if isinstance(item, ForumItem):
            return self.handle_forum(item)
        if isinstance(item, TopicItem):
            return self.handle_topic(item)
        if isinstance(item, PostItem):
            return self.handle_post(item)
        return item

    def handle_forum(self, item):
        """
        Process ForumItem and save it to the output file
        :param item: ForumItem to process
        """
        self.forum_writer.writerow([item['link'][0], item['name'][0]])
        return item

    def handle_topic(self, item):
        """
        Process TopicItem and save it to the output file
        :param item: TopicItem to process
        """
        self.topic_writer.writerow([item['id'][0], item['link'][0], item['name'][0]])
        return item

    def handle_post(self, item):
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
