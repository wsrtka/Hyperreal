import wx
from hyperreal.gui.Dialogues import error
from wx.lib import wordwrap


class ImagePanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.parent = parent

        image = wx.Image(1, 1)
        self.photo_max_size = 900
        self.image_control = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(image))

        self.image_control.Bind(wx.EVT_RIGHT_DOWN, parent.on_right_down)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddStretchSpacer()
        sizer.Add(self.image_control, 0, wx.CENTER)
        sizer.AddStretchSpacer()

        self.SetSizer(sizer)

    def load_image(self, filename):
        try:
            image = wx.Image(filename, wx.BITMAP_TYPE_ANY)
            self.image_control.SetBitmap(wx.Bitmap(image))
            self.parent.SetSize(image.GetWidth(), image.GetHeight() + 100)
            self.Refresh()
        except IOError:
            error(self, "Image file %s not found" % filename)


class TextPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        self.text = wx.StaticText(self, label="empty")
        self.text.Bind(wx.EVT_RIGHT_DOWN, parent.on_right_down)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.text)
        self.SetSizer(sizer)

    def load_text(self, text: str):
        self.text.SetLabel(label=text)
        self.text.Wrap(1000)
