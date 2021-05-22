from datetime import datetime

from .constants import VEHICLE_NAME


async def handle_status():
    return {"status": "OK", "timestamp": datetime.now(), "vehicle_number": VEHICLE_NAME}


async def handle_v2d_request():
    return {"status": "OK"}
