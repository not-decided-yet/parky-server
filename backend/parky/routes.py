from datetime import datetime

from fastapi import Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from parky.database import get_db
from parky.services import UserService


async def handle_status():
    return {"status": "OK", "timestamp": datetime.now()}


class SignupRequest(BaseModel):
    name: str
    ssn: str
    user_id: str
    password: str
    public_key: str


async def handle_sign_up(signup_request: SignupRequest, db: Session = Depends(get_db)):
    print(*signup_request)
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
