import json
from enum import Enum

from DAL import DAL


class RequestType(Enum):
    REG_REQUEST = "REG_REQUEST"
    REG_RESPONSE = "REG_RESPONSE"
    AUTH_REQUEST = "REG_RESPONSE"
    AUTH_RESPONSE = "REG_RESPONSE"
    BALLOT_REQUEST = "BALLOT_REQUEST"
    BALLOT_RESPONSE = "BALLOT_RESPONSE"
    VOTE_REQUEST = "VOTE_REQUEST"
    VOTE_RESPONSE = "VOTE_RESPONSE"
    CAMPAIGN_LIST_REQUEST = "CAMPAIGN_LIST_REQUEST"
    CAMPAIGN_LIST_RESPONSE = "CAMPAIGN_LIST_RESPONSE"
    ERROR = "ERROR"


class RequestHandler:
    def __init__(self):
        self.dal = DAL()
        pass

    def handle_request(self, request_str):
        request = json.loads(request_str)

        match request["type"]:
            case RequestType.REG_REQUEST:
                response = self.handle_register(request)
            case RequestType.AUTH_REQUEST:
                response = self.handle_auth(request)
            case RequestType.BALLOT_REQUEST:
                response = self.handle_ballot_request(request)
            case RequestType.VOTE_REQUEST:
                response = self.handle_vote(request)
            case RequestType.CAMPAIGN_LIST_REQUEST:
                response = self.handle_campaign_list_request(request)
            case _:
                response = self.handle_error(request, "Invalid request type.")

        return response

    def handle_register(self, request):
        return 1

    def handle_auth(self, request):
        return 1

    def handle_ballot_request(self, request):
        return 1

    def handle_vote(self, request):
        return 1

    def handle_campaign_list_request(self, request):
        return 1

    def handle_error(self, request, message):
        return 1


if __name__ == '__main__':
    r = RequestHandler()
    x = {
        "type": "REG_REQUEST",
        "username": "yoyo666",
        "password": "bomba!1234"
    }
    print(r.handle_request(json.dumps(x)))
