from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import InvalidRequestError, NoResultFound

from user import User

Base = declarative_base()

class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by arbitrary keyword arguments."""
        for key in kwargs.keys():
            if not hasattr(User, key):
                raise InvalidRequestError()

            user = self._session.query(User).filter_by(**kwargs).first()
            if user:
                return user
            raise NoResultFound()
    def update_user(self, user_id: int, **kwargs) -> None:
        """
        
        """
        user_to_update = self.find_user_by(id=user_id)
        
        for attr, value in kwargs.items():
            if hasattr(User, attr):
                set_attr(user_to_update, attr, value)
            else:
                raise ValueError()
        self.__session.commit()
    