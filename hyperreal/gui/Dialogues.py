import wx


class ErrorDialogue(wx.MessageDialog):
    def __init__(self, window, message):
        super().__init__(window, message, "Error", wx.OK | wx.ICON_ERROR)
        self.ShowModal()
        self.Destroy()