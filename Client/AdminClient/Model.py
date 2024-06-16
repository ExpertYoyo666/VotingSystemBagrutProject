from DAL import DAL


class Model:
    def __init__(self):
        self.DAL = DAL()
        self.is_auth = False
        self.campaigns = []

    def is_auth(self):
        return self.is_auth

    def toggle_auth(self):
        self.is_auth = not self.is_auth

    def get_campaign_id(self, campaign_name):
        return next(x[0] for x in self.campaigns if x[1] == campaign_name)

    def set_campaigns(self, campaigns):
        self.campaigns = campaigns

    def get_campaign_by_index(self, index):
        return self.campaigns[index]

    def add_campaign(self, uid, campaign_name, public_key, private_key):
        self.DAL.add_campaign(uid, campaign_name, public_key, private_key)

    def get_campaign_info(self, remote_campaign_id):
        return self.DAL.get_campaign_info(remote_campaign_id)
