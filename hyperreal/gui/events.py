import wx

CRAWLER_DONE_ID = wx.NewId()
DATA_LOAD_DONE = wx.NewId()


def connect_event(win, func, event_id):
    win.Connect(-1, -1, event_id, func)


class CrawlerDoneEvent(wx.PyEvent):

    def __init__(self, aborted):
        super().__init__()
        self.SetEventType(CRAWLER_DONE_ID)
        self.aborted = aborted


class AsyncOperationDoneEvent(wx.PyEvent):
    def __init__(self, event_id):
        super().__init__()
        self.SetEventType(event_id)
