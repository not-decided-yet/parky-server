from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import routes as handlers
from .database import Base, engine

origins = ["http://localhost", "http://localhost:3000", "https://parky.ml"]


def create_app():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Initialize DB connection
    Base.metadata.create_all(bind=engine)

    # Register handlers
    app.get("/")(handlers.handle_status)

    app.post("/user")(handlers.handle_signup)
    app.post("/user/signin")(handlers.handle_signin)

    app.get("/vehicle")(handlers.handle_get_vehicles)
    app.get("/vehicle/{number}")(handlers.handle_find_vehicle)
    app.post("/vehicle")(handlers.handle_register_vehicle)

    app.post("/v2d/auth/{uid}/{vid}")(handlers.handle_start_session)
    app.post("/v2d/auth/vehicle")(handlers.handle_auth_vehicle)
    app.post("/v2d/auth/client")(handlers.handle_auth_client)

    app.get("/parking")(handlers.handle_get_all_parking_lot)
    app.get("/parking/{parking_id}/{user_id}")(handlers.handle_reserve)
    app.get("/parking/{parking_id}/{vehicle_number}")(handlers.handle_income_car)
    app.get("/parking/{vehicle_number}")(handlers.handle_go_out_car)

    return app
