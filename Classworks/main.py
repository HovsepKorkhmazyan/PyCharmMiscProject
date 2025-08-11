from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

books = [
    {"author": "George Orwell", "title": "1984", "year": 1949},
    {"author": "Harper Lee", "title": "To Kill a Mockingbird", "year": 1960},
    {"author": "F. Scott Fitzgerald", "title": "The Great Gatsby", "year": 1925},
    {"author": "Jane Austen", "title": "Pride and Prejudice", "year": 1813}
]

class Book(BaseModel):
    author: str = Field(..., min_length=2)
    title: str = Field(..., min_length=1)
    year: int = Field(..., gt=0, le=2024)

@app.get("/books")
async def get_all_books(limit: int = 10):
    return books[:limit]

@app.get("/books/{title}")
async def get_book_by_title(title: str):
    for book in books:
        if book["title"].lower() == title.lower():
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books")
async def post_book(book: Book):
    for existing_book in books:
        if existing_book["title"].lower() == book.title.lower():
            raise HTTPException(status_code=400, detail="Book already exists!")

    new_book = {
        "author": book.author,
        "title": book.title,
        "year": book.year
    }
    books.append(new_book)
    return new_book

@app.delete("/books/{title}")
async def delete_book_by_title(title: str):
    for i, book in enumerate(books):
        if book["title"].lower() == title.lower():
            deleted_book = books.pop(i)
            return {"message": "Book deleted", "deleted_book": deleted_book}
    raise HTTPException(status_code=404, detail="Book not found")


