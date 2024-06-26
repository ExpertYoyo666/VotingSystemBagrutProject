import wx


def display_popup_message(message, title="Voting Client"):
    popup_window = wx.MessageDialog(None, message, title, wx.STAY_ON_TOP)
    popup_window.ShowModal()


def display_error(reason):
    display_popup_message(reason)


class Controller:
    def __init__(self, model, view, request_handler):
        self.model = model
        self.view = view
        self.request_handler = request_handler

        # start by showing login screen
        self.view.show_login_view()

        # bind buttons to function in both screens
        self.view.bind_login(wx.EVT_BUTTON, self.on_login)
        self.view.bind_vote(wx.EVT_BUTTON, self.on_vote)
        self.view.bind_campaign_choice(wx.EVT_CHOICE, self.on_campaign_choice)
        self.view.login_view.bind_username_input(wx.EVT_TEXT, self.on_input_change)
        self.view.login_view.bind_password_input(wx.EVT_TEXT, self.on_input_change)

    def on_login(self, event):
        username, password = self.view.get_login_credentials()

        try:
            success, reason = self.request_handler.auth(username, password)

            if success:
                self.view.show_main_view()
                self.model.toggle_auth()
                self.update_time()
                self.view.set_welcome_message(username)
                self.model.campaigns = self.request_handler.get_campaigns_list()
                self.view.set_campaign_choices([campaign[2] for campaign in self.model.campaigns])
                self.view.Layout()
            else:
                display_error("Invalid username or password")
        except ConnectionError as e:
            display_popup_message("Server Disconnected", "Connection Error")

    def update_time(self):
        self.view.update_time()
        wx.CallLater(1000, self.update_time)

    def on_input_change(self, event):
        username, password = self.view.get_login_credentials()
        if username and password:
            self.view.login_view.enable_login_button()
        else:
            self.view.login_view.disable_login_button()

    def on_campaign_choice(self, event):
        campaign_name = self.view.get_campaign_choice()

        campaign_id = self.model.get_campaign_id_from_name(campaign_name)

        try:
            self.model.nominees, self.model.public_key = self.request_handler.get_campaign_info(campaign_id)
            self.view.set_nominee_choices([nominee[1] for nominee in self.model.nominees])

        except ConnectionError as e:
            display_popup_message("Server Disconnected", "Connection Error")

    def on_vote(self, event):
        # get inputs
        campaign_name = self.view.get_campaign_choice()
        nominee_name = self.view.get_nominee_choice()
        campaign_id = self.model.get_campaign_id_from_name(campaign_name)
        nominee_id = self.model.get_nominee_id_from_name(nominee_name)
        num_candidates = len(self.model.nominees)

        # check that a campaign and nominee were chosen
        if campaign_id is None or nominee_id is None:
            display_popup_message("Invalid campaign or nominee.")
            return

        # do vote
        success, receipt = False, None
        try:
            success, receipt, reason = self.request_handler.vote(campaign_id, nominee_id, num_candidates, self.model.public_key)
        except ConnectionError as e:
            display_popup_message("Server Disconnected", "Connection Error")

        if success == "SUCCESS":
            message = "Success\nReceipt: " + receipt
        else:
            message = reason

        display_popup_message(message, "Vote Result")
