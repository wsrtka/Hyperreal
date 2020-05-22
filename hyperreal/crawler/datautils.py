import os
import csv
from hyperreal.crawler.constants import *
from hyperreal.crawler.crawler_error import *


def create_data_csv(folder):
    try:
        forums_file = open(os.path.join(folder, FORUMS_FILE_NAME), 'r', encoding="utf-8")
        topics_file = open(os.path.join(folder, TOPICS_FILE_NAME), 'r', encoding="utf-8")
        posts_file = open(os.path.join(folder, POSTS_FILE_NAME), 'r', encoding="utf-8")
        data_file = open(os.path.join(folder, DATA_FILE_NAME), 'w', encoding="utf-8", newline='')
    except OSError:
        raise CrawlerError

    with forums_file:
        forums_dict = _create_element_dict(forums_file, FORUMS_FORMAT)

    with topics_file:
        topics_dict = _create_element_dict(topics_file, TOPICS_FORMAT)

    with posts_file, data_file:
        _process_posts(data_file, posts_file, forums_dict, topics_dict)


def append_data_csv(folder):
    # TODO implement
    pass


def _create_element_dict(forums_file, element_format):
    csv_reader = csv.reader(forums_file)
    csv_dict = {}
    for row in csv_reader:
        element = {}
        for key in element_format.keys():
            element[key] = row[element_format[key]]
        csv_dict[row[element_format["id"]]] = element
    return csv_dict


def _process_posts(data_file, posts_file, forums_dict, topics_dict):
    csv_writer = csv.writer(data_file)
    csv_post_reader = csv.reader(posts_file)

    def get_topic(p):
        if p[POSTS_FORMAT['thread_id']] not in topics_dict:
            return None
        return topics_dict[p[POSTS_FORMAT['thread_id']]]

    def get_forum(p):
        if get_topic(p) is None or get_topic(p)['forum_id'] not in forums_dict:
            return None
        return forums_dict[get_topic(p)['forum_id']]

    for post in csv_post_reader:
        topic = get_topic(post)
        forum = get_forum(post)

        if topic is None or forum is None:
            # TODO investigate how can this happen
            continue

        data_line = [None] * 9
        data_line[DATA_FORMAT["post_id"]] = post[POSTS_FORMAT["post_id"]]
        data_line[DATA_FORMAT["thread_id"]] = post[POSTS_FORMAT["thread_id"]]
        data_line[DATA_FORMAT["post_number"]] = post[POSTS_FORMAT["post_number"]]
        data_line[DATA_FORMAT["username"]] = post[POSTS_FORMAT["username"]]
        data_line[DATA_FORMAT["content"]] = post[POSTS_FORMAT["content"]]
        data_line[DATA_FORMAT["date"]] = post[POSTS_FORMAT["date"]]
        data_line[DATA_FORMAT["forum_id"]] = topic["forum_id"]
        data_line[DATA_FORMAT["forum_link"]] = forum["link"]
        data_line[DATA_FORMAT["thread_name"]] = topic["name"]

        csv_writer.writerow(data_line)
