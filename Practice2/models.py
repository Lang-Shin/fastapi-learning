from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from seed import Base


class Author(Base):
    __tablename__ = "authors"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    bio: Mapped[str | None] = mapped_column(String(500), nullable=True)
    initials: Mapped[str | None] = mapped_column(String(10), nullable=True)
    
    books: Mapped[list["Book"]] = relationship(back_populates="author", cascade="all, delete-orphan")
    

class Book(Base):
    __tablename__ = 'books'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    genre: Mapped[str] = mapped_column(String(200), nullable=False)
    pages: Mapped[int] = mapped_column(Integer, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)        # Foreign Key
    
    author: Mapped["Author"] = relationship(back_populates="books", cascade="all, delete-orphan")
    reviews: Mapped[list["Review"]] = relationship(back_populates="book", cascade="all, delete-orphan")
    
    
class Review(Base):
    __tablename__ = 'reviews'
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    reviewer: Mapped[str] = mapped_column(String(100), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    book_id: Mapped["Book"] = mapped_column(ForeignKey("books.id"), nullable=False)
    
    book: Mapped["Book"] = relationship(back_populates="reviews")