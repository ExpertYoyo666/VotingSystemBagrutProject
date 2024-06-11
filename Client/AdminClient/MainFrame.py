import wx

from Client.AdminClient.Controller import Controller
from Client.AdminClient.Model import Model
from Client.AdminClient.Protocol import Protocol
from LoginView import LoginView
from MainView import MainView


class MainFrame(wx.Frame):
    def __init__(self, title):
        super(MainFrame, self).__init__(None, title=title, size=(800, 600))
        self.login_view = LoginView(self)
        self.main_view = MainView(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.login_view, 1, wx.EXPAND)
        self.sizer.Add(self.main_view, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.show_login_view()
        self.Centre()

    def show_login_view(self):
        self.login_view.Show()
        self.main_view.Hide()

    def show_main_view(self):
        self.login_view.Hide()
        self.main_view.Show()

    def bind_login(self, event, target):
        self.login_view.bind_login(event, target)

    def get_login_credentials(self):
        return self.login_view.get_username_input(), self.login_view.get_password_input()


if __name__ == '__main__':
    app = wx.App()
    model = Model()
    main_frame = MainFrame("Voting System")
    main_frame.Show()
    protocol = Protocol()
    c = Controller(model, main_frame, protocol)

    app.MainLoop()
