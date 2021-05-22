from typing import Dict, List, NamedTuple, Tuple

from parky.database import get_db
from parky.services import UserService, VehicleService
from parky.utils import Singleton, generate_random_token


class Session(NamedTuple):
    #: User ID
    uid: str
    #: Vehicle ID
    vid: str


class V2DRelayService(Singleton):
    def __init__(self):
        self.tokens_by_session: Dict[Session : List[str]] = {}
        self.session_by_token: Dict[str:Session] = {}

    def start_session(self, uid: str, vid: str) -> Tuple[str, str]:
        """
        Starts auth session by given UID and VID, and returns first token and public key of the vehicle.

        :param uid: User ID
        :param vid: Vehicle ID
        :returns: Tuple consists of generated first token and public key of the vehicle
        """
        # Obtain the public key of the vehicle
        vehicle_service = VehicleService.instance()
        try:
            vehicle = vehicle_service.find_vehicle_by_number(vid)
        except ValueError:
            raise ValueError("Vehicle not found by given vid")

        # Registration
        session = Session(uid, vid)
        token = generate_random_token(32)
        self.tokens_by_session[session] = [token]
        self.session_by_token[token] = session

        return token, vehicle.public_key

    def auth_vehicle(self, vid: str, token: str):
        # Token check
        session = self.session_by_token.get(token)
        if session is None:
            raise ValueError("Session not found")

        if session.vid != vid:
            raise ValueError("Vehicle ID is not matched")

        token_list = self.tokens_by_session[session]
        if len(token_list) == 2:
            raise ValueError("Vehicle authentication is already done for this session")

        if token_list[0] != token:
            raise ValueError("Token mismatch.")

        # Obtain the public key of the user
        user_service = UserService.instance()
        user = user_service.get_user_by_id(session.uid)
        if user is None:
            raise ValueError("User ID not found")

        # Issue new token
        second_token = generate_random_token(32)
        self.tokens_by_session[session].append(second_token)
        self.session_by_token[second_token] = session

        return (second_token, user)

    def auth_client(self, uid: str, second_token: str):
        with get_db() as db:
            # Check user id
            user_service = UserService.instance()
            user = user_service.get_user_by_id(db, uid)
            if user is None:
                raise ValueError("User ID not found")

            # Token Check
            session = self.session_by_token.get(second_token)
            if session is None:
                raise ValueError("Session not found")

            if session.uid != uid:
                raise ValueError("User ID is not matched")

            token_list = self.tokens_by_session[session]
            if len(token_list) == 1:
                raise ValueError("Need to do vehicle authentication first")

            if token_list[1] != second_token:
                raise ValueError("Token mismatch")

            # Register and Clear
            user_service.add_car_to_user(db, uid, session.vid)
            del self.tokens_by_session[session]
            for token in token_list:
                del self.session_by_token[token]
