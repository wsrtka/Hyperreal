import wx
import os
import functools

import hyperreal.overview.stats as stats
import hyperreal.overview.plotting as plot
import matplotlib.pyplot as plt

from hyperreal.datautils.utils import get_narkopedia
from hyperreal.gui.Dialogues import ask, notify
from hyperreal.gui.Settigns import Settings
from hyperreal.textutils.ngrams import ngram_dict
from hyperreal.textutils.utils import get_narkopedia_map, get_sentences
from hyperreal.textutils.word2vec import load_model_from_file, finetuned_model, find_new_drug_names, find_symptoms


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
        forum_name = ask(message="What is the name of the forum you are interested in?", default_value="inne-stymulanty")
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

        narco_names = wx.MenuItem(self, -1, "Narcotics names")
        self.Append(narco_names)
        self.Bind(wx.EVT_MENU, self.narco_names, narco_names)

        drug_aliases = wx.MenuItem(self, -1, "Narcotic's aliases")
        self.Append(drug_aliases)
        self.Bind(wx.EVT_MENU, self.drug_aliases, drug_aliases)

        drug_ngram = wx.MenuItem(self, -1, "Narcotic's N Gram")
        self.Append(drug_ngram)
        self.Bind(wx.EVT_MENU, self.drug_ngram, drug_ngram)

        if os.path.isfile(self.settings.narcopedia_file):
            self.narkopedia_df = get_narkopedia(self.settings.narcopedia_file)
            self.narkopedia_map = get_narkopedia_map(self.narkopedia_df)
        else:
            narco_names.Enable(False)
            drug_aliases.Enable(False)
            drug_ngram.Enable(False)

    def create_dict(self):
        content_df = self.parent.data_frame['content']
        return ngram_dict(content_df)

    def only_chars(self, res):
        self.parent.raw_save = str(res)
        self.parent.display((None, self.parent.raw_save))

    def narco_names(self, _):
        self.parent.data_frame_cache = None
        self.only_chars(", ".join(self.narkopedia_map.keys()))

    def drug_aliases(self, _):
        drug = ask(message="What drug do you want to know about?", default_value="marihuana")
        self.parent.data_frame_cache = None
        self.only_chars(", ".join(self.narkopedia_map[drug]))

    def drug_ngram(self, _):
        dialog = wx.MessageDialog(self.parent,
                                  "This operation is very computationally intensive. "
                                  "Are you sure your computer can handle it?",
                                  "Proceed?", wx.YES_NO | wx.ICON_QUESTION)
        if dialog.ShowModal() == wx.ID_YES:
            drug = ask(message="What drug do you want to know about?", default_value="marihuana")
            plt.clf()
            ngrams_total, ngrams_docfreq = self.create_dict()
            stats.generate_word_cloud(drug, self.parent.data.frame['content'], self.narkopedia_map, ngrams_docfreq,
                                      length=2)
            plt.savefig(self.settings.temp_folder + "/plot.png")
            self.parent.display((self.settings.temp_folder + "/plot.png", None))


class NLPMenu(wx.Menu):
    settings: Settings

    def __init__(self, parent):
        super(NLPMenu, self).__init__()
        self.parent = parent
        self.settings = parent.settings

        new_drug_names = wx.MenuItem(self, -1, "New drug names")
        self.Append(new_drug_names)
        self.Bind(wx.EVT_MENU, self.new_drug_names, new_drug_names)

        symptoms = wx.MenuItem(self, -1, "Drug symptoms")
        self.Append(symptoms)
        self.Bind(wx.EVT_MENU, self.symptoms, symptoms)

        if os.path.isfile(self.settings.model_file):
            self.model = load_model_from_file(self.settings.model_file)
            self.model_after = None
        else:
            new_drug_names.Enable(False)
            symptoms.Enable(False)

    def get_model(self):
        if not self.model_after:
            sentences = get_sentences(self.parent.data_frame)
            self.model_after = finetuned_model(self.model, sentences, 'fasttext_file', 'drug_w2v', './finetuned_model')
        return self.model_after

    def only_chars(self, res):
        self.parent.raw_save = str(res)
        self.parent.display((None, self.parent.raw_save))

    def new_drug_names(self, e):
        drug = ask(message="What drug do you want to know about?", default_value="marihuana")
        res = find_new_drug_names(drug, self.get_model())
        self.only_chars(res[10:])  # Czy to ma sens?!?!?!?

    def symptoms(self, e):
        symptoms = ask(message="What symptom are you looking for?", default_value="wymioty")
        synonyms = []
        res = find_symptoms(symptoms, self.get_model(), synonyms)
        self.only_chars(res)