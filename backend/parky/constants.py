import os

from dotenv import load_dotenv

load_dotenv()

#: Endpoint of Database
DB_SERVER = os.getenv("DB_SERVER", None)
#: Database user
DB_USER = os.getenv("DB_USER", None)
#: Database password
DB_PASSWORD = os.getenv("DB_PASSWORD", None)
#: Database name
DB_NAME = os.getenv("DB_NAME", "parky")
#: Endpoint of vehicle server
VEHICLE_ENDPOINT = os.getenv("VEHICLE_ENDPOINT", None)
#: Firebase API Key
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY", None)
#: Firebase Alert Icon
FIREBASE_ALERT_ICON = os.getenv("FIREBASE_ALERT_ICON", None)
