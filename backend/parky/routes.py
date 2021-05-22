from datetime import datetime
from typing import Optional

from fastapi import Depends, Header, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from parky.database import ParkingLot, User, get_db
from parky.services import UserService, VehicleService, V2DRelayService, ParkingLotService, UserService
from parky.utils import get_logger

logger = get_logger("RouteHandler")


# Middleware Utils
def _auth_check(authorization: str) -> Optional[str]:
    """
    Check authorization header and retrieve session data.

    :param authorization: HTTP ``Authorization`` header
    :returns: User ID if succeed, else None

    .. note::
        ``Authorization:`` header should be Bearer form:

        * ``Authorization: Bearer TOKENTOKENTOKEN``
    """
    method, token = authorization.strip().split(" ")
    if method != "Bearer":
        logger.error("Authorization method is not Bearer")
        return None

    user_service = UserService.instance()
    try:
        result = user_service.check_session(token)
    except:
        raise ValueError("Failed to retrieve user information")
        return None

    return result


# Handlers
async def handle_status():
    return {"status": "OK", "timestamp": datetime.now()}


class SignupRequest(BaseModel):
    name: str
    ssn: str
    user_id: str
    password: str
    public_key: str


async def handle_signup(signup_request: SignupRequest, db: Session = Depends(get_db)):
    response = UserService.add_user(
        db=db,
        name=signup_request.name,
        ssn=signup_request.ssn,
        user_id=signup_request.user_id,
        password=signup_request.password,
        public_key=signup_request.public_key,
    )
    if not response:
        raise HTTPException(status_code=500, detail=f"Already used user_id {signup_request.user_id}")
    return {"message": f"User {signup_request.user_id} is signed up."}


class SigninRequest(BaseModel):
    user_id: str
    password: str


async def handle_signin(signin_request: SigninRequest, db: Session = Depends(get_db)):
    user_service = UserService.instance()
    try:
        token = await user_service.signin(
            db=db,
            user_id=signin_request.user_id,
            password=signin_request.password,
        )
    except ValueError:
        raise HTTPException(status_code=401, detail=f"not existed user {signin_request.user_id} tried to sign in.")

    return {"status": True, "token": token}


async def handle_get_vehicles(response: Response, authorization: str = Header(None)):
    if _auth_check(authorization) is None:
        raise HTTPException(status_code=401, detail="Not authorized")

    vehicle_service = VehicleService.instance()
    result = vehicle_service.get_vehicles()
    if result is None or len(result) == 0:
        response.status_code = 404
        return {"reason": "No vehicle was registered"}

    return result


async def handle_find_vehicle(response: Response, number: str, authorization: str = Header(None)):
    if _auth_check(authorization) is None:
        raise HTTPException(status_code=401, detail="Not authorized")

    vehicle_service = VehicleService.instance()
    result = vehicle_service.find_vehicle_by_number(number)
    if result is None:
        response.status_code = 404
        return {"reason": "Requested vehicle is not found"}

    return result


class RegisterVehicleRequest(BaseModel):
    number: str
    public_key: str
    signature: str


async def handle_register_vehicle(data: RegisterVehicleRequest, response: Response):
    vehicle_service = VehicleService.instance()
    result = vehicle_service.register_vehicle(data.number, data.public_key, data.signature)
    if result != 0:
        response.status_code = 400
        return {"reason": "Registering vehicle is failed"}

    response.status_code = 200
    return {"ok": True}


async def handle_start_session(uid: str, vid: str):
    v2d_relay_service = V2DRelayService()
    try:
        token, public_key = v2d_relay_service.start_session(uid, vid)
    except ValueError:
        raise HTTPException(status_code=404, detail="Vehicle not found by given ids")

    return {"token": token, "public_key": public_key}


class AuthVehicleRequest(BaseModel):
    vid: str
    token: str


async def handle_auth_vehicle(data: AuthVehicleRequest):
    v2d_relay_service = V2DRelayService()
    try:
        token, public_key = v2d_relay_service.auth_vehicle(data.vid, data.token)
    except ValueError:
        raise HTTPException(status_code=404, detail="Vehicle not found by given ids")

    return {"token": token, "public_key": public_key}


class AuthClientRequest(BaseModel):
    uid: str
    token: str


async def handle_auth_client(data: AuthClientRequest):
    v2d_relay_service = V2DRelayService()
    try:
        v2d_relay_service.auth_client(data.uid, data.token)
    except ValueError:
        raise HTTPException(status_code=404, detail="Vehicle not found by given ids")

    return {"status": True}

    
async def handle_get_all_parking_lot(db: Session = Depends(get_db)):
    parking_lots = ParkingLotService.get_all_lots()
    return {"parking_lots": parking_lots}
