#!/usr/bin/env python3
"""
Definition of _hash_password and other functions
"""
import bcrypt
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar, Optional
from db import DB
from user import User

U = TypeVar('User')


def _hash_password(password: str) -> bytes:
    """
    Hashes a password string and returns it in bytes form
    Args:
        password (str): password in string format
    """
    passwd = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(passwd, bcrypt.gensalt())
    return hashed_password


def _generate_uuid() -> str:
    """Generate a new UUID and return its string representation."""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self) -> None:
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user and return a user object
        Args:
            email (str): new user's email address
            password (str): new user's password
        Return:
            if no user with given email exists, return newly created user
            else raise ValueError
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed = _hash_password(password)
            usr = self._db.add_user(email, hashed)
            return usr
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate user login credentials
        Args:
            email (str): Email address of the user
            password (str): Password of the user
        Returns:
            bool: Returns True if login credentials are valid, otherwise False
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            if existing_user:
                encoded_hashed_pwd = password.encode()
                user_pwd_bytes = existing_user.hashed_password.encode("utf-8")
                return bcrypt.checkpw(encoded_hashed_pwd, user_pwd_bytes)
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> Optional[str]:
        """
        Create a session for a user.

        Args:
            email (str): Email that the user used in registration

        Returns:
            Optional[str]: Session ID if successful, None if otherwise.
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(existing_user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None
