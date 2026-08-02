# main.py

from fastapi import FastAPI, HTTPException, status, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as starletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from schemas import AuthorCreate, AuthorResponse, BookCreate, BookResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
import models
from seed import Base, engine, get_db
from typing import Annotated

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


# authors: list[dict] = [
#      {
#         "id": 1,
#         "name": "Naomi Alderisi",
#         "bio": "Writes quiet, character-driven fiction about people rebuilding their lives in small towns.",
#         "initials": "NA",
#   },
#   {
#         "id": 2,
#         "name": "Femi Okonkwo-Blythe",
#         "bio": "Historian turned novelist, known for meticulously researched historical fiction.",
#         "initials": "FB",
#   },
# ]

# books: list[dict] = [
#     {
#         "id": 1,
#         "title": "The Quiet Ledger",
#         "author_id": 1,
#         "genre": "Fiction",
#         "pages": 312,
#         "year": 2019,
#         "description": "A bookkeeper in a dying mill town discovers a decade of falsified accounts left by her late father, and has to decide who the truth is actually for.",
#         "reviews": [
#             { "reviewer": "M. Ostrander", "rating": 5, "comment": "Restrained and devastating. Not a wasted sentence." },
#             { "reviewer": "j.reads", "rating": 4, "comment": "Slow start, but it earns the ending." },
#             { "reviewer": "Terri K.", "rating": 4, "comment": "Quietly one of the best things I read this year." },
#         ],
#     },
#     {
#         "id": 2,
#         "title": "Harbor Light, 1911",
#         "author_id": 2,
#         "genre": "Historical Fiction",
#         "pages": 428,
#         "year": 2021,
#         "description": "Three lighthouse keepers' families navigate a shipping strike on a fictional New England coast, based on real labor archives.",
#         "reviews": [
#             { "reviewer": "Dockside Reader", "rating": 5, "comment": "The research shows without ever showing off." },
#             { "reviewer": "Priya S.", "rating": 5, "comment": "Immersive and humane. I felt the cold." },
#         ],
#     },
#     {
#         "id": 3,
#         "title": "Return Address",
#         "author_id": 1,
#         "genre": "Fiction",
#         "pages": 274,
#         "year": 2023,
#         "description": "A postal worker in a coastal town spends a year trying to deliver a single undeliverable letter to its rightful owner.",
#         "reviews": [
#             { "reviewer": "j.reads", "rating": 4, "comment": "Gentle, funny, a little sad. Very her." },
#             { "reviewer": "Sam O.", "rating": 3, "comment": "Sweet but slight compared to The Quiet Ledger." },
#         ],
#     },
# ]

GENRE_COLOR = {
  "Fiction": "sage",
  "Historical Fiction": "ochre",
  "Poetry": "rose",
  "Essays": "rose",
  "Nonfiction": "slate",
  "Fantasy": "plum",
}


# Home Page Route
@app.get("/", include_in_schema=False)
@app.get("/home", include_in_schema=False)
def home(request: Request, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Author))
    authors = result.scalars().all()
    
    result = db.execute(select(models.Book))
    books = result.scalars().all()
    
    return templates.TemplateResponse(
        request,
        "index.html",
        {"authors" : authors, "books" : books}
    )

# Authors Page Route
@app.get("/authors", include_in_schema=False)
def authors_page(request: Request, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Author))
    authors = result.scalars().all()
    
    result = db.execute(select(models.Book))
    books = result.scalars().all()
    
    return templates.TemplateResponse(
        request,
        "authors.html",
        {"authors" : authors, "books" : books}
    )
    
# Author Page Route
@app.get("/authors/{author_id}", include_in_schema=False)
def get_author(request: Request, author_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.Author).where(models.Author.id == author_id)
    )
    author = result.scalars().first()
    
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found.")
    
    result = db.execute(
        select(models.Book).where(models.Book.author_id == author_id)
    )
    books = result.scalars().all()
    
    return templates.TemplateResponse(
        request,
        "author.html",
        {"author": author, "books": books}
    )
    

#  Book Page Route
@app.get("/books/{book_id}", include_in_schema=False)
def get_book(request: Request, book_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.Book).where(models.Book.id == book_id)
    )
    book = result.scalars().first()
    
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found.")
    
    return templates.TemplateResponse(
        request,
        "book.html",
        {"book": book, "author": book.author}
    )


@app.get("/api/authors", response_model=list[AuthorResponse])
def get_authors(db: Annotated[Session, Depends(get_db)]):
    results = db.execute(select(models.Author))
    authors = results.scalars().all()
    return authors


@app.get("/api/authors/{author_id}", response_model=AuthorResponse)
def get_author(author_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.Author).where(models.Author.id == author_id)
    )
    author = result.scalars().first()
    
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    
    return author


@app.get("/api/books", response_model=list[BookResponse])
def get_books(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Book))
    books = result.scalars().all()
    return books;



@app.get("/api/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.Book).where(models.Book.id == book_id)
    )
    book = result.scalars().first()

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found.")
    
    return book


@app.post("/api/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def add_book(book: BookCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.Author).where(models.Author.id == book.author_id)
    )
    author = result.scalars().first()
    
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found.")
    
    result = db.execute(
        select(models.Book).where(models.Book.title == book.title)
    )
    existing = result.scalars().first()
    
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book already exists.")
    
    new_book = models.Book(
        title=book.title,
        genre=book.genre,
        pages=book.pages,
        year=book.year,
        description=book.description,
        author=author,
        reviews=[models.Review(**r) for r in book.reviews]
    )
    
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    
    return new_book


@app.exception_handler(starletteHTTPException)
def general_exception_handler(request: Request, exception: starletteHTTPException):
    msg = (
        exception.detail
        if exception.detail
        else "An error occured. Please check your request and try again."
    )
    
    if request.url.path.startswith("/api"):
        return JSONResponse(status_code=exception.status_code, content={"detail": msg})
    
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "detail": msg
        },
        status_code=exception.status_code
    )
    
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()}
        )
        
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "detail": "Invalid request. Please check your input and try again."
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
    )