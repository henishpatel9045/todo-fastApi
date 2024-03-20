from fastapi import Depends, APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from auth import models, schema
from db.connection import get_db
from core.dependencies import decrypt_token, generate_token

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=schema.User)
async def register(user: schema.UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    user_in_db = schema.UserInDB(**dict(user))
    user_in_db.set_password(user.password)
    return await models.User.create_user(user_in_db, db)


@router.post("/login", response_model=schema.Token)
async def login(user: schema.UserLogin, db: Session = Depends(get_db)):
    """Login and generate access token."""
    db_user = await models.User.get_user_by_username(user.username, db)
    db_user = schema.UserInDB(**(db_user.__dict__))
    if db_user and db_user.verify_password(user.password):
        user = jsonable_encoder(schema.User(**dict(db_user)))
        token = generate_token(user)
        return {"access_token": token}
    return {"detail": "Invalid credentials"}


@router.get("/me", response_model=schema.User)
async def get_user(
    user: schema.User = Depends(decrypt_token), db: Session = Depends(get_db)
):
    """Get user information."""
    user = await models.User.get_user_by_id(user.id, db)
    return user


@router.put("/me/update", response_model=schema.User)
async def update_user(
    updated_user: schema.UserUpdate,
    user: schema.User = Depends(decrypt_token),
    db: Session = Depends(get_db),
):
    """Update user information."""
    return await models.User.update_user(user.id, updated_user, db)
