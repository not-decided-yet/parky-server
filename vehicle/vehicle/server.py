from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .constants import VEHICLE_NAME, VEHICLE_PRIVATE_KEY, VEHICLE_PUBLIC_KEY
from .routes import handle_status, handle_v2d_request
from .services import BackendService
from .utils import get_logger

origins = ["http://localhost", "http://localhost:3000", "https://parky.ml", "https://api.parky.ml"]

logger = get_logger("Parky")


def create_app():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register handlers
    app.get("/")(handle_status)
    app.post("/v2d/authenticate")(handle_v2d_request)

    # Send register signal
    registered = BackendService.register_vehicle(VEHICLE_NAME, VEHICLE_PUBLIC_KEY, VEHICLE_PRIVATE_KEY)
    if not registered:
        logger.error("Failed to register vehicle.")
        exit(1)
    logger.info("Registered.")

    return app
