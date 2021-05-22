from sqlalchemy.orm import Session

from parky.database import services as svc
from parky.database.models import User
from parky.utils import get_logger

logger = get_logger()


class UserService:
    @staticmethod
    async def check_and_add_user(db: Session, name: str, ssn: str, user_id: str, password: str, public_key: str):
        print("user_id", user_id)
        result = db.query(User).filter(User.user_id == user_id).all()
        if len(result) != 0:
            print(result)
            logger.info(f"Log: user_id {user_id} is already exist")
            return False

        await svc.add_user(db, name=name, ssn=ssn, user_id=user_id, password=password, public_key=public_key)
        logger.info(f"Log: user_id {user_id} is add")
        return True
