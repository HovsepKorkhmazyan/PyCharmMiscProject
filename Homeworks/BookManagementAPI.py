from datetime import datetime
from typing import List, Optional
from enum import Enum

from fastapi import FastAPI, Query, Body, HTTPException, status, Depends
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


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3)
    author: Optional[str] = None
    year: Optional[int] = Field(None, ge=1500, le=datetime.now().year)
    is_available: Optional[bool] = None


class BookStats(BaseModel):
    total_books: int
    available_books: int
    books_per_author: dict


books: List[Book] = []
book_id_counter: int = 0


async def get_book_or_404(book_id: int) -> Book:
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.post("/books", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(book: Book):
    global book_id_counter
    book_id_counter += 1
    book.id = book_id_counter
    books.append(book)
    return book


@app.post("/books/bulk", status_code=status.HTTP_201_CREATED, response_model=List[Book])
async def bulk_create_books(book_list: List[Book]):
    global book_id_counter
    created_books = []
    for book in book_list:
        book_id_counter += 1
        book.id = book_id_counter
        created_books.append(book)

    books.extend(created_books)
    return created_books


@app.delete("/books/bulk")
async def bulk_delete_books(book_ids: List[int] = Body(...)):
    global books
    ids_to_delete = set(book_ids)

    deleted_books = [book for book in books if book.id in ids_to_delete]
    books_to_keep = [book for book in books if book.id not in ids_to_delete]

    deleted_count = len(books) - len(books_to_keep)
    books = books_to_keep

    return {"deleted_count": deleted_count, "deleted_books": deleted_books}


@app.get("/books", response_model=List[Book])
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
        filtered_books = [b for b in filtered_books if author.lower() in b.author.lower()]
    if is_available is not None:
        filtered_books = [b for b in filtered_books if b.is_available == is_available]
    if min_year:
        filtered_books = [b for b in filtered_books if b.year >= min_year]
    if max_year:
        filtered_books = [b for b in filtered_books if b.year <= max_year]

    reverse = order == SortOrder.DESC
    filtered_books.sort(key=lambda book: getattr(book, sort_by.value), reverse=reverse)

    return filtered_books[skip:skip + limit]


@app.get("/books/search", response_model=List[Book])
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


@app.get("/books/{book_id}", response_model=Book)
async def get_book_by_id(book: Book = Depends(get_book_or_404)):
    return book


@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, book_update: Book, book: Book = Depends(get_book_or_404)):
    book_index = books.index(book)
    book_update.id = book_id
    books[book_index] = book_update
    return book_update


@app.patch("/books/{book_id}", response_model=Book)
async def partial_update_book(book_update: BookUpdate, book: Book = Depends(get_book_or_404)):
    update_data = book_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(book, key, value)
    return book


@app.delete("/books/{book_id}", response_model=Book)
async def delete_book(book: Book = Depends(get_book_or_404)):
    books.remove(book)
    return book