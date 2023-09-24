#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from os import getenv
from models.amenity import Amenity
from models.review import Review


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id',
                             String(60),
                             ForeignKey('places.id'),
                             nullable=False,
                             primary_key=True),

                      Column('amenity_id',
                             String(60),
                             ForeignKey('amenities.id'),
                             nullable=False,
                             primary_key=True))


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

        amenities = relationship(
            "Amenity", secondary=place_amenity,
            viewonly=False,
            back_populates="place_amenities"
        )

    else:
        @property
        def reviews(self):
            import models
            """
            Get reviews of place

            Keyword arguments:
            argument -- self
            Return: list of reviews instances
            """
            objects = models.storage.all(Review)
            return [val for val in objects.items() if val.place_id == self.id]

        @property
        def amenities(self):
            import models
            """
            Get reviews of place

            Keyword arguments:
            argument -- self
            Return: list of reviews instances
            """
            objects = models.storage.all(Amenity)
            return [
                val for val in objects.items()
                if val.amenities_id is self.amenity_ids
                ]

        @amenities.setter
        def amenities(self, amenities):
            """
            Set amenities of place

            Keyword arguments:
            argument -- self
            Return: list of reviews instances
            """
            if isinstance(amenities, Amenity):
                self.amenity_ids.append(amenities.id)
