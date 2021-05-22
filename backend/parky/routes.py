from datetime import datetime

from fastapi import Depends, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from parky.database import ParkingLot, User, get_db
from parky.services import UserService, VehicleService


async def handle_status():
    return {"status": "OK", "timestamp": datetime.now()}


class SignupRequest(BaseModel):
    name: str
    ssn: str
    user_id: str
    password: str
    public_key: str


async def handle_sign_up(signup_request: SignupRequest, db: Session = Depends(get_db)):
    response = await UserService.check_and_add_user(
        db=db,
        name=signup_request.name,
        ssn=signup_request.ssn,
        user_id=signup_request.user_id,
        password=signup_request.password,
        public_key=signup_request.public_key,
    )
    if not response:
        raise HTTPException(status_code=500, detail=f"Already used user_id {signup_request.user_id}")
    return {"message": f"User {signup_request.user_id} is add"}


async def handle_find_vehicle(response: Response, number: str):
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
    print(data)
    result = vehicle_service.register_vehicle(data.number, data.public_key, data.signature)
    if result != 0:
        response.status_code = 400
        return {"reason": "Registering vehicle is failed"}

    return {"ok": True}
