from pydantic import BaseModel

class Book(BaseModel):
    name : str
    body : str
    price : float

class CreateBook(Book):
    category_id : list[int] = []

class Category(BaseModel):
    name : str
    
class ShowBook(Book):
    id : int
    categories : list[Category]=[]    

    class Config:
        orm_model = True
        
class CreateCategory(Category):
    books_id : list[int] = []
    
class ShowCategory(Category):
    id : int
    books : list[Book]=[]
    
    class Config:
        orm_model = True