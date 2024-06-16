class Model:
    def __init__(self):
        self.is_auth = False
        self.public_key = None
        self.campaigns = []
        self.nominees = []

    def is_auth(self):
        return self.is_auth

    def toggle_auth(self):
        self.is_auth = not self.is_auth

    def get_campaign_id_from_name(self, campaign_name):
        for campaign in self.campaigns:
            if campaign[2] == campaign_name:
                return campaign[0]
        return None

    def get_nominee_id_from_name(self, nominee_name):
        for nominee in self.nominees:
            if nominee[1] == nominee_name:
                return nominee[0]
        return None

    def set_campaigns(self, campaigns):
        self.campaigns = campaigns

    def get_campaign_by_index(self, index):
        return self.campaigns[index]
