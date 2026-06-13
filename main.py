# main functions for essential services

import database_models  # import database models
from database_engine import engine
from routers import auth, books
from fastapi import FastAPI

# initialize fastapi
app = FastAPI()

#health checkpoint
@app.get("/health")
def health():
    return {"status": "ok"}

#  create databases based on models imported, if not existed
database_models.Base.metadata.create_all(bind=engine) # bind to engine

# retrieve endpoints from routers
app.include_router(auth.router)
app.include_router(books.router)
