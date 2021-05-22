import os

from dotenv import load_dotenv

load_dotenv()

#: Plate number of the vehicle
VEHICLE_NAME = os.getenv("PARKY_VEHICLE_NAME", "ABC123")
#: File path of the public key
VEHICLE_PUBLIC_KEY_PATH = os.getenv("PARKY_VEHICLE_PUBLIC_KEY_PATH", "/keys/vehicle.pub")
#: File path of the private key
VEHICLE_PRIVATE_KEY_PATH = os.getenv("PARKY_VEHICLE_PRIVATE_KEY_PATH", "/keys/vehicle")
#: Backend endpoint
BACKEND_ENDPOINT = os.getenv("PARKY_BACKEND_ENDPOINT", "")

# Obtain keys
with open(VEHICLE_PRIVATE_KEY_PATH, "r", encoding="utf-8") as f:
    VEHICLE_PRIVATE_KEY = f.read()

with open(VEHICLE_PUBLIC_KEY_PATH, "r", encoding="utf-8") as f:
    VEHICLE_PUBLIC_KEY = f.read()
