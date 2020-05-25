import wx
import pandas as pd
from hyperreal.gui.DataMenu import DataMenu
from hyperreal.gui.Settigns import Settings
import hyperreal.datautils.preprocess as preprocess

title = "Hyperreal"


class MainWindow(wx.Frame):
    def __init__(self):
        super().__init__(None, title=title)
        self.settings = Settings()
        self.data_frame = None

        menubar = wx.MenuBar()
        self.SetMenuBar(menubar)
        self.menus = []

        self.data_menu = DataMenu(self)
        self.menus.append(self.data_menu)
        menubar.Append(self.data_menu, "Data")

        self.Bind(wx.EVT_RIGHT_DOWN, self.on_right_down)

    def on_right_down(self, e):
        self.PopupMenu(PopupMenu(self), e.GetPosition())

    def update_menubar(self):
        for m in self.menus:
            m.update_availability()


class PopupMenu(wx.Menu):

    def __init__(self, parent):
        super(PopupMenu, self).__init__()

        self.parent = parent

        safe = wx.MenuItem(self, wx.ID_NEW, "Safe as png")
        self.Append(safe)
        self.Bind(wx.EVT_MENU, lambda e: print("triger"), safe)

        safe = wx.MenuItem(self, wx.ID_NEW, "Safe as csv")
        self.Append(safe)


app = wx.App()
window = MainWindow()
window.Show()
app.MainLoop()
