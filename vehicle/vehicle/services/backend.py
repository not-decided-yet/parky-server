"""Toolset for communication with backend server."""
from typing import Tuple
import requests

from vehicle.constants import BACKEND_ENDPOINT
from vehicle.utils import get_logger, rsa_encrypt
from vehicle.utils.crypto import generate_signature

logger = get_logger("BackendService")


class BackendService:
    @staticmethod
    def register_vehicle(vehicle_name: str, public_key: str, private_key: str) -> bool:
        """
        Retrieve VID from backend by using vehicle name.

        :param vehicle_name: Plate number of the vehicle
        :param public_key: Vehicle's public key
        :param private_key: Vehicle's private key
        :returns: True if success, False if not
        """
        signature = rsa_encrypt(vehicle_name, private_key)
        payload = {
            "number": vehicle_name,
            "public_key": public_key,
            "signature": generate_signature(vehicle_name, private_key),
        }

        logger.info(f"Registering vehicle {vehicle_name} {public_key} {signature}")
        response = requests.post(
            BACKEND_ENDPOINT + "/vehicle",
            headers={"Content-Type": "application/json"},
            json=payload,
        )

        return response.status_code == 200

    @staticmethod
    def v2d_auth_vehicle(vid: str, token: str) -> Tuple[str, str]:
        """
        Make request for V2D vehicle authentication.

        :param vid: Vehicle ID
        :param token: Auth token
        :returns: Tuple(second_token, public_key)
        """
        payload = {"vid": vid, "token": token}
        logger.info("V2D Authenticating to user")

        response = requests.post(
            BACKEND_ENDPOINT + "/v2d/auth/vehicle", headers={"Content-Type": "application/json"}, json=payload
        )
        if response.status_code != 200:
            raise ValueError("Error occurred while authenticating vehicle by V2D")

        result = response.json()
        return result["token"], result["public_key"]
