import wx

import hyperreal.overview.stats as stats
import hyperreal.overview.plotting as plot
import matplotlib.pyplot as plt

from hyperreal.datautils.utils import get_narkopedia
from hyperreal.gui.Dialogues import ask, notify
from hyperreal.gui.Settigns import Settings
from hyperreal.textutils.ngrams import ngram_dict
from hyperreal.textutils.utils import get_narkopedia_map


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


class NGramsMenu(wx.Menu):
    settings: Settings

    def __init__(self, parent):
        super(NGramsMenu, self).__init__()
        self.parent = parent
        self.settings = parent.settings

        if self.settings.narcopedia_file:
            self.narkopedia_df = get_narkopedia(self.settings.narcopedia_file)
            self.narkopedia_map = get_narkopedia_map(self.narkopedia_df)

        narco_names = wx.MenuItem(self, -1, "Narcotics names")
        self.Append(narco_names)
        self.Bind(wx.EVT_MENU, self.narco_names, narco_names)

        drug_aliases = wx.MenuItem(self, -1, "Narcotic's aliases")
        self.Append(drug_aliases)
        self.Bind(wx.EVT_MENU, self.drug_aliases, drug_aliases)

        drug_ngram = wx.MenuItem(self, -1, "Narcotic's N Gram")
        self.Append(drug_ngram)
        self.Bind(wx.EVT_MENU, self.drug_ngram, drug_ngram)

        if not self.settings.narcopedia_file:
            narco_names.Enable(False)
            drug_aliases.Enable(False)
            drug_ngram.Enable(False)

    def create_dict(self):
        content_df = self.parent.data_frame['content']
        return ngram_dict(content_df)

    def narco_names(self, _):
        self.parent.data_frame_cache = None
        self.parent.raw_save = str(self.narkopedia_map.keys())
        self.parent.display((None, self.parent.raw_save))

    def drug_aliases(self, _):
        drug = ask(message="What drug do you want to know about?", default_value="marihuana")
        self.parent.data_frame_cache = None
        self.parent.raw_save = str(self.narkopedia_map[drug])
        self.parent.display((None, self.parent.raw_save))

    def drug_ngram(self, _):
        notify(message="This operation is very computationally intensive. Are you sure your computer can handle it?",
               header="Proceed?")
        drug = ask(message="What drug do you want to know about?", default_value="marihuana")
        ngrams_total, ngrams_docfreq = self.create_dict()
        stats.generate_word_cloud(drug, self.parent.data.frame['content'], self.narkopedia_map, ngrams_docfreq,
                                  length=2)
