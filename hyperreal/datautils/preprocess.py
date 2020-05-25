import pandas as pd

from hyperreal.textutils.cleaning import normalize_date


def data_pre(data, save=False, name="data-clean.csv", date_col="date", content_col="content", fill=" "):
    """
    Preprocess data merged from topics and posts. Data must have date and content columns.
    :param fill: string containing character to fill missing data with
    :param content_col: string containing content column name
    :param date_col: string containing date column name
    :param name: string containing name of file to save data to
    :param save: boolean, True if data is to be saved to file
    :param data: dataframe containing merged data
    :return: dataframe containing preprocessed data
    """
    data[date_col] = pd.to_datetime(data[date_col])
    data = data.dropna(subset=[content_col])
    data = data.fillna(fill)

    if save:
        data.to_csv(name, index=False)

    return data


def threads_pre(threads, save=False, name="threads_clean.csv", columns=['thread_id', 'forum_id', 'url', 'name'], thread_id_col="thread_id", forum_id_col="forum_id"):
    """
    Preprocess threads for further analysis. Dataframe should have thread_id, forum_id column.
    :param forum_id_col: string containing forum_id column name
    :param thread_id_col: string containing thread_id column name
    :param columns: array of strings containing dataframe column names
    :param threads: dataframe containing thread data to preprocess
    :param save: boolean, True if data is to be saved to file
    :param name: string containing name of file to save data to
    :return: dataframe containing preprocessed thread data
    """
    threads = threads[columns]
    threads = threads[threads[thread_id_col].notnull()]
    threads[forum_id_col] = threads[forum_id_col].astype(str)
    query = threads[thread_id_col].str.startswith('-')
    threads.loc[query, thread_id_col] = threads.loc[query, thread_id_col].str.lstrip('-').values
    threads = threads.drop_duplicates(subset=[thread_id_col])

    if save:
        threads.to_csv(name, index=False)

    return threads


def posts_pre(posts, save=False, name="posts_clean.csv", date_col="date"):
    """
    Preprocess posts data for further analysis. Posts should have date column.
    :param posts: dataframe containing posts data
    :param save: boolean, True if processed data is to be saved to file
    :param name: string containing name of file to save data to
    :param date_col: string containing name of date column
    :return: dataframe containing preprocessed posts data
    """
    posts = posts.dropna(subset=[date_col])

    posts[date_col] = posts[date_col].apply(normalize_date)
    posts[date_col] = pd.to_datetime(posts[date_col], format='%d/%m/%Y')

    if save:
        posts.to_csv(name, index=False)

    return posts


def get_data(posts, threads, key="thread_id", method="left", save=True, name="data.csv"):
    """
    Merge posts and threads data.
    :param posts: dataframe containing posts data
    :param threads: dataframe containing threads data
    :param key: string containing common key for both dataframes
    :param method: string containing pd.merge how directive
    :param save: boolean, True if data is to be saved to file
    :param name: string containing name of file to save to
    :return: dataframe containing merged data
    """
    df = pd.merge(posts, threads, on='thread_id', how='left')

    if save:
        df.to_csv('data.csv', index=False)

    return df

