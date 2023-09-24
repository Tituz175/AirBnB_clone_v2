#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from os import getenv


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guests = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)

    if getenv('HBNB_TYPE_STORAGE') == "db":
        reviews = relationship(
            "Review", backref="place", cascade="all, delete"
            )

    else:
        @property
        def reviews(self):
            """
            Get reviews of place

            Keyword arguments:
            argument -- self
            Return: list of reviews instances
            """
            objects = models.storage.all(type(self))
            return [val for val in objects.items() if val.place_id == self.id]
