#!/usr/bin/python3
"""This module defines a class User"""
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = "users"
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))
    places = relationship("Place", backref="user", cascade="all, delete, delete-orphan")
    reviews = relationship("Review", backref="user", cascade="all, delete, delete-orphan")
