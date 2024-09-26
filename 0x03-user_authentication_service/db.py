#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user by arbitrary keyword arguments.
        Raises:
            - NoResultFound: if no user matches the query.
            - InvalidRequestError: if the query contains invalid parameters.
        """
        try:
            # Use the filter_by method to match the keyword arguments
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            # If no user is found
            raise NoResultFound
        except InvalidRequestError:
            # If invalid keyword arguments are passed (e.g., no_email)
            raise InvalidRequestError

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """add user to database
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user
    	
