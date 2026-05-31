# reference for sqlalchemy to understand the type of tables to be created
# records inside database tables

from database.database_engine import Base # foundation of tables
from sqlalchemy import ForeignKey, Column, Integer, String, Boolean
from pydantic import BaseModel, Field

# create a table of users class
class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, index=True) # primary key and indexable (1st column in table)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean)
    role = Column(String)

# create a table of book class
class Books(Base): 
    __tablename__ = 'Books'
    id = Column(Integer, primary_key=True, index=True) 
    title = Column(String)
    author = Column(String)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey('Users.id')) # foreign key = id of "Users" table

# create new class to add new book
class CreateBook(BaseModel):
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=3)

