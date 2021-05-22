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
    app.post("/user")(handlers.handle_sign_up)
    app.get("/vehicle/{number}")(handlers.handle_find_vehicle)
    app.post("/vehicle")(handlers.handle_register_vehicle)

    return app
