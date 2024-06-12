import threading

import wx


def display_popup_message(message, title="Admin Client - Message"):
    popup_window = wx.MessageDialog(None, message, title, wx.STAY_ON_TOP)
    popup_window.ShowModal()


class Controller:
    def __init__(self, model, view, request_handler):
        self.model = model
        self.view = view
        self.request_handler = request_handler

        self.view.show_login_view()

        self.view.bind_login(wx.EVT_BUTTON, self.on_login)
        self.view.bind_add_campaign(wx.EVT_BUTTON, self.on_add_campaign)
        self.view.bind_add_voter(wx.EVT_BUTTON, self.on_add_voter)
        self.view.bind_add_voter_to_campaign(wx.EVT_BUTTON, self.on_add_voter_to_campaign)
        self.view.bind_add_nominee_to_campaign(wx.EVT_BUTTON, self.on_add_nominee_to_campaign)
        self.view.bind_get_results(wx.EVT_BUTTON, self.on_get_results)

    def on_login(self, event):
        username, password = self.view.get_login_credentials()
        success = self.request_handler.auth(username, password)

        if success:
            self.view.show_main_view()
            self.model.toggle_auth()
            self.update_time()
            self.view.Layout()
            self.view.set_welcome_message(username)
            self.populate_campaign_choices()

    def update_time(self):
        self.view.update_time()
        wx.CallLater(1000, self.update_time)

    def populate_campaign_choices(self):
        campaigns = self.request_handler.get_campaigns_list()
        self.view.set_campaigns_choices([campaign[1] for campaign in campaigns])
        self.model.set_campaigns(campaigns)

    def on_add_campaign(self, event):
        inputs = self.view.get_add_campaign_input()
        success = self.request_handler.add_campaign(*inputs)

        title = "Add Campaign Result"
        if success:
            message = "Success."
            self.populate_campaign_choices()
        else:
            message = "Failed."

        display_popup_message(message, title)

    def on_add_voter(self, event):
        inputs = self.view.get_add_voter_input()
        success = self.request_handler.add_voter(*inputs)

        title = "Add Voter Result"
        if success:
            message = "Success."
        else:
            message = "Failed."

        display_popup_message(message, title)

    def on_add_voter_to_campaign(self, event):
        voter_name, campaign_index = self.view.get_add_voter_to_campaign_input()
        campaign_name = self.model.get_campaign_by_index(campaign_index)[1]
        campaign_id = self.model.get_campaign_id(campaign_name)
        success = self.request_handler.add_voter_to_campaign(voter_name, campaign_id)

        title = "Add Voter To Campaign Result"
        if success:
            message = "Success."
        else:
            message = "Failed."

        display_popup_message(message, title)

    def on_add_nominee_to_campaign(self, event):
        nominee_name, campaign_index = self.view.get_add_nominee_to_campaign_input()
        campaign_name = self.model.get_campaign_by_index(campaign_index)[1]
        campaign_id = self.model.get_campaign_id(campaign_name)
        success = self.request_handler.add_nominee_to_campaign(nominee_name, campaign_id)

        title = "Add Nominee To Campaign Result"
        if success:
            message = "Success."
        else:
            message = "Failed."

        display_popup_message(message, title)

    def on_get_results(self, event):
        pass
