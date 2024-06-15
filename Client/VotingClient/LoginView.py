import wx


class LoginView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, pos=wx.DefaultPosition, size=wx.Size(800, 600),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.title_st = wx.StaticText(self, wx.ID_ANY, "Digital Voting System", wx.DefaultPosition, wx.DefaultSize, 0)
        self.title_st.Wrap(-1)

        self.title_st.SetFont(
            wx.Font(30, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString))

        main_sizer.Add(self.title_st, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.author_st = wx.StaticText(self, wx.ID_ANY, "By: Yoav Steinberg", wx.DefaultPosition, wx.DefaultSize, 0)
        self.author_st.Wrap(-1)

        self.author_st.SetFont(
            wx.Font(15, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString))

        main_sizer.Add(self.author_st, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        main_sizer.Add((0, 100), 0, wx.EXPAND, 5)

        sizer2 = wx.BoxSizer(wx.VERTICAL)

        sizer3 = wx.BoxSizer(wx.HORIZONTAL)

        self.login_st = wx.StaticText(self, wx.ID_ANY, "Login Page", wx.DefaultPosition, wx.DefaultSize, 0)
        self.login_st.Wrap(-1)

        self.login_st.SetFont(
            wx.Font(22, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString))

        sizer3.Add(self.login_st, 0, wx.ALIGN_CENTER | wx.ALL, 0)

        sizer2.Add(sizer3, 1, wx.ALIGN_CENTER | wx.ALL, 5)

        sizer4 = wx.FlexGridSizer(0, 2, 0, 0)
        sizer4.SetFlexibleDirection(wx.BOTH)
        sizer4.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.username_st = wx.StaticText(self, wx.ID_ANY, "Username:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.username_st.Wrap(-1)

        self.username_st.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True, wx.EmptyString))

        sizer4.Add(self.username_st, 0, wx.ALL, 5)

        self.username_input = wx.TextCtrl(self, wx.ID_ANY, "", wx.DefaultPosition, wx.Size(150, 25), 0)
        self.username_input.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString))

        sizer4.Add(self.username_input, 0, wx.ALL, 5)

        self.password_st = wx.StaticText(self, wx.ID_ANY, "Password:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.password_st.Wrap(-1)

        self.password_st.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True, wx.EmptyString))

        sizer4.Add(self.password_st, 0, wx.ALL, 5)

        self.password_input = wx.TextCtrl(self, wx.ID_ANY, "", wx.DefaultPosition, wx.Size(150, 25), 0)
        self.password_input.SetFont(
            wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString))

        sizer4.Add(self.password_input, 0, wx.ALL, 5)

        sizer2.Add(sizer4, 1, wx.ALIGN_CENTER, 5)

        sizer5 = wx.BoxSizer(wx.HORIZONTAL)

        self.login_button = wx.Button(self, wx.ID_ANY, "Login", wx.DefaultPosition, wx.DefaultSize, 0)
        self.login_button.SetFont(
            wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, wx.EmptyString))

        sizer5.Add(self.login_button, 0, wx.ALL, 5)

        sizer2.Add(sizer5, 0, wx.ALIGN_CENTER, 5)

        sizer2.Add((0, 100), 1, wx.EXPAND, 5)

        sizer6 = wx.BoxSizer(wx.VERTICAL)

        self.message_st = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.message_st.Wrap(-1)

        self.message_st.SetFont(
            wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString))

        sizer6.Add(self.message_st, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        sizer2.Add(sizer6, 1, wx.EXPAND, 5)

        main_sizer.Add(sizer2, 0, wx.EXPAND, 100)

        self.SetSizer(main_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

    def get_username_input(self):
        return self.username_input.GetValue()

    def get_password_input(self):
        return self.password_input.GetValue()

    def bind_login(self, event, target):
        self.login_button.Bind(event, target)
