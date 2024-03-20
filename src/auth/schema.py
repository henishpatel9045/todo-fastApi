from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserBase(BaseModel):
    username: str = Field(..., example="john_doe")
    first_name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    email: EmailStr = Field(None, example="john.doe@example.com")


class UserCreate(UserBase):
    password: str = Field(
        ..., example="password123", min_length=8, max_length=50, pattern="^[a-zA-Z0-9]*$"
    )


class UserUpdate(BaseModel):
    first_name: str = Field(None, example="John")
    last_name: str = Field(None, example="Doe")
    email: EmailStr = Field(None, example="john.doe@example.com")


class User(UserBase):
    id: str = Field(..., example="1234567890")
    created_at: datetime = Field(..., example=datetime.now())
    updated_at: datetime = Field(..., example=datetime.now())


class UserInDB(UserBase):
    id: str = Field(None, example="1234567890")
    hashed_password: str = Field(None, example="hashed_password")
    created_at: datetime = Field(None, example=datetime.now())
    updated_at: datetime = Field(None, example=datetime.now())

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.hashed_password)

    def set_password(self, password):
        self.hashed_password = pwd_context.hash(password)


class UserLogin(BaseModel):
    username: str = Field(..., example="john_doe")
    password: str = Field(..., example="password123")


class Token(BaseModel):
    access_token: str = Field(..., example="token")
    scope: str = Field("bearer", example="bearer")
