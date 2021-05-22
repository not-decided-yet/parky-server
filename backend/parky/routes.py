from datetime import datetime

from parky.database import User, ParkingLot


async def handle_status():
    return {"status": "OK", "timestamp": datetime.now()}
