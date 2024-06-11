import wx


class Controller:
    def __init__(self, model, view, request_handler):
        self.model = model
        self.view = view
        self.request_handler = request_handler

        self.view.show_login_view()
        self.view.bind_login(wx.EVT_BUTTON, self.on_login)

    def on_login(self, event):
        username, password = self.view.get_login_credentials()
        success = self.request_handler.auth(username, password)
        if success:
            self.view.show_main_view()
            self.model.toggle_auth()

