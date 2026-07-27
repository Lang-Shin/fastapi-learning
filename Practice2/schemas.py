from pydantic import BaseModel, ConfigDict, Field


class ReviewBase(BaseModel):
    reviewer: str = Field(min_length=1, max_length=200)
    rating: int = Field(ge=1, le=5)
    comment: str = Field(max_length=1000)

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    book_id: int


class AuthorBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    bio: str = Field(max_length=500)
    initials: str = Field(max_length=10)
    
class AuthorCreate(AuthorBase):
    pass

class AuthorResponse(AuthorBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    
    
class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    genre: str = Field(min_length=1, max_length=200)
    pages: int
    year: int
    description: str = Field(min_length=1)
    reviews: list[dict] = []
    
class BookCreate(BookBase):
    author_id: int

class BookResponse(BookBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    # author_id: int
    # reviews: list[ReviewResponse] 