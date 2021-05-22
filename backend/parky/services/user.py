from typing import Dict, Optional

from sqlalchemy.orm import Session

from parky.database import services as svc
from parky.database.models import User
from parky.utils import Singleton, generate_random_token, get_logger

logger = get_logger()


class UserService(Singleton):
    def __init__(self):
        self.token_by_id: Dict[str, str] = {}
        self.id_by_token: Dict[str, str] = {}

    def signin(self, db: Session, user_id: str, password: str) -> str:
        """
        Signin with given user ID and password.

        :param db: SQLAlchemy DB Session
        :param user_id: User's username
        :param password: User's password
        :returns: token if succeed, else raises ``ValueError``
        """
        result = db.query(User).filter(User.user_id == user_id).one_or_none()
        if result is None:
            logger.info(f"Log: Not existed user {user_id} tried to sign in.")
            raise ValueError(f"User {user_id} does not exist")
        if result.password != password:
            logger.info(f"Log: Password not matched")
            raise ValueError(f"Password not matched")

        logger.info(f"Log: User {user_id} signed in.")
        token = generate_random_token(32)
        self.token_by_id[user_id] = token
        self.id_by_token[token] = user_id
        return token

    def get_user_by_id(self, db: Session, user_id: str) -> Optional[User]:
        """
        Get user by ID.

        :param db: SQLAlchemy DB Session
        :param user_id: User's id
        :returns: User
        """
        return db.query(User).filter(User.user_id == user_id).one_or_none()

    def check_session(self, token: str) -> str:
        """
        Check the session data based on given token.

        :param token: Session token
        :returns: User ID if succeed, else raise ``ValueError``
        """
        if token not in self.id_by_token:
            raise ValueError("No information is available by given token")
        return self.id_by_token[token]

    @staticmethod
    def add_user(db: Session, name: str, ssn: str, user_id: str, password: str, public_key: str):
        result = db.query(User).filter(User.user_id == user_id).all()
        if len(result) != 0:
            logger.info(f"Log: Already existed user {user_id} tried to sign up.")
            return False

        svc.add_user(db, name=name, ssn=ssn, user_id=user_id, password=password, public_key=public_key)
        logger.info(f"Log: User {user_id} signed up.")
        return True
