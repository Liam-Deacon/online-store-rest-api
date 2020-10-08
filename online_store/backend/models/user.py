"""Module describing users as an ORM model."""
from enum import Enum, auto
from passlib.hash import pbkdf2_sha256 as sha256

from .database import db


class UserRole(Enum):
    """Enumeration representing different user roles.

    Attributes
    ----------
    USER: int
        Indicates the user is a normal user.
    ADMIN: int
        Indicates the user can perform administrative actions.  
    """
    USER: int = auto()
    ADMIN: int = auto()

    def __int__(self) -> int:
        """Convenience method for the integer value of the enum instance."""
        return self.value

    def __str__(self) -> str:
        """Convenience method to return a string name of the enum instance."""
        return self.name


class UserModel(db.Model):
    """Model representing a user.

    Attributes
    ----------
    id: int
        The unique ID of the user.
    username: str
        The unique username of the user.
    email: str
        The unique email address of the user.
    password: str
        A SHA256 hash representation of the user's password.
    role: int
        The role of the user, default is standard user.
    phone_number: Optional[str]
        The user's phone number.
    address: Optional[str]
        The user's address.

    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.Integer, default=int(UserRole.USER))
    phone_number = db.Column(db.String(16))
    address = db.Column(db.String(2000))

    def __int__(self) -> int:
        return self.id

    def __str__(self) -> str:
        return self.username

    def __repr__(self) -> str:
        return f'<{UserRole(self.role)} {self.username!r}>'

    @staticmethod
    def generate_hash(password: str) -> str:
        """Generate password hash using SHA256 algorithm."""
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password: str, hash: str) -> str:
        """Verifies `password` against stored password `hash`."""
        return sha256.verify(password, hash)
