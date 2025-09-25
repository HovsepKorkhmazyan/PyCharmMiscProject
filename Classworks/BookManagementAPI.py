from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional


class Book(BaseModel):
    author: str
    name: str
    pages: int

app = FastAPI(
    title="Book Management API",
)

DB_FILE = "db.txt"


def read_db() -> List[Book]:
    books = []
    try:
        with open(DB_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        author, name, pages = line.split(',')
                        books.append(Book(author=author.strip(), name=name.strip(), pages=int(pages.strip())))
                    except ValueError:

                        print(f"Skipping malformed line: {line}")
                        continue
    except FileNotFoundError:

        open(DB_FILE, "w").close()
    return books


def write_db(books: List[Book]):
    with open(DB_FILE, "w") as f:
        for book in books:
            f.write(f"{book.author},{book.name},{book.pages}\n")


@app.get("/books", response_model=List[Book], tags=["Books"])
def get_all_books():
    return read_db()


@app.get("/books/author/{author_name}", response_model=List[Book], tags=["Books"])
def get_books_by_author(author_name: str):
    books = read_db()
    books_by_author = [book for book in books if book.author.lower() == author_name.lower()]
    if not books_by_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No books found for author: {author_name}"
        )
    return books_by_author


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED, tags=["Books"])
def add_book(book: Book):
    books = read_db()

    if any(b.name.lower() == book.name.lower() for b in books):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Book with name '{book.name}' already exists."
        )
    books.append(book)
    write_db(books)
    return book


@app.put("/books/{book_name}", response_model=Book, tags=["Books"])
def update_book(book_name: str, updated_book: Book):
    books = read_db()
    book_to_update_index = -1
    for i, b in enumerate(books):
        if b.name.lower() == book_name.lower():
            book_to_update_index = i
            break

    if book_to_update_index == -1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with name '{book_name}' not found."
        )

    books[book_to_update_index] = updated_book
    write_db(books)
    return updated_book


@app.delete("/books/{book_name}", status_code=status.HTTP_204_NO_CONTENT, tags=["Books"])
def delete_book(book_name: str):
    books = read_db()
    original_count = len(books)
    books_to_keep = [b for b in books if b.name.lower() != book_name.lower()]

    if len(books_to_keep) == original_count:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with name '{book_name}' not found."
        )

    write_db(books_to_keep)
    return None
