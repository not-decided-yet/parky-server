from typing import Dict, List, Optional

from parky.database import Vehicle
from parky.utils import Singleton, get_logger, verify_signature

logger = get_logger("VehicleService")


class VehicleService(Singleton):
    def __init__(self):
        self.vehicles: Dict[str, Vehicle] = {}

    def register_vehicle(self, number: str, public_key: str, signature: str, bits: int = 2048):
        """
        Register vehicle by given information.

        :param number: Vehicle's plate number
        :param public_key: Vehicle's public key
        :param signature: Signature of public key
        :param bits: Bits for RSA algorithm
        :returns: 0 if success, 1 if sanity check fail, 2 if signature verification fail

        .. note::
            Vehicle will encrypt it's plate number by it's private key,
            and will submit it as a signature.
            Server will verify it by trying to decrypt the message by public key.
        """
        if number == "" or public_key == "" or signature == "":
            logger.error("Register: insufficient data was provided")
            return 1

        decrypted = verify_signature(number, signature, public_key)
        if not decrypted:
            logger.error("Register: signature is not matched with provided public key")
            return 2

        self.vehicles[number] = Vehicle(number=number, public_key=public_key)
        logger.info(f"Register: Vehicle {number} registered")
        return 0

    def get_vehicles(self) -> List[Vehicle]:
        """
        Returns every vehicles.

        :returns: List of ``Vehicle``
        """
        return [value for value in self.vehicles.values()]

    def find_vehicle_by_number(self, number: str) -> Optional[Vehicle]:
        """
        Search vehicle list by number.

        :param number: Vehicle's plate number
        :returns: ``Vehicle`` instance if available, None if not
        """
        return self.vehicles.get(number, None)

    def deregister_vehicle(self, number: str):
        """
        Deregister vehicle from existing database.

        :param number: Vehicle's plate number
        """
        if number in self.vehicles:
            del self.vehicles[number]
