from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models
from app.database import engine
from app.routers import post, user, auth, misc, vote
from fastapi_pagination import add_pagination

# this like help in createtable when we save first our code but after use of alembic in code we dont need this
# models.Base.metadata.create_all(bind=engine)
origins = ["https://www.google.com"]  # this contain list of domain
description = """
You can do cool stuff.

## With Functionality:-

## USERS
You can create **User**.
## POST
You can create **Post**.

You will be able to:
* **like post of other users**.
"""
app = FastAPI(
    title="Shivam Fast Api",
    description=description,
    contact={"email": "shivamsharma199802@gmail.com"},
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # for public use ["*"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(misc.router)
app.include_router(vote.router)
