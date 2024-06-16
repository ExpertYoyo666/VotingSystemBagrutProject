import wx
import wx.adv


class MainView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, pos=wx.DefaultPosition, size=wx.Size(800, 600),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        # main sizer that contains the entire panel
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # title sizers
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        title_sizer2 = wx.GridSizer(0, 2, 0, 0)

        # welcome message
        self.welcome_st = wx.StaticText(self, wx.ID_ANY, "Welcome", wx.DefaultPosition, wx.DefaultSize, 0)
        self.welcome_st.Wrap(-1)
        self.welcome_st.SetFont(
            wx.Font(22, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString))
        title_sizer2.Add(self.welcome_st, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        # time text
        self.time_st = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.time_st.Wrap(-1)
        self.time_st.SetFont(
            wx.Font(22, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString))
        title_sizer2.Add(self.time_st, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        title_sizer.Add(title_sizer2, 1, wx.EXPAND, 5)

        main_sizer.Add(title_sizer, 0, wx.EXPAND, 5)

        main_sizer.Add((0, 50), 0, wx.EXPAND, 5)

        body_sizer = wx.BoxSizer(wx.HORIZONTAL)

        left_body_sizer = wx.BoxSizer(wx.VERTICAL)

        # add campaign section
        add_campaign_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, wx.EmptyString), wx.VERTICAL)

        add_campaign_title_sizer = wx.BoxSizer(wx.VERTICAL)

        # title
        self.add_campaign_st = wx.StaticText(add_campaign_sizer.GetStaticBox(), wx.ID_ANY, "Add Campaign",
                                             wx.DefaultPosition, wx.DefaultSize, 0)
        self.add_campaign_st.Wrap(-1)
        self.add_campaign_st.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True, wx.EmptyString))
        add_campaign_title_sizer.Add(self.add_campaign_st, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        add_campaign_sizer.Add(add_campaign_title_sizer, 0, wx.EXPAND, 5)

        add_campaign_input_sizer = wx.FlexGridSizer(0, 2, 0, 0)
        add_campaign_input_sizer.SetFlexibleDirection(wx.BOTH)
        add_campaign_input_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # campaign name text
        self.add_campaign_name_st = wx.StaticText(add_campaign_sizer.GetStaticBox(), wx.ID_ANY,
                                                  "Campaign Name:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.add_campaign_name_st.Wrap(-1)
        self.add_campaign_name_st.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True, wx.EmptyString))
        add_campaign_input_sizer.Add(self.add_campaign_name_st, 0, wx.ALL, 5)

        # campaign name input
        self.add_campaign_name_input = wx.TextCtrl(add_campaign_sizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                                   wx.DefaultPosition, wx.Size(180, -1), 0)
        self.add_campaign_name_input.SetFont(
            wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString))
        add_campaign_input_sizer.Add(self.add_campaign_name_input, 0, wx.ALL, 5)

        # start time text
        self.add_campaign_start_st = wx.StaticText(add_campaign_sizer.GetStaticBox(), wx.ID_ANY, "Start Time:",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
        self.add_campaign_start_st.Wrap(-1)
        self.add_campaign_start_st.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True, wx.EmptyString))
        add_campaign_input_sizer.Add(self.add_campaign_start_st, 0, wx.ALL, 5)

        # start time input
        add_campaign_start_time_sizer = wx.GridSizer(0, 2, 0, 0)
        self.start_dp = wx.adv.DatePickerCtrl(add_campaign_sizer.GetStaticBox(), wx.ID_ANY, wx.DefaultDateTime,
                                              wx.DefaultPosition, wx.Size(85, -1), wx.adv.DP_DEFAULT)
        self.start_dp.SetFont(
            wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString))
        add_campaign_start_time_sizer.Add(self.start_dp, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.start_tp = wx.adv.TimePickerCtrl(add_campaign_sizer.GetStaticBox(), wx.ID_ANY, wx.DefaultDateTime,
                                              wx.DefaultPosition, wx.Size(85, -1), wx.adv.TP_DEFAULT)
        self.start_tp.SetFont(
            wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString))
        add_campaign_start_time_sizer.Add(self.start_tp, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        add_campaign_input_sizer.Add(add_campaign_start_time_sizer, 1, wx.EXPAND, 5)

        # end time text
        self.add_campaign_end_st = wx.StaticText(add_campaign_sizer.GetStaticBox(), wx.ID_ANY, "End Time:",
                                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.add_campaign_end_st.Wrap(-1)
        self.add_campaign_end_st.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True, wx.EmptyString))
        add_campaign_input_sizer.Add(self.add_campaign_end_st, 0, wx.ALL, 5)

        # end time input
        add_campaign_end_time_sizer = wx.GridSizer(0, 2, 0, 0)
        self.end_dp = wx.adv.DatePickerCtrl(add_campaign_sizer.GetStaticBox(), wx.ID_ANY, wx.DefaultDateTime,
                                            wx.DefaultPosition, wx.Size(85, -1), wx.adv.DP_DEFAULT)
        self.end_dp.SetFont(
            wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString))
        add_campaign_end_time_sizer.Add(self.end_dp, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.end_tp = wx.adv.TimePickerCtrl(add_campaign_sizer.GetStaticBox(), wx.ID_ANY, wx.DefaultDateTime,
                                            wx.DefaultPosition, wx.Size(85, -1), wx.adv.TP_DEFAULT)
        self.end_tp.SetFont(
            wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString))
        add_campaign_end_time_sizer.Add(self.end_tp, 0, wx.ALIGN_CENTER, 5)
        add_campaign_input_sizer.Add(add_campaign_end_time_sizer, 1, wx.EXPAND, 5)

        add_campaign_sizer.Add(add_campaign_input_sizer, 0, wx.ALIGN_CENTER, 5)

        # add campaign submit button
        add_campaign_submit_sizer = wx.BoxSizer(wx.VERTICAL)
        self.add_campaign_button = wx.Button(add_campaign_sizer.GetStaticBox(), wx.ID_ANY, "Submit",
                                             wx.DefaultPosition, wx.DefaultSize, 0)
        self.add_campaign_button.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString))
        add_campaign_submit_sizer.Add(self.add_campaign_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        add_campaign_sizer.Add(add_campaign_submit_sizer, 0, wx.EXPAND, 5)

        left_body_sizer.Add(add_campaign_sizer, 0, wx.EXPAND, 5)

        # activate campaign section
        activate_campaign_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, wx.EmptyString), wx.VERTICAL)

        # title
        activate_campaign_title_sizer = wx.BoxSizer(wx.VERTICAL)
        self.activate_campaign_st = wx.StaticText(activate_campaign_sizer.GetStaticBox(), wx.ID_ANY,
                                                  "Activate Campaign", wx.DefaultPosition, wx.DefaultSize, 0)
        self.activate_campaign_st.Wrap(-1)
        self.activate_campaign_st.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True, wx.EmptyString))
        activate_campaign_title_sizer.Add(self.activate_campaign_st, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        activate_campaign_sizer.Add(activate_campaign_title_sizer, 1, wx.EXPAND, 5)

        # input
        activate_campaign_input_sizer = wx.FlexGridSizer(0, 2, 0, 0)
        activate_campaign_input_sizer.SetFlexibleDirection(wx.BOTH)
        activate_campaign_input_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # campaign name text
        self.activate_campaign_name_st = wx.StaticText(activate_campaign_sizer.GetStaticBox(), wx.ID_ANY,
                                                       "Campaign Name:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.activate_campaign_name_st.Wrap(-1)
        self.activate_campaign_name_st.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True, wx.EmptyString))
        activate_campaign_input_sizer.Add(self.activate_campaign_name_st, 0, wx.ALL, 5)

        # campaign name choice
        self.activate_campaign_name_choice = wx.Choice(activate_campaign_sizer.GetStaticBox(), wx.ID_ANY,
                                                       wx.DefaultPosition, wx.Size(180, -1), [], 0)
        self.activate_campaign_name_choice.SetSelection(0)
        self.activate_campaign_name_choice.SetFont(
            wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString))
        activate_campaign_input_sizer.Add(self.activate_campaign_name_choice, 0, wx.ALL, 5)

        activate_campaign_sizer.Add(activate_campaign_input_sizer, 1, wx.ALIGN_CENTER, 5)

        # submit
        activate_campaign_submit_sizer = wx.BoxSizer(wx.VERTICAL)

        # submit button
        self.activate_campaign_button = wx.Button(activate_campaign_sizer.GetStaticBox(), wx.ID_ANY, "Submit",
                                                  wx.DefaultPosition, wx.DefaultSize, 0)
        self.activate_campaign_button.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString))
        activate_campaign_submit_sizer.Add(self.activate_campaign_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        activate_campaign_sizer.Add(activate_campaign_submit_sizer, 1, wx.EXPAND, 5)

        left_body_sizer.Add(activate_campaign_sizer, 1, wx.EXPAND, 5)

        # add voter section
        add_voter_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, wx.EmptyString), wx.VERTICAL)

        # title
        add_sizer_title_sizer = wx.BoxSizer(wx.VERTICAL)
        self.add_voter_st = wx.StaticText(add_voter_sizer.GetStaticBox(), wx.ID_ANY, "Add Voter",
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        self.add_voter_st.Wrap(-1)
        self.add_voter_st.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True, wx.EmptyString))
        add_sizer_title_sizer.Add(self.add_voter_st, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        add_voter_sizer.Add(add_sizer_title_sizer, 0, wx.EXPAND, 5)

        # input
        add_voter_input_sizer = wx.FlexGridSizer(0, 2, 0, 0)
        add_voter_input_sizer.SetFlexibleDirection(wx.BOTH)
        add_voter_input_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # voter name text
        self.add_voter_name_st = wx.StaticText(add_voter_sizer.GetStaticBox(), wx.ID_ANY, "Name:",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.add_voter_name_st.Wrap(-1)
        self.add_voter_name_st.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True, wx.EmptyString))
        add_voter_input_sizer.Add(self.add_voter_name_st, 0, wx.ALL, 5)

        # voter name input
        self.add_voter_name_input = wx.TextCtrl(add_voter_sizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                                wx.DefaultPosition, wx.Size(180, -1), 0)
        self.add_voter_name_input.SetFont(
            wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString))
        add_voter_input_sizer.Add(self.add_voter_name_input, 0, wx.ALL, 5)

        # voter password text
        self.add_voter_password_st = wx.StaticText(add_voter_sizer.GetStaticBox(), wx.ID_ANY, "Password:",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
        self.add_voter_password_st.Wrap(-1)
        self.add_voter_password_st.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True, wx.EmptyString))
        add_voter_input_sizer.Add(self.add_voter_password_st, 0, wx.ALL, 5)

        # voter password input
        self.add_voter_password_input = wx.TextCtrl(add_voter_sizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                                    wx.DefaultPosition, wx.Size(180, -1), 0)
        add_voter_input_sizer.Add(self.add_voter_password_input, 0, wx.ALL, 5)
        add_voter_sizer.Add(add_voter_input_sizer, 0, wx.ALIGN_CENTER, 5)

        # submit
        add_voter_submit_sizer = wx.BoxSizer(wx.VERTICAL)

        # submit button
        self.add_voter_button = wx.Button(add_voter_sizer.GetStaticBox(), wx.ID_ANY, "Submit",
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        self.add_voter_button.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString))
        add_voter_submit_sizer.Add(self.add_voter_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        add_voter_sizer.Add(add_voter_submit_sizer, 0, wx.EXPAND, 5)

        left_body_sizer.Add(add_voter_sizer, 1, wx.EXPAND, 5)

        body_sizer.Add(left_body_sizer, 1, wx.EXPAND, 5)

        right_body_sizer = wx.BoxSizer(wx.VERTICAL)

        # add voter to campaign section
        add_voter_to_campaign_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, wx.EmptyString), wx.VERTICAL)

        # title
        add_voter_to_campaign_title_sizer = wx.BoxSizer(wx.VERTICAL)
        # title text
        self.add_voter_to_campaign_title_st = wx.StaticText(add_voter_to_campaign_sizer.GetStaticBox(), wx.ID_ANY,
                                                            "Add Voter To Campaign", wx.DefaultPosition,
                                                            wx.DefaultSize, 0)
        self.add_voter_to_campaign_title_st.Wrap(-1)
        self.add_voter_to_campaign_title_st.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True, wx.EmptyString))
        add_voter_to_campaign_title_sizer.Add(self.add_voter_to_campaign_title_st, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        add_voter_to_campaign_sizer.Add(add_voter_to_campaign_title_sizer, 0, wx.EXPAND, 5)

        # input
        add_voter_to_campaign_input_sizer = wx.FlexGridSizer(0, 2, 0, 0)
        add_voter_to_campaign_input_sizer.SetFlexibleDirection(wx.BOTH)
        add_voter_to_campaign_input_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # voter name text
        self.add_voter_to_campaign_voter_name_st = wx.StaticText(add_voter_to_campaign_sizer.GetStaticBox(),
                                                                 wx.ID_ANY, "Voter Name:", wx.DefaultPosition,
                                                                 wx.DefaultSize, 0)
        self.add_voter_to_campaign_voter_name_st.Wrap(-1)
        self.add_voter_to_campaign_voter_name_st.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True, wx.EmptyString))
        add_voter_to_campaign_input_sizer.Add(self.add_voter_to_campaign_voter_name_st, 0, wx.ALL, 5)

        # voter name input
        self.add_voter_to_campaign_voter_name_input = wx.TextCtrl(add_voter_to_campaign_sizer.GetStaticBox(),
                                                                  wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                                  wx.Size(180, -1), 0)
        self.add_voter_to_campaign_voter_name_input.SetFont(
            wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString))
        add_voter_to_campaign_input_sizer.Add(self.add_voter_to_campaign_voter_name_input, 0, wx.ALL, 5)

        # campaign name text
        self.add_voter_to_campaign_campaign_name_st = wx.StaticText(add_voter_to_campaign_sizer.GetStaticBox(),
                                                                    wx.ID_ANY, "Campaign Name:",
                                                                    wx.DefaultPosition, wx.DefaultSize, 0)
        self.add_voter_to_campaign_campaign_name_st.Wrap(-1)
        self.add_voter_to_campaign_campaign_name_st.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True, wx.EmptyString))
        add_voter_to_campaign_input_sizer.Add(self.add_voter_to_campaign_campaign_name_st, 0, wx.ALL, 5)

        # campaign name choice
        self.add_voter_to_campaign_campaign_name_choice = wx.Choice(add_voter_to_campaign_sizer.GetStaticBox(),
                                                                    wx.ID_ANY, wx.DefaultPosition, wx.Size(180, -1), [],
                                                                    0)
        self.add_voter_to_campaign_campaign_name_choice.SetSelection(0)
        add_voter_to_campaign_input_sizer.Add(self.add_voter_to_campaign_campaign_name_choice, 0, wx.ALL, 5)
        self.add_voter_to_campaign_campaign_name_choice.SetFont(
            wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString))

        add_voter_to_campaign_sizer.Add(add_voter_to_campaign_input_sizer, 0, wx.ALIGN_CENTER, 5)

        # submit
        add_voter_to_campaign_submit_sizer = wx.BoxSizer(wx.VERTICAL)

        # submit button
        self.add_voter_to_campaign_button = wx.Button(add_voter_to_campaign_sizer.GetStaticBox(), wx.ID_ANY,
                                                      "Submit", wx.DefaultPosition, wx.DefaultSize, 0)
        self.add_voter_to_campaign_button.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString))
        add_voter_to_campaign_submit_sizer.Add(self.add_voter_to_campaign_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        add_voter_to_campaign_sizer.Add(add_voter_to_campaign_submit_sizer, 0, wx.EXPAND, 5)

        right_body_sizer.Add(add_voter_to_campaign_sizer, 0, wx.EXPAND, 5)

        # add nominee to campaign section
        add_nominee_to_campaign_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, wx.EmptyString), wx.VERTICAL)

        # title
        add_nominee_to_campaign_title_sizer = wx.BoxSizer(wx.VERTICAL)

        # title text
        self.add_nominee_to_campaign_title_st = wx.StaticText(add_nominee_to_campaign_sizer.GetStaticBox(),
                                                              wx.ID_ANY, "Add Nominee To Campaign",
                                                              wx.DefaultPosition, wx.DefaultSize, 0)
        self.add_nominee_to_campaign_title_st.Wrap(-1)
        self.add_nominee_to_campaign_title_st.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True, wx.EmptyString))
        add_nominee_to_campaign_title_sizer.Add(self.add_nominee_to_campaign_title_st, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        add_nominee_to_campaign_sizer.Add(add_nominee_to_campaign_title_sizer, 0, wx.EXPAND, 5)

        # input
        add_nominee_to_campaign_input_sizer = wx.FlexGridSizer(0, 2, 0, 0)
        add_nominee_to_campaign_input_sizer.SetFlexibleDirection(wx.BOTH)
        add_nominee_to_campaign_input_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # nominee name text
        self.add_nominee_to_campaign_nominee_name_st = wx.StaticText(add_nominee_to_campaign_sizer.GetStaticBox(),
                                                                     wx.ID_ANY, "Nominee Name:",
                                                                     wx.DefaultPosition, wx.DefaultSize, 0)
        self.add_nominee_to_campaign_nominee_name_st.Wrap(-1)
        self.add_nominee_to_campaign_nominee_name_st.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True, wx.EmptyString))
        add_nominee_to_campaign_input_sizer.Add(self.add_nominee_to_campaign_nominee_name_st, 0, wx.ALL, 5)

        # nominee name input
        self.add_nominee_to_campaign_nominee_name_input = wx.TextCtrl(add_nominee_to_campaign_sizer.GetStaticBox(),
                                                                      wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                                      wx.Size(180, -1), 0)
        self.add_nominee_to_campaign_nominee_name_input.SetFont(
            wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString))
        add_nominee_to_campaign_input_sizer.Add(self.add_nominee_to_campaign_nominee_name_input, 0, wx.ALL, 5)

        # campaign name text
        self.add_nominee_to_campaign_campaign_name_st = wx.StaticText(add_nominee_to_campaign_sizer.GetStaticBox(),
                                                                      wx.ID_ANY, "Campaign Name:",
                                                                      wx.DefaultPosition, wx.DefaultSize, 0)
        self.add_nominee_to_campaign_campaign_name_st.Wrap(-1)
        self.add_nominee_to_campaign_campaign_name_st.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True, wx.EmptyString))

        # campaign name choice
        add_nominee_to_campaign_input_sizer.Add(self.add_nominee_to_campaign_campaign_name_st, 0, wx.ALL, 5)

        self.add_nominee_to_campaign_campaign_name_choice = wx.Choice(add_nominee_to_campaign_sizer.GetStaticBox(),
                                                                      wx.ID_ANY, wx.DefaultPosition,
                                                                      wx.Size(180, -1), [], 0)
        self.add_nominee_to_campaign_campaign_name_choice.SetSelection(0)
        self.add_nominee_to_campaign_campaign_name_choice.SetFont(
            wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString))
        add_nominee_to_campaign_input_sizer.Add(self.add_nominee_to_campaign_campaign_name_choice, 0, wx.ALL, 5)

        add_nominee_to_campaign_sizer.Add(add_nominee_to_campaign_input_sizer, 0, wx.ALIGN_CENTER, 5)

        # submit
        add_nominee_to_campaign_submit_sizer = wx.BoxSizer(wx.VERTICAL)

        # submit button
        self.add_nominee_to_campaign_button = wx.Button(add_nominee_to_campaign_sizer.GetStaticBox(), wx.ID_ANY,
                                                        "Submit", wx.DefaultPosition, wx.DefaultSize, 0)
        self.add_nominee_to_campaign_button.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString))
        add_nominee_to_campaign_submit_sizer.Add(self.add_nominee_to_campaign_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        add_nominee_to_campaign_sizer.Add(add_nominee_to_campaign_submit_sizer, 0, wx.EXPAND, 5)

        right_body_sizer.Add(add_nominee_to_campaign_sizer, 1, wx.EXPAND, 5)

        # get results section
        get_results_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, wx.EmptyString), wx.VERTICAL)

        # title
        get_results_title_sizer = wx.BoxSizer(wx.VERTICAL)

        # title text
        self.get_results_title_st = wx.StaticText(get_results_sizer.GetStaticBox(), wx.ID_ANY, "Get Results",
                                                  wx.DefaultPosition, wx.DefaultSize, 0)
        self.get_results_title_st.Wrap(-1)
        self.get_results_title_st.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True, wx.EmptyString))
        get_results_title_sizer.Add(self.get_results_title_st, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        get_results_sizer.Add(get_results_title_sizer, 0, wx.EXPAND, 5)

        # input
        get_results_input_sizer = wx.FlexGridSizer(0, 2, 0, 0)
        get_results_input_sizer.SetFlexibleDirection(wx.BOTH)
        get_results_input_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # campaign name text
        self.get_results_campaign_name_st = wx.StaticText(get_results_sizer.GetStaticBox(), wx.ID_ANY,
                                                          "Campaign Name:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.get_results_campaign_name_st.Wrap(-1)
        self.get_results_campaign_name_st.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True, wx.EmptyString))
        get_results_input_sizer.Add(self.get_results_campaign_name_st, 0, wx.ALL, 5)

        # campaign name choice
        self.get_results_campaign_name_choice = wx.Choice(get_results_sizer.GetStaticBox(), wx.ID_ANY,
                                                          wx.DefaultPosition, wx.Size(180, -1), [], 0)
        self.get_results_campaign_name_choice.SetSelection(0)
        self.get_results_campaign_name_choice.SetFont(
            wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString))
        get_results_input_sizer.Add(self.get_results_campaign_name_choice, 0, wx.ALL, 5)

        get_results_sizer.Add(get_results_input_sizer, 0, wx.ALIGN_CENTER, 5)

        # submit
        get_results_submit_sizer = wx.BoxSizer(wx.VERTICAL)

        # submit button
        self.get_results_button = wx.Button(get_results_sizer.GetStaticBox(), wx.ID_ANY, "Submit",
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        self.get_results_button.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString))
        get_results_submit_sizer.Add(self.get_results_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        get_results_sizer.Add(get_results_submit_sizer, 0, wx.EXPAND, 5)

        right_body_sizer.Add(get_results_sizer, 1, wx.EXPAND, 5)

        body_sizer.Add(right_body_sizer, 1, wx.EXPAND, 5)

        main_sizer.Add(body_sizer, 1, wx.EXPAND, 5)

        self.SetSizer(main_sizer)
        self.Layout()
        self.Centre(wx.BOTH)

    def get_add_campaign_input(self):
        campaign_name = self.add_campaign_name_input.GetValue()
        x = self.start_tp.GetValue()
        y = self.start_dp.GetValue()
        # convert start time to ticks (seconds since 1 Jan 1970)
        start_time = wx.DateTime(year=y.GetYear(), month=y.GetMonth(), day=y.GetDay(),
                                 hour=x.GetHour(), minute=x.GetMinute(), second=x.GetSecond()).GetTicks()

        x = self.end_tp.GetValue()
        y = self.end_dp.GetValue()
        # convert start time to ticks
        end_time = wx.DateTime(year=y.GetYear(), month=y.GetMonth(), day=y.GetDay(),
                               hour=x.GetHour(), minute=x.GetMinute(), second=x.GetSecond()).GetTicks()
        return campaign_name, start_time, end_time

    def get_activate_campaign_input(self):
        campaign_name = self.activate_campaign_name_choice.GetCurrentSelection()

        return campaign_name

    def get_add_voter_input(self):
        name = self.add_voter_name_input.GetValue()
        password = self.add_voter_password_input.GetValue()

        return name, password

    def get_add_voter_to_campaign_input(self):
        voter_name = self.add_voter_to_campaign_voter_name_input.GetValue()
        campaign_name = self.add_voter_to_campaign_campaign_name_choice.GetCurrentSelection()

        return voter_name, campaign_name

    def get_get_results_input(self):
        campaign_name = self.get_results_campaign_name_choice.GetCurrentSelection()

        return campaign_name

    def get_add_nominee_to_campaign_input(self):
        nominee_name = self.add_nominee_to_campaign_nominee_name_input.GetValue()
        campaign_name = self.add_nominee_to_campaign_campaign_name_choice.GetCurrentSelection()

        return nominee_name, campaign_name

    def set_welcome_message(self, username):
        self.welcome_st.SetLabel(f"Welcome {username}")
        self.Layout()

    def set_campaigns_choices(self, campaigns):
        self.activate_campaign_name_choice.SetItems(campaigns)
        self.add_voter_to_campaign_campaign_name_choice.SetItems(campaigns)
        self.get_results_campaign_name_choice.SetItems(campaigns)
        self.add_nominee_to_campaign_campaign_name_choice.SetItems(campaigns)

    def bind_add_campaign(self, event, target):
        self.add_campaign_button.Bind(event, target)

    def bind_activate_campaign(self, event, target):
        self.activate_campaign_button.Bind(event, target)

    def bind_add_voter(self, event, target):
        self.add_voter_button.Bind(event, target)

    def bind_add_voter_to_campaign(self, event, target):
        self.add_voter_to_campaign_button.Bind(event, target)

    def bind_add_nominee_to_campaign(self, event, target):
        self.add_nominee_to_campaign_button.Bind(event, target)

    def bind_get_results(self, event, target):
        self.get_results_button.Bind(event, target)

    def update_time(self, time_str):
        self.time_st.SetLabel(time_str)
