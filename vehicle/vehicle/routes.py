from datetime import datetime
from vehicle.services.backend import BackendService

from pydantic import BaseModel

from .constants import VEHICLE_NAME, VEHICLE_PRIVATE_KEY
from .utils import rsa_encrypt, rsa_decrypt
from .services import V2DService


async def handle_status():
    return {"status": "OK", "timestamp": datetime.now(), "vehicle_number": VEHICLE_NAME}


class V2DRequest(BaseModel):
    uid: str
    encrypted_token: str


async def handle_v2d_request(data: V2DRequest):
    decrypted = rsa_decrypt(data.encrypted_token, VEHICLE_PRIVATE_KEY)
    token, public_key = BackendService.v2d_auth_vehicle(VEHICLE_NAME, decrypted)
    encrypted = rsa_encrypt(token, public_key)
    return {"vid": VEHICLE_NAME, "token": encrypted}
