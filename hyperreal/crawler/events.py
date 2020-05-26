import wx

EVT_RESULT_ID = wx.NewId()


def EVT_RESULT(win, func):
    win.Connect(-1, -1, EVT_RESULT_ID, func)


class CrawlerDoneEvent(wx.PyEvent):

    def __init__(self, aborted):
        super().__init__()
        self.SetEventType(EVT_RESULT_ID)
        self.aborted = aborted
