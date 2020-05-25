FORUMS_FILE_NAME = "forums.csv"
TOPICS_FILE_NAME = "topics.csv"
POSTS_FILE_NAME = "posts.csv"
DATA_FILE_NAME = "data.csv"

FORUMS_TO_APPEND_FILE_NAME = "forums_append.csv"
TOPICS_TO_APPEND_FILE_NAME = "topics_append.csv"
POSTS_TO_APPEND_FILE_NAME = "posts_append.csv"

FORUMS_FORMAT = {
    "link": 0,
    "name": 1,
    "forum_id": 2,
    "id": 2
}

TOPICS_FORMAT = {
    "topic_id": 0,
    "forum_id": 1,
    "link": 2,
    "name": 3,
    "id": 0
}

POSTS_FORMAT = {
    "post_id": 0,
    "thread_id": 1,
    "post_number": 2,
    "username": 3,
    "content": 4,
    "date": 5,
    "id": 0
}

DATA_FORMAT = {
    "post_id": 0,
    "thread_id": 1,
    "post_number": 2,
    "author": 3,
    "content": 4,
    "date": 5,
    "forum_id": 6,
    "forum_link": 7,
    "thread_name": 8
}
