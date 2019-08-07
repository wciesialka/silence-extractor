import wx

app = wx.App(None)

def open_dialog(caption="Open File",wildcard="All Files|*.*",defaultDir=""):
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    path = None
    with wx.FileDialog(None, caption, wildcard=wildcard, style=style, defaultDir=defaultDir) as dialog:
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
    return path

def save_dialog(data, caption="Save File", wildcard="All Files|*.*"):
    style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
    with wx.FileDialog(None,caption, wildcard=wildcard,style=style) as dialog:
        if dialog.ShowModal() == wx.ID_CANCEL:
            return False
        
        path = dialog.GetPath()
        try:
            with open(path, 'w') as file:
                file.write(data)
        except IOError:
            print(f"Error in saving file to {path}")
            return False
    return True

def dir_dialog(caption="Open Folder",defaultPath=""):
    style = wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST
    path = None
    with wx.DirDialog(None,message=caption,style=style,defaultPath=defaultPath) as dialog:
        if dialog.ShowModal() == wx.ID_CANCEL:
            return None
        path = dialog.GetPath()
    return path

def ok_cancel_dialog(message, caption=""):
    style = wx.OK | wx.CENTRE | wx.ICON_INFORMATION | wx.OK_DEFAULT | wx.CANCEL
    value = None
    with wx.MessageDialog(None,message,caption=caption,style=style) as dialog:
        value = dialog.ShowModal()
    return value == wx.ID_OK

def ok_dialog(message, caption=""):
    style = wx.OK | wx.CENTRE | wx.ICON_INFORMATION | wx.OK_DEFAULT
    with wx.MessageDialog(None,message,caption=caption,style=style) as dialog:
        dialog.ShowModal()
    return True

def error_dialog(message, caption=""):
    style = wx.OK | wx.CENTRE | wx.ICON_ERROR | wx.OK_DEFAULT
    with wx.MessageDialog(None,message,caption=caption,style=style) as dialog:
        dialog.ShowModal()
    return True

def text_entry_dialog(message="", caption="", default=""):
    response = None
    with wx.TextEntryDialog(None, message, caption=caption, value=default) as dialog:
        dialog.ShowModal()
        response = dialog.GetValue()
    return response

def number_entry_dialog(message="",prompt="",caption="",default=0,min=-2147483647,max=2147483647):
    response = None
    with wx.NumberEntryDialog(None,message,prompt,caption,default,min,max) as dialog:
        dialog.ShowModal()
        response = dialog.GetValue()
    return response

def yes_no_dialog(message, caption=""):
    style = wx.YES_NO | wx.CENTRE | wx.ICON_QUESTION | wx.YES_DEFAULT
    with wx.MessageDialog(None,message,caption=caption,style=style) as dialog:
        response = dialog.ShowModal()
    return response == wx.ID_YES

def progress_dialog(message, caption="", maximum=100):
    return wx.GenericProgressDialog(caption,message,maximum=maximum)