from datetime import datetime
from typing import Annotated, List
from enum import Enum
from fastapi import FastAPI, Query, Body, HTTPException, status
from pydantic import BaseModel, validator

app = FastAPI()


class SortField(str, Enum):
    ID = "id"
    TITLE = "title"
    DUE_DATE = "due_date"


class ToDo(BaseModel):
    id: int | None = None
    title: str
    description: str | None = None
    completed: bool = False
    due_date: datetime | None = None

    @validator('due_date')
    def validate_due_date(cls, value):
        if value and value < datetime.now():
            raise ValueError("Due date must be today or in the future")
        return value


class ToDoCreate(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False
    due_date: datetime | None = None

    @validator('due_date')
    def validate_due_date(cls, value):
        if value and value < datetime.now():
            raise ValueError("Due date must be today or in the future")
        return value


todos = []


def is_title_unique(title: str) -> bool:
    return all(todo.title.lower() != title.lower() for todo in todos)


@app.get("/todos/overdue")
async def get_overdue_todos():
    now = datetime.now()
    return [
        todo for todo in todos
        if not todo.completed and todo.due_date and todo.due_date < now
    ]


@app.post("/todos", status_code=status.HTTP_201_CREATED)
async def post_todo(todo: ToDo):
    if not is_title_unique(todo.title):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Todo with this title already exists"
        )

    todo.id = len(todos) + 1
    todos.append(todo)
    return todo


@app.post("/todos/bulk", status_code=status.HTTP_201_CREATED)
async def bulk_create_todos(todo_list: List[ToDoCreate]):
    if not todo_list:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Todo list cannot be empty"
        )

    created_todos = []


    titles_in_request = [todo.title.lower() for todo in todo_list]
    if len(set(titles_in_request)) != len(titles_in_request):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Duplicate titles found in the request"
        )


    for todo_create in todo_list:
        if not is_title_unique(todo_create.title):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Todo with title '{todo_create.title}' already exists"
            )


    for todo_create in todo_list:
        new_todo = ToDo(
            id=len(todos) + 1,
            **todo_create.model_dump()
        )
        todos.append(new_todo)
        created_todos.append(new_todo)

    return created_todos


@app.delete("/todos/completed", status_code=status.HTTP_200_OK)
async def bulk_delete_completed_todos():
    completed_todos = [todo for todo in todos if todo.completed]

    if not completed_todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No completed todos found to delete"
        )


    global todos
    todos = [todo for todo in todos if not todo.completed]

    return {
        "message": f"Deleted {len(completed_todos)} completed todos",
        "deleted_count": len(completed_todos),
        "deleted_todos": completed_todos
    }


@app.get("/todos")
async def get_todos(
        q: str | None = None,
        completed: bool | None = None,
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        sort_by: SortField = Query(SortField.ID)
):
    filtered_todos = todos.copy()

    if q:
        filtered_todos = [todo for todo in filtered_todos if q.lower() in todo.title.lower()]

    if completed is not None:
        filtered_todos = [todo for todo in filtered_todos if todo.completed == completed]


    if sort_by == SortField.TITLE:
        filtered_todos.sort(key=lambda x: x.title)
    elif sort_by == SortField.DUE_DATE:
        filtered_todos.sort(key=lambda x: x.due_date or datetime.max)
    else:
        filtered_todos.sort(key=lambda x: x.id)

    return filtered_todos[skip:skip + limit]


@app.get("/todos/{todo_id}")
async def get_todo_by_id(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")


@app.put("/todos/{todo_id}")
async def put_todo_by_id(todo_id: int, todo_update: ToDo):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            todo_update.id = todo_id
            todos[i] = todo_update
            return todo_update
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")


@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            return todos.pop(i)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")


@app.put("/todos/{todo_id}/complete")
async def mark_todo_complete(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            todo.completed = True
            return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")


@app.patch("/todos/{todo_id}/description")
async def update_description(todo_id: int, description: Annotated[str, Body(embed=True)]):
    for todo in todos:
        if todo.id == todo_id:
            todo.description = description
            return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
