import wx


class MainView(wx.Panel):
    def __init__(self, parent):
        super(MainView, self).__init__(parent, size=wx.Size(800, 600), pos=wx.DefaultPosition,
                                       style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.init_ui()

    def init_ui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.text_display = wx.StaticText(self, label="Welcome to the Main View")
        vbox.Add(self.text_display, flag=wx.EXPAND | wx.ALL, border=10)

        self.SetSizer(vbox)
