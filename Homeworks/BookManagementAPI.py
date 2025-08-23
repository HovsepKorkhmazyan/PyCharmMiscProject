from datetime import datetime
from typing import List
from enum import Enum
from fastapi import FastAPI, Query, Body, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()


class BookSortField(str, Enum):
    ID = "id"
    TITLE = "title"
    YEAR = "year"
    AUTHOR = "author"


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class Book(BaseModel):
    id: int | None = None
    title: str = Field(..., min_length=3)
    author: str
    year: int = Field(..., ge=1500, le=datetime.now().year)
    is_available: bool = True


class BookStats(BaseModel):
    total_books: int
    available_books: int
    books_per_author: dict


books = []


@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    book.id = len(books) + 1
    books.append(book)
    return book


@app.post("/books/bulk", status_code=status.HTTP_201_CREATED)
async def bulk_create_books(book_list: List[Book]):
    created_books = []
    for book in book_list:
        book.id = len(books) + len(created_books) + 1
        created_books.append(book)

    books.extend(created_books)
    return created_books


@app.delete("/books/bulk")
async def bulk_delete_books(book_ids: List[int] = Body(...)):
    deleted_books = []
    global books

    for book_id in book_ids:
        for i, book in enumerate(books):
            if book.id == book_id:
                deleted_books.append(books.pop(i))
                break

    return {"deleted_count": len(deleted_books), "deleted_books": deleted_books}


@app.get("/books")
async def get_books(
        author: str | None = None,
        is_available: bool | None = None,
        min_year: int | None = None,
        max_year: int | None = None,
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        sort_by: BookSortField = Query(BookSortField.ID),
        order: SortOrder = Query(SortOrder.ASC)
):
    filtered_books = books.copy()

    if author:
        filtered_books = [book for book in filtered_books if author.lower() in book.author.lower()]

    if is_available is not None:
        filtered_books = [book for book in filtered_books if book.is_available == is_available]

    if min_year:
        filtered_books = [book for book in filtered_books if book.year >= min_year]

    if max_year:
        filtered_books = [book for book in filtered_books if book.year <= max_year]

    reverse = order == SortOrder.DESC
    if sort_by == BookSortField.TITLE:
        filtered_books.sort(key=lambda x: x.title, reverse=reverse)
    elif sort_by == BookSortField.YEAR:
        filtered_books.sort(key=lambda x: x.year, reverse=reverse)
    elif sort_by == BookSortField.AUTHOR:
        filtered_books.sort(key=lambda x: x.author, reverse=reverse)
    else:
        filtered_books.sort(key=lambda x: x.id, reverse=reverse)

    return filtered_books[skip:skip + limit]


@app.get("/books/search")
async def search_books(q: str):
    return [
        book for book in books
        if q.lower() in book.title.lower() or q.lower() in book.author.lower()
    ]


@app.get("/books/stats", response_model=BookStats)
async def get_book_stats():
    total_books = len(books)
    available_books = len([book for book in books if book.is_available])

    books_per_author = {}
    for book in books:
        books_per_author[book.author] = books_per_author.get(book.author, 0) + 1

    return BookStats(
        total_books=total_books,
        available_books=available_books,
        books_per_author=books_per_author
    )


@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.put("/books/{book_id}")
async def update_book(book_id: int, book_update: Book):
    for i, book in enumerate(books):
        if book.id == book_id:
            book_update.id = book_id
            books[i] = book_update
            return book_update
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i, book in enumerate(books):
        if book.id == book_id:
            return books.pop(i)
    raise HTTPException(status_code=404, detail="Book not found")
