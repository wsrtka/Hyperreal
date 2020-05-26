import wx

import hyperreal.overview.stats as stats
import hyperreal.overview.plotting as plot
import matplotlib.pyplot as plt
from hyperreal.gui.Dialogues import ask
from hyperreal.gui.Settigns import Settings


class ForumMenu(wx.Menu):
    settings: Settings

    def __init__(self, parent):
        super(ForumMenu, self).__init__()
        self.parent = parent
        self.settings = parent.settings

        forum_summary = wx.MenuItem(self, -1, "Forum Summary")
        self.Append(forum_summary)
        self.Bind(wx.EVT_MENU, self.forum_summary, forum_summary)

        most_active_authors = wx.MenuItem(self, -1, "Most active authors")
        self.Append(most_active_authors)
        self.Bind(wx.EVT_MENU, self.most_active_authors, most_active_authors)

        posts_distribution = wx.MenuItem(self, -1, "Posts distribution")
        self.Append(posts_distribution)
        self.Bind(wx.EVT_MENU, self.posts_distribution, posts_distribution)

        forum_popularity = wx.MenuItem(self, -1, "Check forum popularity")
        self.Append(forum_popularity)
        self.Bind(wx.EVT_MENU, self.forum_popularity, forum_popularity)

    def forum_summary(self, _):
        plt.clf()
        df = self.parent.data_frame.copy()
        data = stats.get_posts_per_year(df)
        self.parent.data_frame_cache = data
        plot.plot_post_per_year(df)
        plt.savefig(self.settings.temp_folder + "/plot.png")
        self.parent.display((self.settings.temp_folder + "/plot.png", str(data)))

    def most_active_authors(self, _):
        plt.clf()
        df = self.parent.data_frame.copy()
        data = stats.get_most_active_authors(df)
        self.parent.data_frame_cache = data
        plot.plot_author_activity(df)
        plt.savefig(self.settings.temp_folder + "/plot.png")
        self.parent.display((self.settings.temp_folder + "/plot.png", str(data)))

    def posts_distribution(self, _):
        plt.clf()
        df = self.parent.data_frame.copy()
        data = stats.get_total_posts(df)
        self.parent.data_frame_cache = data
        self.parent.display((None, str(data)))

    def forum_popularity(self, _):
        plt.clf()
        df = self.parent.data_frame.copy()
        forum_name = ask(message="What is the name of the forum you are interested in?")
        if forum_name:
            data, name = (stats.get_forum_popularity(df, forum_name))
            self.parent.data_frame_cache = data
            plot.plot_forum_popularity(data, name)
            plt.savefig(self.settings.temp_folder + "/plot.png")
            self.parent.display((self.settings.temp_folder + "/plot.png", str(data)))