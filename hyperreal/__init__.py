"""
**posts.csv (~750Mb)** \
Information on posts and their content.

Schema:
- post_id: string
- thread_id: string
- idx: int
- author: string
- content: string

**forums.csv (14Kb)** \
Forum & subforum information.
- id: string
- is_main: bool
- url: string
- name: string

**topics.csv (~1.5Mb)** \
Information on which thread belongs to which forums.

Schema:
- thread_id: string
- forum_id: string
- url: string
- name: string


**data.csv (~850Mb)** \
Posts from posts.csv merged with forum information from topics.csv.

Schema:
- post_id: string
- thread_id: string
- idx: int
- author: string
- content: string
- date: string
- forum_id: string
- url: string
- name: string

**narkopedia.json (~240Kb)** \
Information on most popular drugs and substances crawled from narkopedia (https://hyperreal.info/narkopedia/Specjalna:Wszystkie_strony).

Schema:
- name: string
- url: string
- other-forms: list(string) (Odmiany nazwy substancji)
- other-names: list(string) (Inne nazwy substancji)
- generic-names: list(string) (Nazwa generyczna)
"""
