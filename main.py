from fastapi import FastAPI, Depends
import database, models, schemas
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

def getdb():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.get("/books", response_model=list[schemas.ShowBook], tags=["books"])
def list_books(db:Session=Depends(getdb)):
    books = db.query(models.Book).all()
    return books
@app.post("/books", response_model=schemas.ShowBook, tags=["books"])
def create_book(req:schemas.CreateBook, db:Session=Depends(getdb)):
    new_book = models.Book(name=req.name, body=req.body, price=req.price)
    for cat_id in req.category_id:
        cat = db.query(models.Category).filter(models.Category.id == cat_id).first()    
        if cat:
            new_book.categories.append(cat)

    db.add(new_book)    
    db.commit()
    db.refresh(new_book)
    return new_book

@app.delete("/books/{id}", tags=["books"])
def delete_book(id:int, db:Session=Depends(getdb)):
    db.query(models.Book).filter(models.Book.id == id).delete()
    db.commit()
    return "done"

@app.post("/categories", response_model=schemas.ShowCategory, tags=['categories']) 
def create_blog(req:schemas.CreateCategory, db:Session=Depends(getdb)):
    new_cat = models.Category(name=req.name)
    for book_id in req.books_id: 
        book = db.query(models.Book).filter(models.Book.id==book_id).first()
        if book:
            new_cat.books.append(book)
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return new_cat

@app.get('/categories', response_model=list[schemas.ShowCategory], tags=['categories'])
def list_categories(db:Session=Depends(getdb)):
    cats = db.query(models.Category).all()
    return cats