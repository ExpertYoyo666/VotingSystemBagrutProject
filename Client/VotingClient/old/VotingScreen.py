import wx
from abc import abstractmethod
from datetime import datetime




class VoterCampaignManager(VoterCampaignFrame):
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