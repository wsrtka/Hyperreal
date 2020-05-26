import wx
import pandas as pd
from hyperreal.gui.DataMenu import DataMenu
from hyperreal.gui.PlotMenus import ForumMenu
from hyperreal.gui.Settigns import Settings
import hyperreal.datautils.preprocess as preprocess
from hyperreal.gui.Panels import ImagePanel, TextPanel
from typing import Tuple

title = "Hyperreal"


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title=title)
        self.settings = Settings()
        self.data_frame = None

        menubar = wx.MenuBar()
        self.SetMenuBar(menubar)

        self.data_menu = DataMenu(self)
        menubar.Append(self.data_menu, "Data")

        self.data_dependent_menu = []
        forum_menu = ForumMenu(self)
        menubar.Append(forum_menu, "Forum")

        self.update_menubar()

        self.image_panel = ImagePanel(self)
        self.text_panel = TextPanel(self)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.image_panel)
        self.sizer.Add(self.text_panel)
        self.SetSizer(self.sizer)

        self.can_switch = False
        self.image_on_top = True
        self.image_panel.Show(True)
        self.text_panel.Show(False)

        self.Bind(wx.EVT_RIGHT_DOWN, self.on_right_down)

        self.SetSize((1000, 600))

    def on_right_down(self, e):
        self.PopupMenu(PopupMenu(self), e.GetPosition())

    def update_menubar(self):
        for m in self.data_dependent_menu:
            m.EnableTop(0, self.data_frame)

    def display(self, data: Tuple[str, str]):
        self.display_image(data[0])
        self.display_text(data[1])
        if data[0]:
            self.display_image()
        self.can_switch = True if (data[0] and data[1]) else False

    def display_text(self, text: str = None):
        if text:
            self.text_panel.load_text(text)
        self.image_panel.Show(False)
        self.image_on_top = False
        self.text_panel.Show(True)
        self.Layout()

    def display_image(self, filename: str = None):
        if filename:
            self.image_panel.load_image(filename)
        self.image_panel.Show(True)
        self.image_on_top = True
        self.text_panel.Show(False)
        self.Layout()


class PopupMenu(wx.Menu):
    parent: MainFrame

    def __init__(self, parent):
        super(PopupMenu, self).__init__()

        self.parent = parent

        switch_control = wx.MenuItem(self, -1, "Switch view")
        switch_control.Enable(self.parent.can_switch)
        self.Append(switch_control)
        self.Bind(wx.EVT_MENU, self.switch, switch_control)

        save_to_file = wx.MenuItem(self, -1, "Safe")
        self.Append(save_to_file)
        self.Bind(wx.EVT_MENU, lambda e: print("safe"), save_to_file)

    def switch(self, _):
        if self.parent.image_on_top:
            self.parent.display_text()
        else:
            self.parent.display_image()


app = wx.App()
window = MainFrame()
window.display(("image_test.png", "a" * 1000))

window.Show()
app.MainLoop()
