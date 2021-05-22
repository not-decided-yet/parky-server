from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text

from .database import Base


class User(Base):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=100))
    ssn = Column(String(length=14))
    user_id = Column(String(length=30))
    password = Column(String(length=30))
    public_key = Column(Text)
    car_number = Column(String(length=10), default="N/A")

    created_at = Column(DateTime, default=datetime.now)

    def as_dict(self):
        """
        Convert to appropriate dictionary structure.
        """
        return {
            "uid": self.uid,
            "name": self.name,
            "ssn": self.ssn,
            "user_id": self.user_id,
            "public_key": self.public_key,
            # Password is not provided
            "created_at": self.created_at,
        }


class ParkingLot(Base):
    __tablename__ = "parking_lots"

    _id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=100))
    longitude = Column(Float)
    latitude = Column(Float)
    is_free = Column(Boolean)
    lots = Column(Text)
    priority = Column(Text)

    created_at = Column(DateTime, default=datetime.now)

    def as_dict(self):
        """
        Convert to appropriate dictionary structure.
        """
        return {
            "_id": self._id,
            "name": self.name,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "is_free": self.is_free,
            "lots": self.lots,
            "priority": self.priority,
            "created_at": self.created_at,
        }


class Vehicle(BaseModel):
    """
    Data Type for vehicle.
    """

    #: Plate number
    number: str
    #: Public key
    public_key: str
