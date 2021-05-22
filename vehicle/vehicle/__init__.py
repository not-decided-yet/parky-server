from .server import create_app

__all__ = ["create_app"]
__version__ = "0.0.1"
__author__ = "Not Decided Yet (NDY)"

if __name__ == "__main__":
    print("Uvicorn is needed to start this server.")
    print("Try `uvicorn --factory vehicle:create_app --reload`.")
