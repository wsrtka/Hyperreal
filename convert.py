import csv
from hyperreal.crawler.constants import POSTS_FORMAT
from hyperreal.crawler.dateutil import parse_date

with open('posts.csv', 'r', encoding='utf-8') as posts_file, open('posts2.csv', 'w', encoding='utf-8',
                                                                  newline='') as posts_file2:
    reader = csv.reader(posts_file)
    writer = csv.writer(posts_file2)

    counter = 0
    for post in reader:
        if post[POSTS_FORMAT['date']] == '':
            counter += 1
            print('skipping post ' + post[POSTS_FORMAT['id']])
            continue
        post[POSTS_FORMAT['date']] = parse_date(post[POSTS_FORMAT['date']])
        writer.writerow(post)
    print(counter)
