import numpy as np
from termcolor import colored
import pandas as pd


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
def get_most_active_authors(df, top=10):
    """
    Get the top most active authors ready to plot.
    :param df: dataframe containing posts with author information
    :param top: int number of top authors to plot
    :return: object ready to plot
    """
    # to apply: .plot.barh( );
    return df.groupby('author').count()['post_id'].sort_values(ascending=False)[:top]


def show_crawled_forums(df):
    """
    Show the ids of forums already crawled.
    :param df: Dataframe containing posts with their forum ids
    :return: print the crawled forum ids in green, uncrawled in red
    """
    forum_ids = df['forum_id'].unique().astype(np.int32)

    for fid in range(1, max(forum_ids) + 1):
        if fid in forum_ids:
            print(colored(fid, on_color='on_green'), end=' ')
        else:
            print(colored(fid, on_color='on_red'), end=' ')


# TODO: Uogólnić?
def get_total_posts(posts, forums):
    """
    Get an object to plot the total posts count per forum.
    :param posts: dataframe containing post data
    :param forums: dataframe containing forum data
    :return: object ready to plot the totals posts count
    """
    tmp = forums[['id', 'name']]
    tmp.columns = ['id', 'forum_name']
    posts = pd.merge(posts, tmp, left_on='forum_id', right_on='id')

    by_forum = posts.groupby('forum_name').size()
    by_forum = by_forum.reset_index()
    by_forum.columns = ['forum_name', 'count']
    by_forum = by_forum.sort_values(by='count', ascending=False)

    # g = sns.catplot(x="forum_name", y="count", data=by_forum, aspect=5, hue='count', legend=False)
    # g.set_xticklabels(rotation=90)

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

    forum_name = forums[forums['id'] == forum_id]['name'].values[0]

    # to apply:
    # sns.set_style("whitegrid")
    # g = sns.relplot(x='date', y='post_count', hue='post_count', aspect=2, data=X);
    # g.fig.autofmt_xdate()
    # g.ax.set_title(forum_name)

    return time, forum_name


# TODO: add function to display above function result data in grid
