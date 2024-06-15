import datetime

import wx

from Client.AdminClient.Controller import Controller
from Client.AdminClient.Model import Model
from Client.AdminClient.Protocol import Protocol
from LoginView import LoginView
from MainView import MainView


class MainFrame(wx.Frame):
    def __init__(self, title):
        super(MainFrame, self).__init__(None, title=title, size=(800, 600),
                                        style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.login_view = LoginView(self)
        self.main_view = MainView(self)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.login_view, 1, wx.EXPAND)
        self.sizer.Add(self.main_view, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.Centre()

    def show_login_view(self):
        self.login_view.Show()
        self.main_view.Hide()
        self.Layout()

    def show_main_view(self):
        self.login_view.Hide()
        self.main_view.Show()
        self.Layout()

    def bind_login(self, event, target):
        self.login_view.bind_login(event, target)

    def bind_add_campaign(self, event, target):
        self.main_view.bind_add_campaign(event, target)

    def bind_activate_campaign(self, event, target):
        self.main_view.bind_activate_campaign(event, target)

    def bind_add_voter(self, event, target):
        self.main_view.bind_add_voter(event, target)

    def bind_add_voter_to_campaign(self, event, target):
        self.main_view.bind_add_voter_to_campaign(event, target)

    def bind_add_nominee_to_campaign(self, event, target):
        self.main_view.bind_add_nominee_to_campaign(event, target)

    def bind_get_results(self, event, target):
        self.main_view.bind_get_results(event, target)

    def get_login_credentials(self):
        return self.login_view.get_username_input(), self.login_view.get_password_input()

    def get_add_campaign_input(self):
        return self.main_view.get_add_campaign_input()

    def get_activate_campaign_input(self):
        return self.main_view.get_activate_campaign_input()

    def get_add_voter_input(self):
        return self.main_view.get_add_voter_input()

    def get_get_results_input(self):
        return self.main_view.get_get_results_input()

    def get_add_voter_to_campaign_input(self):
        return self.main_view.get_add_voter_to_campaign_input()

    def get_add_nominee_to_campaign_input(self):
        return self.main_view.get_add_nominee_to_campaign_input()

    def update_time(self):
        self.main_view.update_time(f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")

    def set_welcome_message(self, username):
        self.main_view.set_welcome_message(username)

    def set_campaigns_choices(self, campaigns):
        self.main_view.set_campaigns_choices(campaigns)
