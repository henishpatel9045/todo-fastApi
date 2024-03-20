from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from auth.routes import router as auth_router
from todo.routes import router as todo_router

app = FastAPI()
app.title = "Todo App Rest API"
app.description = "A simple todo app with authentication and authorization"


@app.exception_handler(Exception)
async def handle_exception(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc.args[0] if exc.args else "An error occurred")},
    )


app.include_router(auth_router, prefix="/auth")
app.include_router(todo_router, prefix="/todo")
