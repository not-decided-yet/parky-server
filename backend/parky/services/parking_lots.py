import random
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from parky.database.models import ParkingLot, User
from parky.utils import Singleton


class ParkingLotService(Singleton):
    def __init__(self):
        self.vehicle_to_parking_place = dict()
        self.reserved_user = set()

    @staticmethod
    def get_all_lots(db: Session) -> List[Dict[str, Any]]:
        """
        Get all lots in our database

        :param db: SQLAlchemy DB Session
        :returns: all lots in list
        """
        results = db.query(ParkingLot).all()
        return [parking_lot.as_dict() for parking_lot in results]

    def income_car(self, db: Session, parking_id: int, vehicle_number: str) -> str:
        """
        handel incoming car

        :param db: SQLAlchemy DB Session
        :parking_id: Parking lot ID
        :vehicle_number Vehicle number of incoming car

        :returns: Parking number for incoming car
        """
        user = db.query(User).filter(User.car_number == vehicle_number).all()
        is_user = 0 if len(user) == 0 else 1

        result = db.query(ParkingLot).filter(ParkingLot._id == parking_id).first()
        lot_dict = result.as_dict()

        income_idx = -1

        if is_user:
            # choice maximum priority lots among rest
            max_p = -1
            for idx, (status, priority) in enumerate(zip(lot_dict["lots_status"], lot_dict["priority"])):
                if max_p < priority and status != "X":
                    max_p = priority
                    income_idx = idx
        else:
            # choice random among rest
            rest_lots_idx = [idx for idx, lot in enumerate(lot_dict["lots_status"]) if lot == "O"]
            income_idx = random.choice(rest_lots_idx)

        if lot_dict["lots_status"][income_idx] == "IR":
            lot_dict["lots_status"][income_idx] = "O"

        self.vehicle_to_parking_place[vehicle_number] = (parking_id, income_idx, lot_dict["lots_status"][income_idx])

        lot_dict["lots_status"][income_idx] = "X"
        result.lots_status = ",".join(lot_dict["lots_status"])
        db.commit()

        return lot_dict["lots_number"][income_idx]

    def go_out_car(self, db: Session, vehicle_number: str) -> int:
        """
        handel go_out car

        :param db: SQLAlchemy DB Session
        :parking_id: Parking lot ID
        :vehicle_number Vehicle number of going out car
        :user_id User id if driver is our user

        :returns: 1 if success, 0 if fail
        """
        user = db.query(User).filter(User.car_number == vehicle_number).all()
        user_id = None if len(user) == 0 else user.user_id

        if vehicle_number not in self.vehicle_to_parking_place:
            return 0

        if user_id and user_id in self.reserved_user:
            self.reserved_user.remove(user_id)

        parking_id, income_idx, pre_state = self.vehicle_to_parking_place[vehicle_number]
        result = db.query(ParkingLot).filter(ParkingLot._id == parking_id).first()

        lot_dict = result.as_dict()
        lot_dict["lots_status"][income_idx] = pre_state

        result.lots_status = ",".join(lot_dict["lots_status"])
        db.commit()

        return 1

    def reserve(self, db: Session, parking_id: int, user_id: str) -> int:
        """
        reserve lot

        :param db: SQLAlchemy DB Session
        :parking_id: Parking lot ID
        :user_id User id if driver is our user

        :returns: 1 if success, 0 if fail
        """
        if user_id in self.reserved_user:
            return 0

        result = db.query(ParkingLot).filter(ParkingLot._id == parking_id).first()
        lot_dict = result.as_dict()

        income_idx = -1
        max_p = -1

        for idx, (status, priority) in enumerate(zip(lot_dict["lots_status"], lot_dict["priority"])):
            if max_p < priority and status == "O":
                max_p = priority
                income_idx = idx

        lot_dict["lots_status"][income_idx] = "IR"
        result.lots_status = ",".join(lot_dict["lots_status"])

        self.reserved_user.add(user_id)
        return 1
