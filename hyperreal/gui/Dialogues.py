import wx


def error(parent=None, message='', caption="Error"):
    erd = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_ERROR)
    erd.ShowModal()
    erd.Destroy()


def ask(parent=None, message='', default_value='') -> str:
    dlg = wx.TextEntryDialog(parent, message, value=default_value)
    dlg.ShowModal()
    result = dlg.GetValue()
    dlg.Destroy()
    return result


