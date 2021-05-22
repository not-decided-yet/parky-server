from sqlalchemy.orm import Session

from parky.database.models import User


def add_user(db: Session, name, ssn, user_id, password, public_key):
    user = User(name=name, ssn=ssn, user_id=user_id, password=password, public_key=public_key)

    db.add(user)
    db.commit()
