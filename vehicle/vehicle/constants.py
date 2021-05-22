from dotenv import load_dotenv
import os

load_dotenv()

#: Plate number of the vehicle
VEHICLE_NAME = os.getenv("PARKY_VEHICLE_NAME", "ABC123")
#: File path of the public key
VEHICLE_PUBLIC_KEY_PATH = os.getenv("PARKY_VEHICLE_PUBLIC_KEY_PATH", "/keys/vehicle.pub")
#: File path of the private key
VEHICLE_PRIVATE_KEY_PATH = os.getenv("PARKY_VEHICLE_PRIVATE_KEY_PATH", "/keys/vehicle")
#: Backend endpoint
BACKEND_ENDPOINT = os.getenv("PARKY_BACKEND_ENDPOINT", "")
