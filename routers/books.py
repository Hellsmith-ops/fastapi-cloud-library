# FUNCTIONS FOR GET, POST, UPDATE, DELETE

from database.database_models import Users, Books, CreateBook # import database models
from typing import Annotated
from sqlalchemy.orm import Session
from database.database_engine import SessionLocal
from fastapi import APIRouter, Depends, HTTPException, status, Path
from .auth import get_current_user

# initialize fastapi routers
router = APIRouter()

# function to call database object
def get_db(): 
    db = SessionLocal() # imported from database engine
    # open database only when necessary,
    try: 
        yield db
    finally:
        db.close() # then close right after

# save dependency injection into a var
db_dependency = Annotated[Session, Depends(get_db)] 
# Depends(get_db) declares a FastAPI dependency
# Annotated[Session, ...] attaches that dependency metadata to the type Session.
# Session is imported from sqlalchemy.orm so FastAPI knows that kind of object expected from get_db() function.

user_dependency = Annotated[dict, Depends(get_current_user)]

# create fastapi endpoint to fetch all books
# call FastAPI() via router
@router.get('/')
# create function to read_all from database imported from database engine
async def read_all(db: db_dependency): # database object is stored in db_dependency
    return db.query(Books).all() # class Books called from models.py 

# endpoint to fetch book by ID
@router.get('/book/{book_id}')
# read_by_id function:
async def read_by_id(db: db_dependency, book_id: int): # typing

    # get first match of Books.id
    book_model = db.query(Books)
    book_model.filter(Books.id == book_id).first() 

    # error handling to accept null value
    if book_model is not None: 
        return book_model # else
    raise HTTPException(status_code=404, detail="Book not found, try again") # True if book_model is null

# endpoint to create new book:
@router.post('/create', status_code=status.HTTP_201_CREATED)
# create_book function:
async def create_book(user: user_dependency, db: db_dependency, book_created: CreateBook):

    if user is None: 
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    
    book_model = Books(**book_created.model_dump(), owner_id=user.get('id'))
    # book_update.model_dump() converts the BookUpdate Pydantic model into a dictionary.
    # ** unpacks that dictionary into keyword arguments.
    # Books(**...) creates a new Books ORM model instance with those unpacked values as fields.
    # example use: Books(title="New Book", author="Author One")

    db.add(book_model) 
    # stages the new Books ORM instance into the session 
    # ORM instance represents a single database record
    # queues it for insertion
    db.commit()
    # executes the transaction and write it to the database
    # without commit(), the transaction stays in short memory

# endpoint to update existing books 
@router.put('/book/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_book(db: db_dependency, 
                      book_id: int, 
                      book_created: CreateBook):
    
    # get first match of Books.id
    book_model = db.query(Books).filter(Books.id == book_id).first()

    # error handling to accept null value
    if book_model is None: 
        raise HTTPException(status_code=404, detail="Book not found, try again")
    
    book_model.title = book_created.title # type: ignore
    book_model.description = book_created.description # type: ignore
    book_model.rating = book_created.rating # type: ignore
    db.add(book_model)
    db.commit()

# endpoint to delete book
@router.delete('/book/{book_id}')
async def delete_book(db: db_dependency, 
                      book_id: int = Path(gt=0)):
    
    # get first match of Books.id
    book_model = db.query(Books).filter(Books.id == book_id).first()

    # error handling to accept null value
    if book_model is None: 
        raise HTTPException(status_code=404, detail="Book not found, try again")
    
    db.query(Books).filter(Books.id == book_id).delete()
    db.commit()