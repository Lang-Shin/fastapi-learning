from pydantic import BaseModel, ConfigDict, Field


class RecipeBase(BaseModel):
    title : str = Field(min_length=1, max_length=100)
    ingredients : list[str] = Field(min_length=1, max_length=500)
    steps : list[str] = Field(min_length=1, max_length=500)
    cook_time_minutes : int 
    

class RecipeResponse(RecipeBase):
    model_config = ConfigDict(from_attributes=True)
    
    id : int