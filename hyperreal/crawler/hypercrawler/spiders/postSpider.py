import scrapy
from scrapy.loader import ItemLoader
from hyperreal.crawler.hypercrawler.items import *


class PostSpider(scrapy.Spider):
    """
    Scrapy spider. Crawls hyperreal.info forum and extracts subforum names, thread names and post contents
    """
    name = "posts"

    allowed_domains = ["hyperreal.info"]
    start_urls = ["https://hyperreal.info/talk/"]

    def parse(self, response):
        """
        Default scrapy callback. To be used on forum main page.
        Follows subforum links.

        :param response: scrapy crawl resposne
        :returns :class:`hyperreal.crawler.hypercrawler.items.PostItem`,
        :class:`hyperreal.crawler.hypercrawler.items.ForumItem`, :class:`hypercrawler.items.TopicItem`
        """
        subforums = response.css('a.forumtitle::attr(href)').getall()
        for forum in subforums:
            next_request = response.urljoin(forum)
            yield scrapy.Request(next_request, callback=self.parse_forum)

    def parse_forum(self, response):
        """
        Forum callback. Parses ForumItem.
        Follows subforum links and thread links (through self.parse_forum_page() method).
        :param response: scrapy crawl response
        """
        forum_loader = ItemLoader(item=ForumItem(), response=response)
        forum_loader.add_value('link', response.request.url)
        forum_loader.add_css('name', 'h2 > a::text')
        yield forum_loader.load_item()

        subforums = response.css('a.forumtitle::attr(href)').getall()
        for forum in subforums:
            next_request = response.urljoin(forum)
            yield scrapy.Request(next_request, callback=self.parse_forum)

        yield from self.parse_forum_page(response)

    def parse_forum_page(self, response):
        """
        Forum page callback. Parses TopicItem.
        Follows next forum page and threads.
        :param response: scrapy crawl response
        """
        next_page = response.css('a[rel=next]::attr(href)').get()
        if next_page:
            next_request = response.urljoin(next_page)
            yield scrapy.Request(next_request, callback=self.parse_forum_page)

        threads = response.css('a.topictitle')
        for thread in threads:
            topic_loader = ItemLoader(item=TopicItem(), response=response)
            thread_href_selector = thread.css('a::attr(href)')
            thread_link = response.urljoin(thread_href_selector.get())
            topic_loader.add_value('id', thread_href_selector.re(r'-(t[0-9]*).html'))
            topic_loader.add_value('link', thread_link)
            topic_loader.add_value('name', thread.css('a::text').get())
            yield topic_loader.load_item()
            yield scrapy.Request(thread_link, callback=self.parse_thread)

    def parse_thread(self, response):
        """
        Thread page callback. Parses PostItem.
        Follows next thread page.
        :param response: scrapy crawl response
        """
        next_page = response.css('a[rel=next]::attr(href)').get()
        if next_page:
            next_request = response.urljoin(next_page)
            yield scrapy.Request(next_request, callback=self.parse_thread)

        posts = response.css('div.post.panel-body')
        post_number = 1
        for post in posts:
            post_loader = ItemLoader(item=PostItem(), selector=post)
            post_loader.add_value('username', post.css('a.username-coloured::text,a.username::text').get())
            post_loader.add_value('date', post.css('div.post-date::text')[1].get()[3:-1])
            post_loader.add_value('post_id', post.css('div.post-date > a::attr(href)').re(r'.html#(.*)'))
            post_loader.add_value('thread_url', response.request.url)
            post_loader.add_value('post_number', post_number)
            post_number += 1
            post_loader.add_value('content', post.css('div.content').get())
            yield post_loader.load_item()
