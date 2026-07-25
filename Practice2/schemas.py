from pydantic import BaseModel, ConfigDict, Field


class AuthorBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    bio: str = Field(max_length=500)
    initials: str = Field(max_length=500)
    
class AuthorCreate(AuthorBase):
    pass

class AuthorResponse(AuthorBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    
    
class BookBase(BaseModel):
    title: int = Field(min_length=1, max_length=100)
    genre: str = Field(min_length=1, max_length=200)
    pages: int
    year: int
    description: str = Field(min_length=1)
    reviews: list[dict]
    
class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    authorId: int