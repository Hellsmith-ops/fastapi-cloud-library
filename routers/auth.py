# FUNCTIONS FOR OAUTH AND API SECURITY

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from database.database_models import Users
from database.database_engine import SessionLocal
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone
import os
from dotenv import load_dotenv

# initialize fastapi routers
router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

# secret key and algo for JWT
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

if not SECRET_KEY:
    raise RuntimeError("Missing SECRET_KEY environment variable.")

# initialize password hashing
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/token')

# create a reusable class for users
class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

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

# function to authenticate user
def authenticate_user(username: str, password: str, db): # take username and password via input
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

# function to create access token
def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    # take sub and id value of JWT and save into encode
    encode = {'sub': username, 'id': user_id} 
    # take current time and save into expires
    expires = datetime.now(timezone.utc) + expires_delta # Coordinated Universal Time
    encode.update({'exp': expires}) 
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='could not validate user.')
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='could not validate user.')

# endpoint to create new user
@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, 
                      create_user_request: CreateUserRequest):
    
    # assign user's inputs into CreateUserRequest class 
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password), # password to be hashed
        is_active=True
    )

    # save to database's persistent memory
    db.add(create_user_model)
    db.commit()

# endpoint to return JSON Web Token
@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='could not validate user.')
    
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}
