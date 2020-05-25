import wx
import json
from hyperreal.gui.CrawlerMenubar import DataMenu
from hyperreal.gui.Settigns import Settings

title = "Hyperreal"


class MainWindow(wx.Frame):
    def __init__(self):
        super().__init__(None, title=title)
        self.settings = Settings()
        self.menus = []
        #self.text = wx.TextCtrl(self, -1, style=wx.EXPAND | wx.TE_MULTILINE)
        self.init_ui()

    def init_ui(self):
        menubar = wx.MenuBar()
        crawler_menu = DataMenu(self)



        self.menus.append(crawler_menu)
        menubar.Append(crawler_menu, "cra")

        wx.PopupTransientWindow(self, 0)

        self.SetMenuBar(menubar)

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
