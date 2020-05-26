import wx
from hyperreal.gui.Dialogues import error


class ImagePanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        image = wx.Image(240, 240)
        self.photo_max_size = 900
        self.image_control = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(image))

        self.image_control.Bind(wx.EVT_RIGHT_DOWN, parent.on_right_down)

    def load_image(self, filename):
        try:
            image = wx.Image(filename, wx.BITMAP_TYPE_ANY)
            # W = image.GetWidth()
            # H = image.GetHeight()
            # if W > H:
            #     NewW = self.photo_max_size
            #     NewH = self.photo_max_size * H / W
            # else:
            #     NewH = self.photo_max_size
            #     NewW = self.photo_max_size * W / H
            # image = image.Scale(NewW, NewH)
            self.image_control.SetBitmap(wx.Bitmap(image))
            self.Refresh()
        except IOError:
            error(self, "Image file %s not found" % filename)


class TextPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.text = wx.StaticText(self, label="elo")

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.mainSizer.Add(self.text, 0, wx.ALL, 5)
        self.mainSizer.Add(self.sizer, 0, wx.ALL, 5)

        self.text.Bind(wx.EVT_RIGHT_DOWN, parent.on_right_down)

    def load_text(self, text: str):
        self.text.SetLabel(label=text)
