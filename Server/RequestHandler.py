import json
import time
from enum import Enum
import bcrypt as bcrypt
import shortuuid

from VoteHandler import validate_vote_signature, tally_votes_in_batches


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
    GET_RESULTS_RESPONSE = "GET_RESULTS_RESPONSE"

    GENERIC_RESPONSE = "GENERIC_RESPONSE"


class RequestHandler:
    def __init__(self, dal):
        self.dal = dal

    def handle_request(self, request_str, state):
        response = {
            "type": RequestType.GENERIC_RESPONSE.value,
            "status": "FAILED",
            "reason": "Expect JSON"
        }

        # Check if the request is a valid JSON
        if not request_str:
            return response

        request = json.loads(request_str)
        is_auth = state["is_auth"]
        is_admin = state["is_admin"]

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
        response = {
            "type": RequestType.AUTH_RESPONSE.value,
            "status": "FAILED",
            "reason": "Invalid request"
        }

        try:
            if "username" not in request or "password" not in request:
                response["reason"] = "Missing required fields"
                return response, None, False

            username = request["username"]
            password = request["password"]

            if not isinstance(username, str) or not isinstance(password, str):
                response["reason"] = "Invalid field types"
                return response, None, False

            voter = self.dal.get_voter(username)
            if voter is not None and bcrypt.checkpw(password.encode(), voter[2]):
                response["status"] = "SUCCESS"
                response["reason"] = ""
                return response, voter[0], True

            response["reason"] = "Authentication failed"
        except Exception as e:
            response["reason"] = str(e)

        return response, None, False

    def handle_campaign_info_request(self, request):
        response = {
            "type": RequestType.CAMPAIGN_INFO_RESPONSE.value,
            "status": "FAILED",
            "reason": "Invalid request"
        }

        try:
            if "campaign_id" not in request:
                response["reason"] = "Missing required field 'campaign_id'"
                return response

            campaign_id = request["campaign_id"]

            if not isinstance(campaign_id, int):
                response["reason"] = "Invalid field type for 'campaign_id'"
                return response

            campaign_info = self.dal.get_campaign_info(campaign_id)
            if campaign_info is None:
                response["reason"] = "Campaign not found"
                return response

            campaign_info["type"] = RequestType.CAMPAIGN_INFO_RESPONSE.value
            campaign_info["status"] = "SUCCESS"
            return campaign_info
        except Exception as e:
            response["reason"] = str(e)

        return response

    def handle_vote(self, request, voter_id):
        response = {
            "type": RequestType.VOTE_RESPONSE.value,
            "status": "FAIL",
            "reason": "Invalid request",
            "receipt": "0000-0000-0000-0000"
        }

        try:
            required_fields = ["campaign_id", "nonce", "encrypted_vote"]
            if not all(field in request for field in required_fields):
                response["reason"] = "Missing required fields"
                return response

            campaign_id = request["campaign_id"]
            nonce = request["nonce"]
            encrypted_vote = request["encrypted_vote"]

            if not isinstance(campaign_id, int) or not isinstance(nonce, str) or not isinstance(encrypted_vote, dict):
                response["reason"] = "Invalid field types"
                return response

            if nonce.strip() == "":
                response["reason"] = "Nonce cannot be empty"
                return response

            # check if voter already voted
            if self.dal.get_voter_has_voted(voter_id, campaign_id) == 1:
                response["reason"] = "Voter has already voted"
                return response

            # check if nonce is already used
            if self.dal.nonce_exists(nonce, campaign_id):
                response["reason"] = "Vote replay rejected"
                return response

            # check if campaign is active
            info = self.dal.get_campaign_info(campaign_id)
            if info is None:
                response["reason"] = "Campaign not found"
                return response

            if info['is_active'] != 1:
                response["reason"] = "Campaign not active"
                return response

            # check vote time in relation to campaign start and end times
            if not (info["start_timestamp"] <= time.time() <= info["end_timestamp"]):
                response["reason"] = "Campaign didn't start yet or expired"
                return response

            # validate signature
            if validate_vote_signature(request):
                short_uuid = shortuuid.ShortUUID().random(length=16)
                vote_receipt = '-'.join(short_uuid[i:i + 4] for i in range(0, 16, 4))
                self.dal.add_vote(nonce, campaign_id, vote_receipt, json.dumps(encrypted_vote))
                self.dal.set_voter_has_voted(voter_id, campaign_id)
                response["status"] = "SUCCESS"
                response["reason"] = "Vote accepted"
                response["receipt"] = vote_receipt
            else:
                response["reason"] = "Invalid vote signature"
        except Exception as e:
            response["reason"] = str(e)

        return response

    def handle_campaign_list_request(self, request, is_admin, voter_id):
        response = {
            "type": RequestType.CAMPAIGN_LIST_RESPONSE.value,
            "status": "FAILED",
            "reason": "Invalid request"
        }

        try:
            if not isinstance(is_admin, bool):
                response["reason"] = "Invalid field type for 'is_admin'"
                return response

            if not isinstance(voter_id, int):
                response["reason"] = "Invalid field type for 'voter_id'"
                return response

            campaigns = self.dal.get_campaign_list(voter_id, is_admin)

            response = {
                "type": RequestType.CAMPAIGN_LIST_RESPONSE.value,
                "status": "SUCCESS",
                "campaigns": campaigns
            }
        except Exception as e:
            response["reason"] = str(e)

        return response

    def handle_add_campaign(self, request):
        response = {
            "type": RequestType.GENERIC_RESPONSE.value,
            "status": "FAILED",
            "reason": "Invalid request"
        }

        try:
            required_fields = ["name", "id", "start_timestamp", "end_timestamp", "public_key"]
            if not all(field in request for field in required_fields):
                response["reason"] = "Missing required fields"
                return response

            campaign_name = request["name"]
            campaign_id = request["id"]
            start_timestamp = request["start_timestamp"]
            end_timestamp = request["end_timestamp"]
            public_key = request["public_key"]

            if not isinstance(campaign_name, str) or not isinstance(campaign_id, str) or \
                    not isinstance(start_timestamp, int) or not isinstance(end_timestamp, int) or \
                    not isinstance(public_key, str):
                response["reason"] = "Invalid field types"
                return response

            if campaign_name.strip() == "" or campaign_id.strip() == "":
                response["reason"] = "Campaign name and id cannot be empty"
                return response

            self.dal.add_campaign(campaign_name, campaign_id, start_timestamp, end_timestamp, public_key)

            response["status"] = "SUCCESS"
            response["reason"] = ""
        except Exception as e:
            response["reason"] = str(e)

        return response

    def handle_activate_campaign(self, request):
        response = {
            "type": RequestType.GENERIC_RESPONSE.value,
            "status": "FAILED",
            "reason": "Invalid request"
        }

        try:
            if "campaign_id" not in request:
                response["reason"] = "Missing required field 'campaign_id'"
                return response

            campaign_id = request["campaign_id"]

            if not isinstance(campaign_id, int):
                response["reason"] = "Invalid field type for 'campaign_id'"
                return response

            campaign_info = self.dal.get_campaign_info(campaign_id)
            if campaign_info is None:
                response["reason"] = "Campaign not found"
                return response

            self.dal.activate_campaign(campaign_id)

            response["status"] = "SUCCESS"
            response["reason"] = ""
        except Exception as e:
            response["reason"] = str(e)

        return response

    def handle_admin_auth(self, request):
        response = {
            "type": RequestType.ADMIN_AUTH_RESPONSE.value,
            "status": "FAILED",
            "reason": "Invalid request"
        }

        try:
            if "username" not in request or "password" not in request:
                response["reason"] = "Missing required fields"
                return response, None, False

            username = request["username"]
            password = request["password"]

            if not isinstance(username, str) or not isinstance(password, str):
                response["reason"] = "Invalid field types"
                return response, None, False

            admin = self.dal.get_admin(username)
            if admin is not None and bcrypt.checkpw(password.encode(), admin[2]):
                response["status"] = "SUCCESS"
                response["reason"] = ""
                return response, admin[0], True

            response["reason"] = "Authentication failed"
        except Exception as e:
            response["reason"] = str(e)

        return response, None, False

    def handle_add_nominee(self, request):
        response = {
            "type": RequestType.GENERIC_RESPONSE.value,
            "status": "FAILED",
            "reason": "Invalid request"
        }

        try:
            if "campaign_id" not in request or "name" not in request:
                response["reason"] = "Missing required fields"
                return response

            campaign_id = request["campaign_id"]
            name = request["name"]

            if not isinstance(campaign_id, int) or not isinstance(name, str):
                response["reason"] = "Invalid field types"
                return response

            if name.strip() == "":
                response["reason"] = "Nominee name cannot be empty"
                return response

            campaign_info = self.dal.get_campaign_info(campaign_id)
            if campaign_info is None:
                response["reason"] = "Campaign not found"
                return response

            is_activated = campaign_info['is_active']
            if not is_activated:
                self.dal.add_nominee_to_campaign(campaign_id, name)
                response["status"] = "SUCCESS"
                response["reason"] = ""
            else:
                response["reason"] = "Campaign is already activated"

        except Exception as e:
            response["reason"] = str(e)

        return response

    def handle_add_voter(self, request):
        response = {
            "type": RequestType.GENERIC_RESPONSE.value,
            "status": "FAILED",
            "reason": "Invalid request"
        }

        try:
            if "username" not in request or "password" not in request:
                response["reason"] = "Missing required fields"
                return response

            username = request["username"]
            password = request["password"]

            if not isinstance(username, str) or not isinstance(password, str):
                response["reason"] = "Invalid field types"
                return response

            if username.strip() == "" or password.strip() == "":
                response["reason"] = "User name and password cannot be empty"
                return response

            if self.dal.get_voter(username):
                response["reason"] = "Voter already exists"
                return response

            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            self.dal.add_voter(username, hashed_password)

            response["status"] = "SUCCESS"
            response["reason"] = ""
        except Exception as e:
            response["reason"] = str(e)

        return response

    def handle_get_results(self, request):
        response = {
            "type": RequestType.GET_RESULTS_RESPONSE.value,
            "status": "FAILED",
            "reason": "Invalid request"
        }

        try:
            if "campaign_id" not in request:
                response["reason"] = "Missing required field 'campaign_id'"
                return response

            campaign_id = request["campaign_id"]

            if not isinstance(campaign_id, int):
                response["reason"] = "Invalid field type for 'campaign_id'"
                return response

            campaign_info = self.dal.get_campaign_info(campaign_id)
            if campaign_info is None:
                response["reason"] = "Campaign not found"
                return response

            public_key_str = campaign_info['public_key']
            tally_votes_in_batches(self.dal, campaign_id, public_key_str)
            results = self.dal.get_aggregated_tallies(campaign_id)

            response = {
                "type": RequestType.GET_RESULTS_RESPONSE.value,
                "status": "SUCCESS",
                "results": results
            }
        except Exception as e:
            response["reason"] = str(e)

        return response

    def handle_assign_voter_to_campaign_request(self, request):
        response = {
            "type": RequestType.GENERIC_RESPONSE.value,
            "status": "FAILED",
            "reason": "Invalid request"
        }

        try:
            if "voter_name" not in request or "campaign_id" not in request:
                response["reason"] = "Missing required fields"
                return response

            voter_name = request["voter_name"]
            campaign_id = request["campaign_id"]

            if not isinstance(voter_name, str) or not isinstance(campaign_id, int):
                response["reason"] = "Invalid field types"
                return response

            voter = self.dal.get_voter(voter_name)
            if voter is None:
                response["reason"] = "Voter not found"
                return response

            voter_id = voter[0]
            self.dal.assign_voter_to_campaign(voter_id, campaign_id)

            response["status"] = "SUCCESS"
            response["reason"] = ""
        except Exception as e:
            response["reason"] = str(e)

        return response
