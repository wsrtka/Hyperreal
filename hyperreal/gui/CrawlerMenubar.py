import wx
import glob
import os
import shutil
from typing import List

from wx import MenuItem

from hyperreal.crawler.crawler import start_append_crawl, start_full_crawl
from hyperreal.crawler.datautils import create_data_csv, append_data_csv

from hyperreal.gui.Dialogues import ErrorDialogue

data_folder = "data"


class DataMenu(wx.Menu):

    item_list: List[MenuItem]

    def __init__(self, parent):
        super(DataMenu, self).__init__()
        self.parent = parent
        self.settings = parent.settings

        self.crawler_active = False

        dynamic_crawl = wx.MenuItem(self, -1, "Download only new data")
        self.Append(dynamic_crawl)
        self.Bind(wx.EVT_MENU, self.dynamic_crawl, dynamic_crawl)

        full_crawl = wx.MenuItem(self, -1, "Download data from scratch")
        self.Append(full_crawl)
        self.Bind(wx.EVT_MENU, self.full_crawl, full_crawl)

        invalidate_data = wx.MenuItem(self, -1, "Invalidate data")
        self.Append(invalidate_data)
        parent.Bind(wx.EVT_MENU, self.invalidate_data, invalidate_data)

        filter_data = wx.MenuItem(self, -1, "Filter data by date")
        self.Append(filter_data)
        self.Bind(wx.EVT_MENU, self.filter_data, filter_data)

        self.item_list = [dynamic_crawl, full_crawl, invalidate_data, filter_data]
        self.update_availability()

    def get_data_availability(self):
        return not self.crawler_active and os.path.isfile(data_folder + "/data.csv")

    def update_availability(self):
        self.Enable(self.item_list[0].GetId(), self.get_data_availability())
        self.Enable(self.item_list[1].GetId(), not self.crawler_active)
        self.Enable(self.item_list[2].GetId(), not self.crawler_active)
        self.Enable(self.item_list[3].GetId(), self.get_data_availability())

    def crawler_change(self, b):
        self.crawler_active = b
        self.parent.update_menubar()

    def dynamic_crawl(self, _):
        dialog = wx.MessageDialog(self.parent,
                                  "Are you sure you want to start dynamic crawl? It might take a while.",
                                  "Start dynamic crawl", wx.YES_NO | wx.ICON_QUESTION)
        if dialog.ShowModal() == wx.YES:
            self.crawler_change(True)
            try:
                start_append_crawl(data_folder, self.settings.last_crawl)
                append_data_csv(data_folder)
            except Exception as error:
                ErrorDialogue(self.parent, "Crawler failed: " + str(error))
            self.crawler_change(False)

    def full_crawl(self, _):
        dialog = wx.MessageDialog(self.parent,
                                  "Are you sure you want to start full crawl? It might even take over 4 hours.",
                                  "Start full crawl", wx.YES_NO | wx.ICON_QUESTION)
        if dialog.ShowModal() == wx.YES:
            self.crawler_change(True)
            self.parent.update_menubar()
            try:
                if not os.path.isdir(data_folder):
                    os.mkdir(data_folder, mode=0o755)
            except OSError as error:
                ErrorDialogue(self.parent, "Failed to create folder for data: " + str(error))
                self.crawler_change(False)
                return
            try:
                start_full_crawl(data_folder)
                create_data_csv(data_folder)
            except Exception as error:
                ErrorDialogue(self.parent, "Crawler failed: " + str(error))
            self.crawler_change(False)

    def invalidate_data(self, _):
        dialog = wx.MessageDialog(self.parent,
                                  "This will delete all data. You will have to download it again.",
                                  "Delete data warning", wx.OK | wx.CANCEL | wx.ICON_WARNING)
        if dialog.ShowModal() == wx.OK:
            self.crawler_change(True)
            self.parent.update_menubar()
            shutil.rmtree(data_folder, ignore_errors=True)
            os.rmdir(data_folder)
            self.crawler_change(False)

    def filter_data(self, _):
        self.crawler_change(True)
        self.parent.update_menubar()
        pass
        self.crawler_change(False)
