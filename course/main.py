from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

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

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
@app.get("/api/posts", response_class=HTMLResponse, include_in_schema=False)
def home():
    return f"<h1>{posts[0]['author']}</h1>"

@app.get("/api/posts")
def get_posts():
    return posts