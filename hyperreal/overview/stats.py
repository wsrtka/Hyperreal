import wordcloud as WordCloud
import numpy as np
from termcolor import colored
import pandas as pd
import matplotlib.pyplot as plt

from hyperreal.textutils.ngrams import ngrams_describing_drug


def show_count(label, column, df):
    """
    Show the count of unique values in column.
    :param df: dataframe containing data of interest
    :param label: string label for describing the data
    :param column: string name of the column to describe
    :return: print the amount of unique values in column
    """
    print('{0:10}: {1}'.format(label, len(df[column].unique())))


# TODO: Uogólnić?
def get_posts_per_year(df):
    """
    Get an object ready to plot the number of posts per year.
    :param df: dataframe containing posts
    :return: object ready to plot
    """
    # to apply: plot('bar');
    return df['date'].groupby([df.date.dt.year]).agg('count')


# TODO: Uogolnić?
def get_most_active_authors(df, top=10, forum=None):
    """
    Get the top most active authors ready to plot.
    :param df: dataframe containing posts with author information
    :param top: int number of top authors to plot
    :param forum: string containing forum name
    :return: object ready to plot
    """
    # to apply: .plot.barh( );
    if forum is not None:
        df = df[df['name'] == forum]

    return df.groupby('author').count()['post_id'].sort_values(ascending=False)[:top]


def show_crawled_forums(df):
    """
    Show the ids of forums already crawled.
    :param df: Dataframe containing posts with their forum ids
    :return: print the crawled forum ids in green, uncrawled in red
    """
    forum_ids = df['forum_id'].unique()

    for fid in range(1, max(forum_ids.count()) + 1):
        if fid in forum_ids:
            print(colored(fid, on_color='on_green'), end=' ')
        else:
            print(colored(fid, on_color='on_red'), end=' ')


# TODO: Uogólnić?
def get_total_posts(df, forum_name_col="forum_id"):
    """
    Get an object to plot the total posts count per forum.
    :param forum_name_col: string name of column containing forum name
    :param df: dataframe containing data
    :return: object ready to plot the totals posts count
    """
    # tmp = forums[['id', 'name']]
    # tmp.columns = ['id', 'forum_name']
    # posts = pd.merge(posts, tmp, left_on='forum_id', right_on='id')

    by_forum = df.groupby(forum_name_col).size()
    by_forum = by_forum.reset_index()
    by_forum.columns = [forum_name_col, 'count']
    by_forum = by_forum.sort_values(by='count', ascending=False)

    return by_forum


def get_forum_popularity(forums, forum_id):
    """
    Get the data needed to plot forum popularity across time
    :param forums: dataframe containing forum data prepared by the get_total_posts() function
    :param forum_id: int number with the forum id to plot
    :return: dataframe with the posts count per month, string containing forum name
    """
    time = forums[forums['forum_id'] == forum_id].set_index('date')
    time = time.groupby(pd.Grouper(freq="M")).size()
    time = time.reset_index()
    time.columns = ['date', 'post_count']

    forum_name = forums[forums['forum_id'] == forum_id]['forum_id'].values[0]

    return time, forum_name


# TODO: add function to display above function result data in grid

def show_word_cloud(drug, raw_docs, narkopedia_map, doc_freq, filter_numeric=True, length=1, top=100):
    """
    Shows word cloud of ngrams associated with given drug.
    :param drug: string containing drug name
    :param raw_docs: list of strings containing texts for analysis
    :param narkopedia_map: dictionary of drug names and their alternative forms
    :param doc_freq: dictionary containing ngrams and number of docs in which they appeared
    :param filter_numeric: boolean, True if drug ngrams should not contain numbers
    :param length: int length of ngrams to create
    :param top: int number of top ngrams to use
    :return: print word cloud of ngrams associated with drug
    """
    fig, axes = plt.subplots(3, 2, figsize=(25, 18))

    for i, metric in enumerate(["tf", "tfidf"]):
        for j, n in enumerate([1, 2, 3]):
            top_ngrams = ngrams_describing_drug(
                narkopedia_map[drug],
                raw_docs,
                doc_freq[n],
                filter_numeric=filter_numeric,
                length=length,
                top=top,
                metric=metric
            )

            text_scores = {" ".join(k): v for k, v in top_ngrams}

            wc = WordCloud(height=400, width=800)
            wc.generate_from_frequencies(text_scores)

            axes[j, i].imshow(wc)

    plt.tight_layout()
    plt.show()
