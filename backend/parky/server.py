from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routes import handle_status

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
    app.get("/")(handle_status)

    return app
