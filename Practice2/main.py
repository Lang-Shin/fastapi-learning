from fastapi import FastAPI, HTTPException, status, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as starletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from schemas import AuthorCreate, AuthorResponse, BookCreate, BookResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


authors: list[dict] = [
     {
        "id": 1,
        "name": "Naomi Alderisi",
        "bio": "Writes quiet, character-driven fiction about people rebuilding their lives in small towns.",
        "initials": "NA",
  },
  {
        "id": 2,
        "name": "Femi Okonkwo-Blythe",
        "bio": "Historian turned novelist, known for meticulously researched historical fiction.",
        "initials": "FB",
  },
]

books: list[dict] = [
    {
        "id": 1,
        "title": "The Quiet Ledger",
        "authorId": 1,
        "genre": "Fiction",
        "pages": 312,
        "year": 2019,
        "description": "A bookkeeper in a dying mill town discovers a decade of falsified accounts left by her late father, and has to decide who the truth is actually for.",
        "reviews": [
            { "reviewer": "M. Ostrander", "rating": 5, "comment": "Restrained and devastating. Not a wasted sentence." },
            { "reviewer": "j.reads", "rating": 4, "comment": "Slow start, but it earns the ending." },
            { "reviewer": "Terri K.", "rating": 4, "comment": "Quietly one of the best things I read this year." },
        ],
    },
    {
        "id": 2,
        "title": "Harbor Light, 1911",
        "authorId": 2,
        "genre": "Historical Fiction",
        "pages": 428,
        "year": 2021,
        "description": "Three lighthouse keepers' families navigate a shipping strike on a fictional New England coast, based on real labor archives.",
        "reviews": [
            { "reviewer": "Dockside Reader", "rating": 5, "comment": "The research shows without ever showing off." },
            { "reviewer": "Priya S.", "rating": 5, "comment": "Immersive and humane. I felt the cold." },
        ],
    },
]

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
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"authors" : authors, "books" : books}
    )

# Authors Page Route
@app.get("/authors", include_in_schema=False)
def authors_page(request: Request):
    return templates.TemplateResponse(
        request,
        "authors.html",
        {"authors" : authors, "books" : books}
    )
    
# Author Page Route
@app.get("/authors/{author_id}", include_in_schema=False)
def get_author(request: Request, author_id: int):
    for author in authors:
        if author.get("id") == author_id:
            author_books = [b for b in books if b['authorId'] == author_id]
            
            return templates.TemplateResponse(
                request,
                "author.html",
                {"author" : author, "books" : author_books}
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found.")
    

#  Book Page Route
@app.get("/books/{book_id}", include_in_schema=False)
def get_book(request: Request, book_id: int):
    for book in books:
        if book.get("id") == book_id:
            author = next((a for a in authors if a['id'] == book.get("authorId")))
            
            return templates.TemplateResponse(
                request,
                "book.html",
                {"book" : book, "author" : author}
            )
            
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found.")


@app.get("/api/authors", response_model=list[AuthorResponse])
def get_authors():
    return authors


@app.get("/api/authors/{author_id}", response_model=AuthorResponse)
def get_author(author_id: int):
    for author in authors:
        if author.get("id") == author_id:
            return author
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found.")


@app.get("/api/books", response_model=list[BookResponse])
def get_books():
    return books;



@app.get("/api/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    for book in books:
        if book.get("id") == book_id:
            return book
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


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