import wx


class MainView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, pos=wx.DefaultPosition, size=wx.Size(800, 600),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        title_sizer = wx.GridSizer(1, 2, 0, 0)

        self.welcome_st = wx.StaticText(self, wx.ID_ANY, "Welcome Voter", wx.DefaultPosition, wx.DefaultSize, 0)
        self.welcome_st.Wrap(-1)

        self.welcome_st.SetFont(
            wx.Font(22, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString))

        title_sizer.Add(self.welcome_st, 0, wx.ALIGN_CENTER, 5)

        self.time_st = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.time_st.Wrap(-1)

        self.time_st.SetFont(
            wx.Font(18, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString))

        title_sizer.Add(self.time_st, 0, wx.ALIGN_CENTER, 5)

        main_sizer.Add(title_sizer, 0, wx.EXPAND, 5)

        main_sizer.Add((0, 100), 0, wx.EXPAND, 5)

        choice_sizer = wx.BoxSizer(wx.VERTICAL)

        self.campaign_st = wx.StaticText(self, wx.ID_ANY, "Choose Campaign To Vote For", wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        self.campaign_st.Wrap(-1)

        self.campaign_st.SetFont(
            wx.Font(24, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString))

        choice_sizer.Add(self.campaign_st, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        campaign_choiceChoices = []
        self.campaign_choice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(300, -1), campaign_choiceChoices,
                                         0)
        self.campaign_choice.SetSelection(0)
        self.campaign_choice.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString))

        choice_sizer.Add(self.campaign_choice, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        choice_sizer.Add((0, 100), 0, 0, 5)

        self.nominee_st = wx.StaticText(self, wx.ID_ANY, "Choose A Nominee To Vote For", wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        self.nominee_st.Wrap(-1)

        self.nominee_st.SetFont(
            wx.Font(24, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString))

        choice_sizer.Add(self.nominee_st, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        nominee_choiceChoices = []
        self.nominee_choice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(300, -1), nominee_choiceChoices, 0)
        self.nominee_choice.SetSelection(0)
        self.nominee_choice.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString))

        choice_sizer.Add(self.nominee_choice, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        main_sizer.Add(choice_sizer, 0, wx.ALIGN_CENTER, 5)

        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.vote_button = wx.Button(self, wx.ID_ANY, "Vote", wx.DefaultPosition, wx.DefaultSize, 0)
        self.vote_button.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString))

        buttons_sizer.Add(self.vote_button, 0, wx.ALL, 5)

        main_sizer.Add(buttons_sizer, 0, wx.ALIGN_CENTER, 5)

        self.SetSizer(main_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

    def set_welcome_message(self, username):
        self.welcome_st.SetLabel(f"Welcome {username}")
        self.Layout()

    def bind_vote(self, event, target):
        self.vote_button.Bind(event, target)

    def get_campaign_choice(self):
        return self.campaign_choice.GetStringSelection()

    def set_campaign_choices(self, campaigns):
        self.campaign_choice.SetItems(campaigns)
        self.Layout()

    def set_nominee_choices(self, nominees):
        self.nominee_choice.SetItems(nominees)
        self.Layout()
