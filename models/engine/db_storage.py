#!/usr/bin/python3
"""This script is used to manage the database for the HBNB project."""


from sqlalchemy import create_engine
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import IntegrityError
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {'User': User,
           'Place': Place,
           'State': State,
           'City': City,
           'Amenity': Amenity,
           'Review': Review}


class DBStorage:
    """this is the class for the storage of the database."""
    __engine = None
    __session = None

    def __init__(self):
        """this is the constructor for the class."""
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        db_url = f"mysql+mysqldb://{user}:{password}@{host}/{db}"

        self.__engine = create_engine(db_url, pool_pre_ping=True)

        if env == "test":
            Base.metadata.dropall(self.__engine)

    def all(self, cls=None):
        """this function is used to get all the objects from the database."""
        cls_items = []
        cls_results = {}
        if cls:
            if isinstance(cls, str):
                cls_name = classes.get(cls_name, None)
            cls_items = self.__session.query(cls_name)
        else:
            for cls_name in classes.values():
                cls_items += self.__session.query(cls_name)

        for cls_item in cls_items:
            if hasattr(cls_item, "_sa_instance_state"):
                delattr(cls_item, "_sa_instance_state")
            cls_key = f"{type(cls_item).__name__}.{cls_item.id}"
            cls_results[cls_key] = cls_item

        return cls_results

    def new(self, obj):
        """This function is used to create a new object in the database."""
        if obj:
            try:
                self.__session.add(obj)
            except Exception as e:
                print(e.message)
        else:
            return

    def save(self):
        """This function is used to save the changes in the database."""
        try:
            self.__session.commit()
        except IntegrityError as e:
            print(e._sql_message)

    def delete(self, obj):
        """This function is used to delete an object from the database."""
        if obj:
            try:
                self.__session.delete(obj)
            except Exception as e:
                print(e.message)

    def reload(self):
        """This function is used to reload the database."""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(
            bind=self.__engine, expire_on_commit=False))
        self.__session = Session()
