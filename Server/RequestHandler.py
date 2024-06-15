import json
from enum import Enum
import bcrypt as bcrypt

from VoteHandler import generate_keys, validate_vote_signature, tally_votes_in_batches, decrypt_results


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
    ACTIVATE_CAMPAIGN_REQUEST = "ACTIVATE_CAMPAIGN_REQUEST"
    ASSIGN_VOTER_TO_CAMPAIGN_REQUEST = "ASSIGN_VOTER_TO_CAMPAIGN_REQUEST"
    ADD_VOTER_REQUEST = "ADD_VOTER_REQUEST"
    ADD_NOMINEE_REQUEST = "ADD_NOMINEE_REQUEST"
    GET_RESULTS_REQUEST = "GET_RESULTS_REQUEST"

    GENERIC_RESPONSE = "GENERIC_RESPONSE"


class RequestHandler:
    def __init__(self, dal):
        self.dal = dal

    def handle_request(self, request_str, state):
        request = json.loads(request_str)
        is_auth = state["is_auth"]
        is_admin = state["is_admin"]

        response = {
            "type": RequestType.GENERIC_RESPONSE.value,
            "status": "FAILED"
        }

        match request["type"]:
            case RequestType.AUTH_REQUEST.value:
                if not is_auth:
                    response, voter_id, auth_ok = self.handle_auth(request)
                    if auth_ok:
                        state["is_auth"] = True
                        state["uid"] = voter_id
            case RequestType.CAMPAIGN_LIST_REQUEST.value:
                if is_auth:
                    response = self.handle_campaign_list_request(request, is_admin, state["uid"])
            case RequestType.CAMPAIGN_INFO_REQUEST.value:
                if is_auth:
                    response = self.handle_campaign_info_request(request)
            case RequestType.VOTE_REQUEST.value:
                if is_auth and not is_admin:
                    response = self.handle_vote(request, state["uid"])
            case RequestType.ADMIN_AUTH_REQUEST.value:
                if not is_auth:
                    response, admin_id, auth_ok = self.handle_admin_auth(request)
                    if auth_ok:
                        state["is_auth"] = True
                        state["is_admin"] = True
                        state["uid"] = admin_id
            case RequestType.ADD_CAMPAIGN_REQUEST.value:
                if is_auth and is_admin:
                    response = self.handle_add_campaign(request)
            case RequestType.ACTIVATE_CAMPAIGN_REQUEST.value:
                if is_auth and is_admin:
                    response = self.handle_activate_campaign(request)
            case RequestType.ADD_NOMINEE_REQUEST.value:
                if is_auth and is_admin:
                    response = self.handle_add_nominee(request)
            case RequestType.ADD_VOTER_REQUEST.value:
                if is_auth and is_admin:
                    response = self.handle_add_voter(request)
            case RequestType.GET_RESULTS_REQUEST.value:
                if is_auth and is_admin:
                    response = self.handle_get_results(request)
            case RequestType.ASSIGN_VOTER_TO_CAMPAIGN_REQUEST.value:
                if is_auth and is_admin:
                    response = self.handle_assign_voter_to_campaign_request(request)

        return response

    def handle_auth(self, request):
        username = request["username"]
        password = request["password"]

        response = {
            "type": RequestType.AUTH_RESPONSE.value,
            "status": "FAILED"
        }

        voter = self.dal.get_voter(username)
        if voter is not None and bcrypt.checkpw(password.encode(), voter[2]):
            response["status"] = "SUCCESS"
            return response, voter[0], True

        return response, None, False

    def handle_campaign_info_request(self, request):
        campaign_id = request["campaign_id"]

        nominees_list, public_key = self.dal.get_campaign_info(campaign_id)

        response = {
            "type": RequestType.CAMPAIGN_INFO_RESPONSE.value,
            "nominees": nominees_list,
            "public_key": public_key
        }

        return response

    def handle_vote(self, request, voter_id):
        campaign_id = request["campaign_id"]
        nonce = request["nonce"]
        encrypted_vote = request["encrypted_vote"]

        response = {
            "type": RequestType.VOTE_RESPONSE.value,
            "status": "FAIL",
            "verification_code": "N/A"
        }

        if self.dal_campaign_info()[2]:
            print("Campaign not active!")

        if validate_vote_signature(request):
            print("Vote is valid")
            self.dal.add_vote(nonce, voter_id, campaign_id, json.dumps(encrypted_vote))
            response["status"] = "SUCCESS"

        return response

    def handle_campaign_list_request(self, request, is_admin, voter_id):
        campaigns = self.dal.get_campaign_list(voter_id, is_admin)

        response = {
            "type": RequestType.CAMPAIGN_LIST_RESPONSE.value,
            "campaigns": campaigns
        }

        return response

    def handle_add_campaign(self, request):
        campaign_name = request["name"]
        start_timestamp = request["start_timestamp"]
        end_timestamp = request["end_timestamp"]
        public_key, private_key = generate_keys()

        public_key_str = f'{public_key.n}'
        private_key_str = f'{private_key.p} {private_key.q}'

        self.dal.add_campaign(campaign_name, start_timestamp, end_timestamp, public_key_str, private_key_str)

        response = {
            "type": RequestType.GENERIC_RESPONSE.value,
            "status": "SUCCESS"
        }

        return response

    def handle_activate_campaign(self, request):
        campaign_id = request["campaign_id"]

        self.dal.activate_campaign(campaign_id)

        response = {
            "type": RequestType.GENERIC_RESPONSE.value,
            "status": "SUCCESS"
        }

        return response

    def handle_admin_auth(self, request):
        username = request["username"]
        password = request["password"]

        response = {
            "type": RequestType.ADMIN_AUTH_RESPONSE.value,
            "status": "FAILED"
        }

        admin = self.dal.get_admin(username)
        if admin is not None and bcrypt.checkpw(password.encode(), admin[2]):
            response["status"] = "SUCCESS"
            return response, admin[0], True

        return response, None, False

    def handle_add_nominee(self, request):
        campaign_id = request["campaign_id"]
        name = request["name"]

        is_activated = self.dal.get_campaign_info(campaign_id)[2]
        response = {
            "type": RequestType.GENERIC_RESPONSE.value
        }

        if not is_activated:
            self.dal.add_nominee_to_campaign(campaign_id, name)

            response["status"] = "SUCCESS"
        else:
            response["status"] = "FAILED"

        return response

    def handle_add_voter(self, request):
        username = request["username"]
        password = request["password"]
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        response = {
            "type": RequestType.GENERIC_RESPONSE.value
        }
        if not self.dal.get_voter(username):
            self.dal.add_voter(username, hashed_password, "")
            response["status"] = "SUCCESS"
        else:
            response["status"] = "FAILED"

        return response

    def handle_get_results(self, request):
        return 1

    def handle_assign_voter_to_campaign_request(self, request):
        voter_name = request["voter_name"]
        campaign_id = request["campaign_id"]

        voter_id = self.dal.get_voter(voter_name)[0]
        self.dal.assign_voter_to_campaign(voter_id, campaign_id)

        response = {
            "type": RequestType.GENERIC_RESPONSE.value,
            "status": "SUCCESS"
        }

        return response
