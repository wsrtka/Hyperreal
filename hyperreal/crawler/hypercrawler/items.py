import scrapy


class ForumItem(scrapy.Item):
    """
    Represents a subforum
    """
    link = scrapy.Field()
    name = scrapy.Field()


class TopicItem(scrapy.Item):
    """
    Represents a forum thread
    """
    id = scrapy.Field()
    thread_link = scrapy.Field()
    forum_link = scrapy.Field()
    name = scrapy.Field()


class PostItem(scrapy.Item):
    """
    Represents a single post
    """
    username = scrapy.Field()
    post_id = scrapy.Field()
    thread_url = scrapy.Field()
    content = scrapy.Field()
    post_number = scrapy.Field()
    date = scrapy.Field()
