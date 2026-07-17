from fastapi import FastAPI, Request, status
from fastapi.templating import Jinja2Templates


app = FastAPI()

templates = Jinja2Templates(directory="templates")

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
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "page.html",
        {"recipes" : recipes, "title" : "Title"}
    )

@app.get("/api/posts")
def get_posts():
    return recipes