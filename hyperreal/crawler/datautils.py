import os
import csv
from hyperreal.crawler.constants import *
from hyperreal.crawler.crawler_error import *


def create_data_csv(folder):
    """
    Create data.csv file from scrapped data and saves result in the given folder
    :param folder: folder with scrapped data: forums.csv, topics.csv, posts.csv
    """
    try:
        posts_file = open(os.path.join(folder, POSTS_FILE_NAME), 'r', encoding="utf-8")
        data_file = open(os.path.join(folder, DATA_FILE_NAME), 'w', encoding="utf-8", newline='')
        forums_dict = _load_element_dict(folder, FORUMS_FILE_NAME, FORUMS_FORMAT)
        topics_dict = _load_element_dict(folder, TOPICS_FILE_NAME, TOPICS_FORMAT)
    except OSError:
        raise CrawlerError

    with posts_file, data_file:
        _process_posts(data_file, posts_file, forums_dict, topics_dict)


def append_data_csv(folder):
    """
    Append newly scrapped data into existing data csv file
    :param folder: folder with scrapped and processed data: data.csv, forums.csv, forums_append.csv, topics.csv, topics_append.csv, posts.csv, posts_append.csv
    """
    try:
        data_file = open(os.path.join(folder, DATA_FILE_NAME), 'r', encoding="utf-8")
        forums_dict = _load_element_dict(folder, FORUMS_FILE_NAME, FORUMS_FORMAT)
        topics_dict = _load_element_dict(folder, TOPICS_FILE_NAME, TOPICS_FORMAT)
        forums_append_file = open(os.path.join(folder, FORUMS_TO_APPEND_FILE_NAME), 'r', encoding="utf-8")
        topics_append_file = open(os.path.join(folder, TOPICS_TO_APPEND_FILE_NAME), 'r', encoding="utf-8")
        posts_append_file = open(os.path.join(folder, POSTS_TO_APPEND_FILE_NAME), 'r', encoding="utf-8")
    except OSError:
        raise CrawlerError

    with forums_append_file, topics_append_file:
        _append_element_dict(forums_dict, forums_append_file, FORUMS_FORMAT)
        _append_element_dict(topics_dict, topics_append_file, TOPICS_FORMAT)

    with data_file:
        posts_keys = _load_post_keys(data_file)

    with posts_append_file, open(os.path.join(folder, DATA_FILE_NAME), 'a', encoding='utf-8', newline='') as data_file:
        _append_posts(posts_append_file, posts_keys, forums_dict, topics_dict, data_file)


def _load_element_dict(folder_name, file_name, element_format):
    with open(os.path.join(folder_name, file_name), 'r', encoding="utf-8") as file:
        return _create_element_dict(file, element_format)


def _create_element(row, element_format):
    element = {}
    for key in element_format.keys():
        element[key] = row[element_format[key]]
    return element


def _create_element_dict(file, element_format):
    csv_reader = csv.reader(file)
    csv_dict = {}
    for row in csv_reader:
        csv_dict[row[element_format["id"]]] = _create_element(row, element_format)
    return csv_dict


def _append_element_dict(current_dict, file, element_format):
    csv_reader = csv.reader(file)
    for row in csv_reader:
        element = _create_element(row, element_format)
        if not element['id'] in current_dict:
            current_dict[element['id']] = element


def _get_topic(p, topics_dict):
    if p[POSTS_FORMAT['thread_id']] not in topics_dict:
        return None
    return topics_dict[p[POSTS_FORMAT['thread_id']]]


def _get_forum(p, forums_dict, topics_dict):
    topic = _get_topic(p, topics_dict)
    if topic is None or topic['forum_id'] not in forums_dict:
        return None
    return forums_dict[topic['forum_id']]


def _create_data_line(post, topic, forum):
    data_line = [None] * 9
    data_line[DATA_FORMAT["post_id"]] = post[POSTS_FORMAT["post_id"]]
    data_line[DATA_FORMAT["thread_id"]] = post[POSTS_FORMAT["thread_id"]]
    data_line[DATA_FORMAT["post_number"]] = post[POSTS_FORMAT["post_number"]]
    data_line[DATA_FORMAT["author"]] = post[POSTS_FORMAT["username"]]
    data_line[DATA_FORMAT["content"]] = post[POSTS_FORMAT["content"]]
    data_line[DATA_FORMAT["date"]] = post[POSTS_FORMAT["date"]]
    data_line[DATA_FORMAT["forum_id"]] = topic["forum_id"]
    data_line[DATA_FORMAT["forum_link"]] = forum["link"]
    data_line[DATA_FORMAT["thread_name"]] = topic["name"]
    return data_line


def _process_posts(data_file, posts_file, forums_dict, topics_dict):
    csv_writer = csv.writer(data_file)
    csv_post_reader = csv.reader(posts_file)

    # write file header
    csv_writer.writerow(_create_csv_header(DATA_FORMAT))

    for post in csv_post_reader:
        topic = _get_topic(post, topics_dict)
        forum = _get_forum(post, forums_dict, topics_dict)

        if topic is None or forum is None:
            # TODO investigate how can this happen
            continue

        csv_writer.writerow(_create_data_line(post, topic, forum))


def _load_post_keys(data_file):
    csv_reader = csv.reader(data_file)
    posts = {}
    for row in csv_reader:
        posts[row[DATA_FORMAT['post_id']]] = True
    return posts


def _append_posts(posts_file, posts_keys, forums_dict, topics_dict, data_file):
    csv_post_reader = csv.reader(posts_file)
    csv_writer = csv.writer(data_file)
    for post in csv_post_reader:
        post_id = post[POSTS_FORMAT["post_id"]]
        if post_id in posts_keys:
            continue
        topic = _get_topic(post, topics_dict)
        forum = _get_forum(post, forums_dict, topics_dict)

        if topic is None or forum is None:
            # TODO investigate how can this happen
            continue

        csv_writer.writerow(_create_data_line(post, topic, forum))


def _create_csv_header(element_format):
    header = [None] * (len(element_format))

    for key in element_format.keys():
        header[element_format[key]] = key

    return header
