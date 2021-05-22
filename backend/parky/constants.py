from dotenv import load_dotenv
import os

load_dotenv()

#: Endpoint of Database
DB_ENDPOINT = os.getenv("DB_ENDPOINT", None)
#: Database user
DB_USER = os.getenv("DB_USER", None)
#: Database password
DB_PASSWORD = os.getenv("DB_PASSWORD", None)
#: Endpoint of vehicle server
VEHICLE_ENDPOINT = os.getenv("VEHICLE_ENDPOINT", None)