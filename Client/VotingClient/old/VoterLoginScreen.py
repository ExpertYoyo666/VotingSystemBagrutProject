from Client.VotingClient.old import VoterLoginFrame
import wx


class VoterLoginScreen(VoterLoginFrame.VoterLoginFrame):
    def __init__(self):
        app = wx.App()
        super(VoterLoginScreen, self).__init__(None)
        self.Show()

        self.bind_login_button(wx.EVT_BUTTON, self.on_login_press)

        app.MainLoop()

    def on_login_press(self, event):
        username = self.get_username_input()
        password = self.get_password_input()

        popup_window = wx.MessageDialog(None, f"username: {username}\npassword: {password}", "bob", wx.STAY_ON_TOP)
        popup_window.ShowModal()


if __name__ == '__main__':
    x = VoterLoginScreen()
