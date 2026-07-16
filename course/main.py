from fastapi import FastAPI, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as starletteHTTPException


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

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


@app.get("/",  include_in_schema=False, name="home")
@app.get("/posts",  include_in_schema=False, name="posts")
def home(request: Request):
    return templates.TemplateResponse(
        request, 
        "home.html", 
        {"posts" : posts, "title" : "Home"}
    )
    
@app.get("/posts/{post_id}", include_in_schema=False, name="post_page")
def post_page(request: Request, post_id: int):
    for post in posts:
        if post.get('id') == post_id:
            
            title = post["title"]
            
            return templates.TemplateResponse(
                request,
                "post.html",
                {"post" : post, "title" : title}
            )
    
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Post not found")


@app.get("/api/posts")
def get_posts():
    return posts


@app.get("/api/posts/{post_id}")
def get_post(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return post
        
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Post not found")


@app.exception_handler(starletteHTTPException)
def general_http_exception_handler(request: Request, exception: starletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occured. Please check your request and try again."
    )
    
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail" : message}
        )
        
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code" : exception.status_code,
            "title" : exception.status_code,
            "message" : message
        },
        status_code = exception.status_code
    )