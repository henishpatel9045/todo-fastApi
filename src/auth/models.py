import uuid
from sqlalchemy import Column, String, DateTime, func
from db.connection import Base
from sqlalchemy.orm import Session, relationship

from .schema import UserInDB, UserUpdate


class User(Base):
    __tablename__ = "users"

    id = Column(
        String(length=512), primary_key=True, index=True, default=str(uuid.uuid4())
    )
    username = Column(String(length=100), unique=True, index=True)
    hashed_password = Column(String(length=512), nullable=False)
    email = Column(String(length=100), index=True, unique=True, nullable=True)
    first_name = Column(String(length=100))
    last_name = Column(String(length=100))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    todo_items = relationship("TodoItem", back_populates="user")

    @staticmethod
    async def get_user_by_username(username: str, db: Session):
        """
        Retrieves a user by their username.

        Returns:
            User: The user object if found, else None.
        """
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    async def get_user_by_email(email: str, db: Session):
        """
        Retrieves a user by their email.

        Returns:
            User: The user object if found, else None.
        """
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    async def get_user_by_id(id: str, db: Session):
        """
        Retrieves a user by their ID.

        Returns:
            User: The user object if found, else None.
        """
        return db.query(User).filter(User.id == id).first()

    @staticmethod
    async def create_user(user: UserInDB, db: Session):
        """
        Creates a new user.

        Returns:
            User: The created user object.
        """
        db_user = User(**dict(user))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    async def update_user(user_id: str, user: UserUpdate, db: Session):
        """
        Updates a user.

        Returns:
            User: The updated user object.
        """
        db_user = db.query(User).filter(User.id == user_id).first()
        for var, value in user.__dict__.items():
            if value is not None:
                setattr(db_user, var, value)
        db.commit()
        db.refresh(db_user)
        return db_user
