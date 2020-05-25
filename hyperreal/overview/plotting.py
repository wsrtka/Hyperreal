import matplotlib as plt


def plot_post_per_year(data, date_column="date"):
    """
    Plot the number of posts per year
    :param data: dataframe containing forum data
    :param date_column: string name of column containing date
    :return:
    """
    by_year = data[date_column].groupby([data.date.dt.year]).agg('count')
    by_year.plot('bar')


def plot_author_activity(data, author_column="author", post_id_column="post_id", ascending=False, top=10):
    """"""
    df.groupby('author').count()['post_id'].sort_values(ascending=False)[:30].plot.barh()
