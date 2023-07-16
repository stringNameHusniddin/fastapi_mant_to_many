from database import Base
from sqlalchemy import Integer, String, ForeignKey, Table, Column, Float
from sqlalchemy.orm import relationship


bookCategory = Table(
    "bookCategory",
    Base.metadata,
    Column("category_id", Integer, ForeignKey("books.id")),
    Column("books_id", Integer, ForeignKey("category.id"))
)

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True)
    
    name = Column(String)
    body =  Column(String)
    price = Column(Float)
    
    categories = relationship("Category", secondary=bookCategory, back_populates="books")
    
class Category(Base):
    __tablename__ = "category"
    
    id = Column(Integer, primary_key=True)
    
    name = Column(String)
    
    books = relationship("Book", secondary=bookCategory, back_populates="categories")