from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class ToDo(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False


todos = []



@app.post("/todos")
async def post_todo(todo: ToDo):
    todo.id = len(todos)+1
    todos.append(todo)
    return todo


@app.get("/todos")
async def get_todos():
    return todos


@app.get("/todos/{todo_id}")
async def get_todo_by_id(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    return None


@app.put("/todos/{todo_id}")
async def put_todo_by_id(todo_id: int, todo_update: ToDo):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            todo_update.id = todo_id
            todos[i] = todo_update
            return todo_update
    return None
