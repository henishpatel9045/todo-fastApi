import uuid
from sqlalchemy import Column, Boolean, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship, Session

from db.connection import Base
from . import schema


class TodoItem(Base):
    __tablename__ = "todo_items"

    id = Column(
        String(length=512), primary_key=True, index=True, default=str(uuid.uuid4())
    )
    content = Column(String(length=1000))
    completed = Column(Boolean, default=False)
    user_id = Column(String(length=512), ForeignKey("users.id"), index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="todo_items")

    @staticmethod
    async def create_todo_item(todo_item: schema.TodoCreate, db: Session):
        db_todo_item = TodoItem(**dict(todo_item))
        db.add(db_todo_item)
        db.commit()
        db.refresh(db_todo_item)
        return db_todo_item

    @staticmethod
    async def get_todo_items_by_user_id(user_id: str, db: Session):
        return db.query(TodoItem).filter(TodoItem.user_id == user_id).all()

    @staticmethod
    async def get_todo_item_by_id(todo_id: str, db: Session):
        return db.query(TodoItem).filter(TodoItem.id == todo_id).first()

    @staticmethod
    async def update_todo_item(todo_id: str, todo_item: schema.TodoUpdate, db: Session):
        db_todo_item = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
        for var, value in todo_item.__dict__.items():
            if value is not None:
                setattr(db_todo_item, var, value)
        db.commit()
        db.refresh(db_todo_item)
        return db_todo_item

    @staticmethod
    async def delete_todo_item(todo_id: str, db: Session):
        db_todo_item = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
        db.delete(db_todo_item)
        db.commit()
        return db_todo_item
