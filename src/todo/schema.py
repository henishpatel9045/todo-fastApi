from datetime import datetime
from pydantic import BaseModel, Field

class TodoBase(BaseModel):
    content: str = Field(..., example="Finish homework")
    completed: bool = Field(False, example=False)


class TodoCreate(TodoBase):
    user_id: str = Field(..., example="user123")


class TodoUpdate(BaseModel):
    content: str = Field(None, example="Update task")
    completed: bool = Field(None, example=True)


class Todo(TodoBase):
    id: str = Field(..., example="task123")
    user_id: str = Field(..., example="user123")
    created_at: datetime = Field(..., example=datetime.now())
    updated_at: datetime = Field(..., example=datetime.now())
