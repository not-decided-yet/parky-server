import json
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Float, Text, Boolean
from sqlalchemy.sql.sqltypes import Boolean

from .database import Base


class User(Base):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=100))
    ssn = Column(String(length=14))
    id = Column(String(length=30))
    password = Column(String(length=30))
    public_key = Column(Text)

    created_at = Column(DateTime, default=datetime.now)

    def as_dict(self):
        """
        Convert to appropriate dictionary structure.
        """
        return {
            "uid": self.uid,
            "name": self.name,
            "ssn": self.ssn,
            "id": self.id,
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
