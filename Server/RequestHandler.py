import json
from enum import Enum

from DAL import DAL


class RequestType(Enum):
    AUTH_REQUEST = "AUTH_REQUEST"
    AUTH_RESPONSE = "AUTH_RESPONSE"
    CAMPAIGN_INFO_REQUEST = "CAMPAIGN_INFO_REQUEST"
    CAMPAIGN_INFO_RESPONSE = "CAMPAIGN_INFO_RESPONSE"
    VOTE_REQUEST = "VOTE_REQUEST"
    VOTE_RESPONSE = "VOTE_RESPONSE"
    CAMPAIGN_LIST_REQUEST = "CAMPAIGN_LIST_REQUEST"
    CAMPAIGN_LIST_RESPONSE = "CAMPAIGN_LIST_RESPONSE"
    ADMIN_AUTH_REQUEST = "ADMIN_AUTH_REQUEST"
    ADMIN_AUTH_RESPONSE = "ADMIN_AUTH_RESPONSE"
    ADD_CAMPAIGN_REQUEST = "ADD_CAMPAIGN_REQUEST"
    ASSIGN_VOTER_TO_CAMPAIGN_REQUEST = "ASSIGN_VOTER_TO_CAMPAIGN_REQUEST"
    ADD_VOTER_REQUEST = "ADD_VOTER_REQUEST"
    ADD_NOMINEE_REQUEST = "ADD_NOMINEE_REQUEST"
    GET_RESULTS_REQUEST = "GET_RESULTS_REQUEST"

    GENERIC_RESPONSE = "GENERIC_RESPONSE"


class RequestHandler:
    def __init__(self):
        self.dal = DAL()
        pass

    def handle_request(self, request_str, state):
        request = json.loads(request_str)
        is_auth = state["is_auth"]
        is_admin = state["is_admin"]

        response = {
            "type": RequestType.GENERIC_RESPONSE,
            "status": "Fail",
            "reason": "Invalid request"
        }

        match request["type"]:
            case RequestType.AUTH_REQUEST:
                if not is_auth:
                    response, voter_id, auth_ok = self.handle_auth(request)
                    if auth_ok:
                        state["is_auth"] = True
                        state["uid"] = voter_id
            case RequestType.CAMPAIGN_LIST_REQUEST:
                if is_auth:
                    response = self.handle_campaign_list_request(request, is_admin)
            case RequestType.CAMPAIGN_INFO_REQUEST:
                if is_auth:
                    response = self.handle_campaign_info_request(request)
            case RequestType.VOTE_REQUEST:
                if is_auth and not is_admin:
                    response = self.handle_vote(request)
            case RequestType.ADMIN_AUTH_REQUEST:
                if not is_auth:
                    response, admin_id, auth_ok = self.handle_admin_auth(request)
                    if auth_ok:
                        state["is_auth"] = True
                        state["is_admin"] = True
                        state["uid"] = admin_id
            case RequestType.ADD_CAMPAIGN_REQUEST:
                if is_auth and is_admin:
                    response = self.handle_add_campaign(request)
            case RequestType.ADD_NOMINEE_REQUEST:
                if is_auth and is_admin:
                    response = self.handle_add_nominee(request)
            case RequestType.ADD_VOTER_REQUEST:
                if is_auth and is_admin:
                    response = self.handle_add_voter(request)
            case RequestType.GET_RESULTS_REQUEST:
                if is_auth and is_admin:
                    response = self.handle_get_results(request)

        return response

    def handle_auth(self, request):
        username = request["username"]
        password = request["password"]

        voter = self.dal.get_voter(username)
        if voter.password == password:
            response = {
                "status": "SUCCESS"
            }

            return response, voter.voter_id, True

        response = {
            "status": "FAILED"
        }
        return response, voter.voter_id, False

    def handle_campaign_info_request(self, request):
        return 1

    def handle_vote(self, request):
        return 1

    def handle_campaign_list_request(self, request, is_admin):
        return 1

    def handle_error(self, request, message):
        return 1

    def handle_add_campaign(self, request):
        return 1

    def handle_admin_auth(self, request):
        username = request["username"]
        password = request["password"]

        admin = self.dal.get_admin(username)
        if admin.password == password:
            response = {
                "status": "SUCCESS"
            }

            return response, admin.admin_id, True

        response = {
            "status": "FAILED"
        }
        return response, admin.admin_id, False

    def handle_add_nominee(self, request):
        return 1

    def handle_add_voter(self, request):
        return 1

    def handle_get_results(self, request):
        return 1


if __name__ == '__main__':
    r = RequestHandler()
    x = {
        "type": "REG_REQUEST",
        "username": "yoyo666",
        "password": "bomba!1234"
    }
    print(r.handle_request(json.dumps(x)))
