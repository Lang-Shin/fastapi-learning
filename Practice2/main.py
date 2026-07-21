from fastapi import FastAPI, HTTPException, status, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates





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


@app.get("/", include_in_schema=False)
@app.get("/home", include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"authors" : authors, "books" : books}
    )


@app.get("/api/authors")
def get_authors():
    return authors


@app.get("/api/author/{author_id}")
def get_author(author_id: int):
    for author in authors:
        if author.get("id") == author_id:
            return author
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found.")


@app.get("/api/books")
def get_books():
    return books;



@app.get("/api/book/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book.get("id") == book_id:
            return book
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
