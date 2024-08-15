#!/usr/bin/env python3
"""Module to hash password and interact with DB
"""
import bcrypt
from sqlalchemy.exc import NoresultFound
from db import DB
from user import User

def _hash_password(password: str) -> bytes:
    """Hashing password using bcrypt
    """
    encoded_pwd = password_encode("utf_8")
    
    salt = bcrypt.gensalt()
    hashed_pwd  = bcrypt.hashpw(encoded_pwd, salt)
 
    return hashed_pwd


class Auth:
    """
    Auth class to interact with the authentication Database
    """
    def __init__(self) -> None:
        """
        Initialize Auth instance
        """
        self._db = DB()
    
    def register_user(self, email: str, password: str) -> User:
        """Register a new user with  a unique email

        Args:
            email (str): User email
            password (str): User password

        Returns:
            User: Returns User Object
        """
        try:
            existing_user = self._db.find_user_by(email=email)
        
            if existing_user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass
        
        hashed_pwd = _hash_password(password)
        
        new_user = self._db.add_user(email=email, 
                                     hashed_password=hashed_pwd.decode("utf-8"))
        self._db
        return new_user