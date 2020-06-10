import wx
import os
import shutil
from typing import List
import pandas as pd
from datetime import date, datetime

from wx import MenuItem

import hyperreal.gui.events as events
from hyperreal.crawler.crawler import start_append_crawl, start_full_crawl
import hyperreal.datautils.preprocess as preprocess

from hyperreal.gui.Dialogues import ask, error, notify


class DataMenu(wx.Menu):
    item_list: List[MenuItem]

    def __init__(self, parent):
        super(DataMenu, self).__init__()

        self.parent = parent

        self.settings = parent.settings

        self.crawler_active = False

        load_data = wx.MenuItem(self, -1, "Load/reload data")
        self.Append(load_data)
        self.Bind(wx.EVT_MENU, self.load_data, load_data)

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

        abort_crawler = wx.MenuItem(self, -1, "Abort downloading data")
        self.Append(abort_crawler)
        self.Bind(wx.EVT_MENU, self.abort_crawler, abort_crawler)

        self.item_list = [load_data, dynamic_crawl, full_crawl, invalidate_data, filter_data, abort_crawler]
        self.update_availability()

        self.parent.background_thread = None

    def get_data_availability(self):
        return not self.crawler_active and os.path.isfile(self.settings.data_folder + "/data.csv")

    def update_availability(self):
        self.Enable(self.item_list[0].GetId(), self.get_data_availability())
        self.Enable(self.item_list[1].GetId(), self.get_data_availability() and not self.crawler_active)
        self.Enable(self.item_list[2].GetId(), not self.crawler_active)
        self.Enable(self.item_list[3].GetId(), not self.crawler_active and self.get_data_availability())
        self.Enable(self.item_list[4].GetId(), self.parent.data_frame is not None)
        self.Enable(self.item_list[5].GetId(), self.crawler_active)

    def crawler_change(self, b):
        self.crawler_active = b
        self.update_availability()

    def abort_crawler(self, _):
        self.parent.abort_background_task()

    def dynamic_crawl(self, _):
        if self.parent.is_background_task_running():
            error(self.parent, "Background task already running")
            return

        dialog = wx.MessageDialog(self.parent,
                                  "Are you sure you want to start dynamic crawl? It might take a while.",
                                  "Start dynamic crawl", wx.YES_NO | wx.ICON_QUESTION)
        if dialog.ShowModal() == wx.ID_YES:
            self.crawler_change(True)
            events.connect_event(self, self.on_crawler_done, events.CRAWLER_DONE_ID)
            self.parent.background_thread = start_append_crawl(self.settings.data_folder, self.settings.last_crawl,
                                                               self)
            self.parent.background_thread.start()

    def full_crawl(self, _):
        if self.parent.is_background_task_running():
            error(self.parent, "Background task already running")
            return

        dialog = wx.MessageDialog(self.parent,
                                  "Are you sure you want to start full crawl? It might take a few hours.",
                                  "Start full crawl", wx.YES_NO | wx.ICON_QUESTION)
        if dialog.ShowModal() == wx.ID_YES:
            self.crawler_change(True)

            events.connect_event(self, self.on_crawler_done, events.CRAWLER_DONE_ID)
            self.parent.background_thread = start_full_crawl(self.settings.data_folder, self)
            self.parent.background_thread.start()

    def on_crawler_done(self, event):
        self.crawler_change(False)
        if event.aborted:
            notify(message="Crawler aborted")
        else:
            notify(message="Crawler finished")
        self.settings.last_crawl = date.today()
        self.settings.save()

    def invalidate_data(self, _):
        dialog = wx.MessageDialog(self.parent,
                                  "This will delete all data. You will have to download it again.",
                                  "Delete data warning", wx.OK | wx.CANCEL | wx.ICON_WARNING)
        if dialog.ShowModal() == wx.OK:
            self.crawler_change(True)
            shutil.rmtree(self.settings.data_folder, ignore_errors=True)
            os.rmdir(self.settings.data_folder)
            self.crawler_change(False)

    def filter_data(self, _):
        def validate_date(date_text):
            try:
                year, month, day = date_text.split("-")
                datetime(int(year), int(month), int(day))
            except ValueError:
                raise ValueError("Incorrect data format, should be YYYY-MM-DD")

        try:
            date1 = ask(self.parent, "Enter start date or leave empty")
            if date1:
                validate_date(date1)
            else:
                date1 = "1980-01-01"
            date2 = ask(self.parent, "Enter end date or leave empty")
            if date2:
                validate_date(date2)
            else:
                date2 = "2050-01-01"

            df = self.parent.data_frame
            self.parent.data_frame = df[(df['date'] > date1) & (df['date'] < date2)]
        except ValueError as exc:
            error(self.parent, str(exc))

    def load_data(self, _):
        if self.get_data_availability():
            events.connect_event(self, self.on_load_data_done, events.DATA_LOAD_DONE)
            self.parent.start_background_task(self.exec_load_data)

    def exec_load_data(self):
        df = pd.read_csv(self.settings.data_folder + "/data.csv")
        self.parent.data_frame = preprocess.data_pre(df)
        self.update_availability()
        self.parent.update_menubar()
        wx.PostEvent(self, events.AsyncOperationDoneEvent(events.DATA_LOAD_DONE))

    def on_load_data_done(self, _):
        notify(message="Finished loading data")
        self.parent.display([None, "Finished loading data"])
