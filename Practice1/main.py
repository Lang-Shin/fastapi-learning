from fastapi import FastAPI, Request, status, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as starletteHTTPException
from schema import RecipeResponse, RecipeCreate

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")    # for CSS / JS

# Init data
recipes: list[dict] = [
    {
        "id": 1,
        "title": "Chicken Adobo",
        "ingredients": [
            "1/2 kilo chicken thighs",
            "1/4 cup soy sauce",
            "1/4 cup vinegar",
            "4 cloves garlic, crushed",
            "2 bay leaves",
            "1 tsp whole peppercorns"
        ],
        "steps": [
            "Marinate chicken in soy sauce, vinegar, and garlic for 30 minutes.",
            "Bring everything to a boil, then simmer uncovered for 25 minutes.",
            "Add bay leaves and peppercorns, simmer until sauce thickens."
        ],
        "cook_time_minutes": 45
    },
    {
        "id": 2,
        "title": "Garlic Fried Rice",
        "ingredients": [
            "3 cups day-old rice",
            "6 cloves garlic, minced",
            "3 tbsp cooking oil",
            "Salt to taste"
        ],
        "steps": [
            "Fry garlic in oil until golden and crisp, set aside.",
            "Fry the rice in the garlic oil until heated through.",
            "Season with salt, top with the fried garlic bits."
        ],
        "cook_time_minutes": 15
    },
    {
        "id": 3,
        "title": "Simple Pancakes",
        "ingredients": [
            "1 cup all-purpose flour",
            "1 tbsp sugar",
            "1 egg",
            "3/4 cup milk",
            "1 tsp baking powder"
        ],
        "steps": [
            "Whisk dry ingredients together in a bowl.",
            "Add egg and milk, whisk until just combined (small lumps are fine).",
            "Cook on a greased pan over medium heat until bubbles form, then flip."
        ],
        "cook_time_minutes": 20
    }
]

@app.get("/", include_in_schema=False)
@app.get("/home", include_in_schema=False)
@app.get("/recipes", include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "page.html",
        {"recipes" : recipes, "title" : "Title"}
    )

@app.get("/recipes/{recipe_id}", include_in_schema=False)
def get_recipe(request: Request, recipe_id: int):
    for recipe in recipes:
        if recipe.get("id") == recipe_id:
            
            return templates.TemplateResponse(
                request,
                "page.html",
                {
                    "recipes" : recipes, 
                    "active_recipe" : recipe,
                    "title" : recipe.get("title")
                }
            )
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")


@app.get("/api/recipes", response_model=list[RecipeResponse])
def get_recipes():
    return recipes


@app.get("/api/recipes/{recipe_id}", response_model=RecipeResponse)
def get_recipe(recipe_id: int):
    for recipe in recipes:
        if recipe.get("id") == recipe_id:
            return recipe
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe Not Found.")


@app.post("/api/recipes", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
def add_recipe(recipe: RecipeCreate):
    new_id = max(r['id'] for r in recipes) + 1 if recipe else 1
    
    new_recipe = {
        "id" : new_id,
        "title" : recipe.title,
        "ingredients" : recipe.ingredients,
        "steps" : recipe.steps,
        "cook_time_minutes" : recipe.cook_time_minutes
    }
    
    recipes.append(new_recipe)
    
    return new_recipe


@app.exception_handler(starletteHTTPException)
def general_http_exception_handler(request: Request, exception: starletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occured. Please check your request and try again."
    )
    
    if request.url.path.startswith("/api"):
        return JSONResponse(status_code=exception.status_code, content={"detail" : message})
    
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code" : exception.status_code,
            "title" : exception.status_code,
            "detail" : message
        },
        status_code=exception.status_code
    )
    
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content= {"content" : exception.errors()}
        )
        
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code" : status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title" : status.HTTP_422_UNPROCESSABLE_CONTENT,
            "detail" : "Invalid Request. Please check your input and try again."
        },
        status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    )