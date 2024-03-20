from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth import schema as auth_schema
from core.dependencies import decrypt_token
from db.connection import get_db
from . import schema, models

router = APIRouter(tags=["Todo"])


@router.post("", response_model=schema.Todo)
async def create(
    todo_item: schema.TodoCreate,
    user: auth_schema.User = Depends(decrypt_token),
    db: Session = Depends(get_db),
):
    """
    Create a new todo item.
    """
    todo_item.user_id = user.id
    return await models.TodoItem.create_todo_item(todo_item, db)


@router.get("", response_model=list[schema.Todo])
async def get(
    user: auth_schema.User = Depends(decrypt_token),
    db: Session = Depends(get_db),
):
    """
    Get all todo items for the authenticated user.
    """
    return await models.TodoItem.get_todo_items_by_user_id(user.id, db)


@router.put("/{todo_id}", response_model=schema.Todo)
async def update(
    todo_id: str,
    todo_item: schema.TodoUpdate,
    user: auth_schema.User = Depends(decrypt_token),
    db: Session = Depends(get_db),
):
    """
    Update a todo item.
    """
    db_todo_item = await models.TodoItem.get_todo_item_by_id(todo_id, db)
    if db_todo_item.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await models.TodoItem.update_todo_item(todo_id, todo_item, db)


@router.delete("/{todo_id}", response_model=schema.Todo)
async def delete(
    todo_id: str,
    user: auth_schema.User = Depends(decrypt_token),
    db: Session = Depends(get_db),
):
    """
    Delete a todo item.
    """
    db_todo_item = await models.TodoItem.get_todo_item_by_id(todo_id, db)
    if db_todo_item.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await models.TodoItem.delete_todo_item(todo_id, db)
