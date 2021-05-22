from sqlalchemy.orm import Session

from parky.database import services as svc
from parky.database.models import User
from parky.utils import get_logger

logger = get_logger()


class UserService:
    @staticmethod
    async def check_and_add_user(db: Session, name: str, ssn: str, user_id: str, password: str, public_key: str):
        result = db.query(User).filter(User.user_id == user_id).all()
        if len(result) != 0:
            logger.info(f"Log: already existed user {user_id} try to sign up.")
            return False

        await svc.add_user(db, name=name, ssn=ssn, user_id=user_id, password=password, public_key=public_key)
        logger.info(f"Log: user {user_id} sign up.")
        return True

    @staticmethod
    async def check_log_in(db: Session, user_id: str, password: str):
        result = db.query(User).filter(User.user_id == user_id).all()
        if len(result) != 0:
            logger.info(f"Log: user {user_id} log in.")
            return True

        logger.info(f"Log: not existed user {user_id} try login.")
        return False
