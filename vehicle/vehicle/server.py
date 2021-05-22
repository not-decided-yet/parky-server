from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import handle_status, handle_v2d_request


origins = ["http://localhost", "http://localhost:3000", "https://parky.ml", "https://api.parky.ml"]


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

    return app
