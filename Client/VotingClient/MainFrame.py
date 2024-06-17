import datetime

import wx

from LoginView import LoginView
from MainView import MainView


class MainFrame(wx.Frame):
    def __init__(self, title):
        super(MainFrame, self).__init__(None, title=title, size=(800, 600),
                                        style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.login_view = LoginView(self)
        self.main_view = MainView(self)

        # add both panels to the frame
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.login_view, 1, wx.EXPAND)
        self.sizer.Add(self.main_view, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.Centre()

    def show_login_view(self):
        # show login panel and hide main panel
        self.login_view.Show()
        self.main_view.Hide()
        self.Layout()

    def show_main_view(self):
        # show main panel and hide login panel
        self.login_view.Hide()
        self.main_view.Show()
        self.Layout()

    def bind_login(self, event, target):
        self.login_view.bind_login(event, target)

    def bind_vote(self, event, target):
        self.main_view.bind_vote(event, target)

    def bind_campaign_choice(self, event, target):
        self.main_view.campaign_choice.Bind(event, target)

    def get_login_credentials(self):
        return self.login_view.get_username_input(), self.login_view.get_password_input()

    def update_time(self):
        self.main_view.time_st.SetLabel(f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")

    def set_welcome_message(self, username):
        self.main_view.set_welcome_message(username)

    def get_campaign_choice(self):
        return self.main_view.campaign_choice.GetStringSelection()

    def get_nominee_choice(self):
        return self.main_view.nominee_choice.GetStringSelection()

    def set_campaign_choices(self, campaigns):
        self.main_view.set_campaign_choices(campaigns)

    def set_nominee_choices(self, nominees):
        self.main_view.set_nominee_choices(nominees)
