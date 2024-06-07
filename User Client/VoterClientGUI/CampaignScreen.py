import wx
import abc
from datetime import datetime


class VoterCampaignFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="Digital Voting System Voter Client - Vote",
                          pos=wx.DefaultPosition, size=wx.Size(800, 600),
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

        title_sizer.Add(self.time_st, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

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
        self.vote_button.Bind(wx.EVT_BUTTON, self.on_vote_button_press)
        self.vote_button.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString))

        buttons_sizer.Add(self.vote_button, 0, wx.ALL, 5)

        self.confirmation_button = wx.Button(self, wx.ID_ANY, "Get Confirmation", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.confirmation_button.Bind(wx.EVT_BUTTON, self.on_confirmation_button_press)
        self.confirmation_button.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString))

        buttons_sizer.Add(self.confirmation_button, 0, wx.ALL, 5)

        main_sizer.Add(buttons_sizer, 0, wx.ALIGN_CENTER, 5)

        self.SetSizer(main_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

    @abc.abstractmethod
    def on_confirmation_button_press(self, event):
        pass

    @abc.abstractmethod
    def on_vote_button_press(self, event):
        pass


class VoterCampaignScreen(VoterCampaignFrame):
    def __init__(self):
        super().__init__(None)
        self.update_time()

    def on_confirmation_button_press(self, event):
        popup_window = wx.MessageDialog(None, "hi", "Confirmation Message", wx.STAY_ON_TOP)
        popup_window.ShowModal()

    def on_vote_button_press(self, event):
        popup_window = wx.MessageDialog(None, "hi", "Confirmation Message", wx.STAY_ON_TOP)
        popup_window.ShowModal()

    def update_time(self):
        self.time_st.SetLabel(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
        wx.CallLater(1000, self.update_time)


if __name__ == '__main__':
    app = wx.App()
    frm = VoterCampaignScreen()
    frm.Show()
    app.MainLoop()
