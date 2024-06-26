import uuid

import wx
from phe import paillier


def display_popup_message(message, title="Admin Client - Message"):
    popup_window = wx.MessageDialog(None, message, title, wx.STAY_ON_TOP)
    popup_window.ShowModal()


class Controller:
    def __init__(self, model, view, request_handler):
        self.model = model
        self.view = view
        self.request_handler = request_handler

        # start by showing login screen
        self.view.show_login_view()

        # bind buttons to function in both screens
        self.view.bind_login(wx.EVT_BUTTON, self.on_login)
        self.view.bind_add_campaign(wx.EVT_BUTTON, self.on_add_campaign)
        self.view.bind_activate_campaign(wx.EVT_BUTTON, self.on_activate_campaign)
        self.view.bind_add_voter(wx.EVT_BUTTON, self.on_add_voter)
        self.view.bind_add_voter_to_campaign(wx.EVT_BUTTON, self.on_add_voter_to_campaign)
        self.view.bind_add_nominee_to_campaign(wx.EVT_BUTTON, self.on_add_nominee_to_campaign)
        self.view.bind_get_results(wx.EVT_BUTTON, self.on_get_results)
        self.view.login_view.bind_username_input(wx.EVT_TEXT, self.on_input_change)
        self.view.login_view.bind_password_input(wx.EVT_TEXT, self.on_input_change)

    def on_login(self, event):
        # get username and password and try to auth
        username, password = self.view.get_login_credentials()

        if not username or not password:
            display_popup_message("Invalid username or password", "Login Error")
            return

        try:
            success, reason = self.request_handler.auth(username, password)
        except ConnectionError as e:
            display_popup_message("Server Disconnected", "Connection Error")
        # if success, move to main view, init the main screen and save that we are logged in
        if success:
            self.view.show_main_view()
            self.model.toggle_auth()
            self.update_time()
            self.view.Layout()
            self.view.set_welcome_message(username)
            self.populate_campaign_choices()
        else:
            display_popup_message(reason, "Login Error")

    def update_time(self):
        # every second call this again to update the time text
        self.view.update_time()
        wx.CallLater(1000, self.update_time)

    def on_input_change(self, event):
        username, password = self.view.get_login_credentials()
        if username and password:
            self.view.login_view.enable_login_button()
        else:
            self.view.login_view.disable_login_button()

    def populate_campaign_choices(self):
        # get all available campaigns
        campaigns = self.request_handler.get_campaigns_list()
        # set campaign choices in UI to be the name of all the available campaigns
        self.view.set_campaigns_choices([campaign[2] for campaign in campaigns])
        self.model.set_campaigns(campaigns)

    def on_add_campaign(self, event):
        inputs = self.view.get_add_campaign_input()
        public_key, private_key = paillier.generate_paillier_keypair()  # generate public and private keys
        # save both keys as str
        public_key_str = f'{public_key.n}'
        private_key_str = f'{private_key.p}, {private_key.q}'
        uid = str(uuid.uuid4())  # get a random 128 bit uuid
        # send the request

        try:
            success, reason = self.request_handler.add_campaign(inputs[0], uid, inputs[1], inputs[2], public_key_str)
        except ConnectionError as e:
            display_popup_message("Server Disconnected", "Connection Error")

        # act on success or failure
        title = "Add Campaign Result"
        if success:
            message = "Success."
            self.model.add_campaign(uid, inputs[0], public_key_str, private_key_str)
            self.populate_campaign_choices()
        else:
            message = reason

        display_popup_message(message, title)

    def on_activate_campaign(self, event):
        # send inputs and send request
        campaign_index = self.view.get_activate_campaign_input()
        if campaign_index is wx.NOT_FOUND:
            display_popup_message("Please select a campaign")
            return
        campaign_id = self.model.get_campaign_by_index(campaign_index)[0]

        try:
            success, reason = self.request_handler.activate_campaign(campaign_id)
        except ConnectionError as e:
            display_popup_message("Server Disconnected", "Connection Error")

        # act on success or failure
        title = "Activate Campaign Result"
        if success:
            message = "Success."
        else:
            message = reason

        display_popup_message(message, title)

    def on_add_voter(self, event):
        inputs = self.view.get_add_voter_input()

        try:
            success, reason = self.request_handler.add_voter(*inputs)
        except ConnectionError as e:
            display_popup_message("Server Disconnected", "Connection Error")

        # act on success or failure
        title = "Add Voter Result"
        if success:
            message = "Success."
        else:
            message = reason

        display_popup_message(message, title)

    def on_add_voter_to_campaign(self, event):
        voter_name, campaign_index = self.view.get_add_voter_to_campaign_input()
        if campaign_index is wx.NOT_FOUND:
            display_popup_message("Please select a campaign")
            return
        campaign_name = self.model.get_campaign_by_index(campaign_index)[1]
        campaign_id = self.model.get_campaign_id(campaign_name)

        try:
            success, reason = self.request_handler.add_voter_to_campaign(voter_name, campaign_id)
        except ConnectionError as e:
            display_popup_message("Server Disconnected", "Connection Error")

        # act on success or failure
        title = "Add Voter To Campaign Result"
        if success:
            message = "Success."
        else:
            message = reason

        display_popup_message(message, title)

    def on_add_nominee_to_campaign(self, event):
        nominee_name, campaign_index = self.view.get_add_nominee_to_campaign_input()
        if campaign_index is wx.NOT_FOUND:
            display_popup_message("Please select a campaign")
            return
        campaign_name = self.model.get_campaign_by_index(campaign_index)[1]
        campaign_id = self.model.get_campaign_id(campaign_name)

        try:
            success, reason = self.request_handler.add_nominee_to_campaign(nominee_name, campaign_id)
        except ConnectionError as e:
            display_popup_message("Server Disconnected", "Connection Error")

        # act on success or failure
        title = "Add Nominee To Campaign Result"
        if success:
            message = "Success."
        else:
            message = reason

        display_popup_message(message, title)

    def on_get_results(self, event):
        # get campaign input and process the input
        campaign_index = self.view.get_get_results_input()
        if campaign_index is wx.NOT_FOUND:
            display_popup_message("Please select a campaign")
            return
        campaign = self.model.get_campaign_by_index(campaign_index)
        campaign_id = campaign[0]
        campaign_remote_id = campaign[1]

        try:
            results = self.request_handler.get_campaign_results(campaign_id)

            # get info on campaign from server
            campaign_server_info = None
            campaign_server_info = self.request_handler.get_campaign_info(campaign_id)
        except ConnectionError as e:
            display_popup_message("Server Disconnected", "Connection Error")

        # get info on campaign from local database
        campaign_info = self.model.get_campaign_info(campaign_remote_id)
        # setup public and private keys
        public_key_str = campaign_info['public_key']
        private_key_str = campaign_info['private_key']
        p_str, q_str = private_key_str.split(',')

        public_key = paillier.PaillierPublicKey(int(public_key_str))
        private_key = paillier.PaillierPrivateKey(public_key, int(p_str), int(q_str))

        # decrypt results
        total_votes = {i: private_key.decrypt(paillier.EncryptedNumber(public_key, int(tally))) for
                       i, tally
                       in results.items()}

        # print results to console
        print(f"Campaign '{campaign[2]}' results:")
        print(f"Total votes: {campaign_server_info['votes']}")
        print(f"Total voters: {campaign_server_info['voters']}")
        for i, tally in total_votes.items():
            nominee_name = campaign_server_info['nominees'][int(i)][1]
            print(f"Total votes for candidate {nominee_name}: {tally}")

        # save results to file
        with open(f"results_{campaign_id}", "w") as file:
            file.write(f"Campaign '{campaign[2]}' results:\n")
            file.write(f"Total votes: {campaign_server_info['votes']}\n")
            file.write(f"Total voters: {campaign_server_info['voters']}\n")
            for i, tally in total_votes.items():
                nominee_name = campaign_server_info['nominees'][int(i)][1]
                file.write(f"Total votes for candidate {nominee_name}: {tally}\n")
