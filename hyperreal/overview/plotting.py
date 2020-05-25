import matplotlib.pyplot as plt
import seaborn as sns


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
    """
    Plot the user activity using the number of their posts.
    :param data: dataframe containing post data
    :param author_column: string name of author column
    :param post_id_column: string name of post identifier
    :param ascending: boolean, True if you want to get
    :param top: int number of top authors to plot
    :return:
    """
    data.groupby(author_column).count()[post_id_column].sort_values(ascending=ascending)[:30].plot.barh()


def plot_total_post_count_per_forum(to_plot):
    """
    Plot total post count per forum.
    :param to_plot: object prepared by the get_total_posts() function in hyperreal.overview.stats
    :return:
    """
    g = sns.catplot(x="forum_name", y="count", data=to_plot, aspect=5, hue='count', legend=False)
    g.set_xticklabels(rotation=90)


def plot_forum_popularity(timeframe, forum_name):
    """
    Plot the number of posts per month.
    :param timeframe: data prepared by the get_forum_popularity() function in hyperreal.overview.stats
    :param forum_name: name of forum (also returned by the aforementioned function
    :return:
    """
    sns.set_style("whitegrid")
    g = sns.relplot(x='date', y='post_count', hue='post_count', aspect=2, data=timeframe)
    g.fig.autofmt_xdate()
    g.ax.set_title(forum_name)


def plot_drug_correlation(data):
    """
    Plot the correlation between interest in tow drugs.
    :param data: dataframe returned by the get_drug_correlation() function in hyperreal.overview.user
    :return:
    """
    
