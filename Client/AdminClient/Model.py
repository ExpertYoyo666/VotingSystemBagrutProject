class Model:
    def __init__(self):
        self.is_auth = False

    def is_auth(self):
        return self.is_auth

    def toggle_auth(self):
        self.is_auth = not self.is_auth

