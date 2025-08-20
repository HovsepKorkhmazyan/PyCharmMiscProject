from typing import Annotated

from fastapi import FastAPI, Query, Body, HTTPException
from pydantic import BaseModel

app = FastAPI()


class ToDo(BaseModel):
    id: int | None = None
    title: str
    description: str | None = None
    completed: bool = False


todos = []


@app.post("/todos")
async def post_todo(todo: ToDo):
    todo.id = len(todos) + 1
    todos.append(todo)
    return todo


@app.get("/todos")
async def get_todos(
        q: str | None = None,
        completed: bool | None = None,
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100)
):
    filtered_todos = todos

    if q:
        filtered_todos = [todo for todo in filtered_todos if q.lower() in todo.title.lower()]

    if completed is not None:
        filtered_todos = [todo for todo in filtered_todos if todo.completed == completed]

    return filtered_todos[skip:skip + limit]


@app.get("/todos/{todo_id}")
async def get_todo_by_id(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@app.put("/todos/{todo_id}")
async def put_todo_by_id(todo_id: int, todo_update: ToDo):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            todo_update.id = todo_id
            todos[i] = todo_update
            return todo_update
    raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            return todos.pop(i)
    raise HTTPException(status_code=404, detail="Todo not found")


@app.put("/todos/{todo_id}/complete")
async def mark_todo_complete(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            todo.completed = True
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@app.patch("/todos/{todo_id}/description")
async def update_description(todo_id: int, description: Annotated[str, Body(embed=True)]):
    for todo in todos:
        if todo.id == todo_id:
            todo.description = description
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")
