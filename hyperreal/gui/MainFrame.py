import wx
import pandas as pd
from hyperreal.gui.DataMenu import DataMenu
from hyperreal.gui.Settigns import Settings
import hyperreal.datautils.preprocess as preprocess
from hyperreal.gui.Panels import ImagePanel, TextPanel

title = "Hyperreal"


class MainFrame(wx.Frame):
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

        self.image_panel = ImagePanel(self)
        self.text_panel = TextPanel(self)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.image_panel)
        self.sizer.Add(self.text_panel)
        self.SetSizer(self.sizer)

        self.image_panel.Show(True)
        self.text_panel.Show(False)

        self.Bind(wx.EVT_RIGHT_DOWN, self.on_right_down)

        self.SetSize((600, 600))

    def on_right_down(self, e):
        self.PopupMenu(PopupMenu(self), e.GetPosition())

    def update_menubar(self):
        for m in self.menus:
            m.update_availability()

    def display_text(self, text: str = None):
        if text:
            self.text_panel.load_text(text)
        self.image_panel.Show(False)
        self.text_panel.Show(True)
        self.Layout()

    def display_image(self, filename: str = None):
        if filename:
            self.image_panel.load_image(filename)
        self.image_panel.Show(True)
        self.text_panel.Show(False)
        self.Layout()


class PopupMenu(wx.Menu):

    def __init__(self, parent):
        super(PopupMenu, self).__init__()

        self.parent = parent

        safe_png = wx.MenuItem(self, -1, "Safe as png")
        self.Append(safe_png)
        self.Bind(wx.EVT_MENU, lambda e: window.display_text("a" * 1000), safe_png)

        save_csv = wx.MenuItem(self, -1, "Safe as csv")
        self.Append(save_csv)
        self.Bind(wx.EVT_MENU, lambda e: window.display_image("image_test.png"), save_csv)


app = wx.App()
window = MainFrame()
window.display_text("eljfla;kwfjdsal;fjsadl;fj")
window.display_image("image_test.png")

window.Show()
app.MainLoop()
