"""Toolset for communication with backend server."""
import requests

from vehicle.constants import BACKEND_ENDPOINT
from vehicle.utils import get_logger, rsa_encrypt
from vehicle.utils.crypto import generate_signature

logger = get_logger("BackendService")


class BackendService:
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
        return response.status_code != 200
