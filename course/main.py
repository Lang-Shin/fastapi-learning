from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

posts: list[dict] = [
    {
        "id" : 1,
        "author" : "Charise Kimberly",
        "title" : "Isn't Biologist Beautiful",
        "content" : "The art of being a Biologist in CSM",
        "date_posted" : "August 8, 2024"
    },
    {
        "id" : 2,
        "author" : "Shijme Pacheco",
        "title" : "Isn't Computer Scientist Beautiful",
        "content" : "The art of being a Computer Scientist in CEIT",
        "date_posted" : "August 8, 2024"
    }
]


@app.get("/",  include_in_schema=False)
@app.get("/posts",  include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(
        request, 
        "home.html", 
        {"posts" : posts, "title" : "Home"}
    )


@app.get("/api/posts")
def get_posts():
    return posts